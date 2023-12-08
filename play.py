import os
import yaml
import pdb
import json
import alfworld
import alfworld.agents.environment
import time

import argparse

from llm import llm

'''
This module contains the core loop of calling the OpenAI API to play the game.
'''


def act(env):
	'''
	Implement the Act framework.
	'''
	# see the observation and info
	observation, info = env.reset()
	observation = observation[0].replace('-= Welcome to TextWorld, ALFRED! =-\n\n', '')

	task = '/'.join(info['extra.gamefile'][0].split('/')[-3:-1])

	with open('alfworld_act.json', 'r') as reader:
		alfworld_act = json.load(reader)
	
	icl_examples = [alfworld_act[key] for key in alfworld_act.keys() if key[:-2] in task]
	icl_examples = [example.replace('Action', ">Action") for example in icl_examples]


	conversation_history = [f'''
You are an agent and you will complete a task.

---

Here are three examples:

Example 1:
{icl_examples[0]}

Example 2:
{icl_examples[1]}

Example 3:
{icl_examples[2]}

---

Here is your task:
{observation}
''']



	steps = 0
	# core loop
	while True:

		# get the user input from conversation history
		prompt = ''.join(conversation_history)
		prompt += ">"

		print(prompt)

		response = llm(prompt)
		
		if response.startswith('Action: '):
			action = response.replace('Action: ', '')
		else:
			action = response
		
		if not response.endswith('\n'):
			response += '\n'

		conversation_history.append('>' + response)
		
		observation, reward, done, info = env.step([action])
		observation, reward, done = observation[0], info['won'][0], done[0]
		if observation.startswith('You arrive at loc '):
			observation = observation[observation.find('. ')+2:]

		conversation_history.append(f'Observation: {observation}\n')

		print(f'{response}{observation}')


		if done: # if the game is over
			return reward, conversation_history

		steps += 1

		if steps >= 20:
			print('You have reached the maximum number of steps.')
			return reward, conversation_history
		
		# wait 20 seconds since we can only call the API 3 times per minute
		time.sleep(20)


def react(env):
	'''
	Implement the ReAct framework.
	'''
	# see the observation and info
	observation, info = env.reset()
	observation = observation[0].replace('-= Welcome to TextWorld, ALFRED! =-\n\n', '')

	task = '/'.join(info['extra.gamefile'][0].split('/')[-3:-1])

	with open('alfworld_react.json', 'r') as reader:
		alfworld_react = json.load(reader)
	
	icl_examples = [alfworld_react[key] for key in alfworld_react.keys() if key[:-2] in task]
	icl_examples = [example.replace('Action', ">Action") for example in icl_examples]
	icl_examples = [example.replace('Think', ">Think") for example in icl_examples]

	conversation_history = [f'''
You are an agent and you will complete a task.

---

Here are three examples:

Example 1:
{icl_examples[0]}

Example 2:
{icl_examples[1]}

Example 3:
{icl_examples[2]}

---

Here is your task:
{observation}
''']

	steps = 0
	done = False
	# core loop
	while True:

		# get the user input from conversation history
		prompt = ''.join(conversation_history)
		prompt += ">"
		print(prompt)

		response = llm(prompt)
		if not response.startswith('Action: ') and not response.startswith('Think: '):
			print(f'Your response {response} is not in the correct format. It must start with Action: or Think:')
			return False, conversation_history

		if not response.endswith('\n'):
			response += '\n'

		conversation_history.append('>' + response)
		
		if response.startswith('Think: '):
			observation = 'OK.'

		elif response.startswith('Action: '):
			action = response.replace('Action: ', '')
		
			observation, reward, done, info = env.step([action])
			observation, reward, done = observation[0], info['won'][0], done[0]
			if observation.startswith('You arrive at loc '):
				observation = observation[observation.find('. ')+2:]

		conversation_history.append(f'Observation: {observation}\n')

		print(response, observation)

		if done: # if the game is over
			return reward, conversation_history
		
		steps += 1

		if steps >= 20:
			print('You have reached the maximum number of steps.')
			return reward, conversation_history
		
		# wait 20 seconds since we can only call the API 3 times per minute
		time.sleep(20)



if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--mode', type=str, default='react', choices=['act', 'react'], help='act or react')
	args = parser.parse_args()

	os.environ['ALFWORLD_DATA'] = '/opt/work' # the path where you store the ALFWorld data

	with open('base_config.yaml') as reader:
		config = yaml.safe_load(reader)

	# in this task, we will use the eval_out_of_distribution data split
	split = "eval_out_of_distribution"
	env = alfworld.agents.environment.AlfredTWEnv(config, train_eval=split)
	env = env.init_env(batch_size=1)


	if args.mode == 'act':
		reward, conversation_history = act(env)
	elif args.mode == 'react':
		reward, conversation_history = react(env)
	else:
		raise NotImplementedError
	
	
	print(f'\nYou have completed the task with reward {reward}.\n')
	print('\nHere is the conversation history:\n')
	print(''.join(conversation_history))
