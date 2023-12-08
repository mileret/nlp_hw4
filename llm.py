import openai
import os
import pdb
import json

'''
This module is used to call the OpenAI API to generate text.
'''

# get the API key from the environment variable
API_KEY = os.environ.get('OPENAI_API_KEY')

openai.api_key = API_KEY

def llm(prompt, stop=["\n"]):
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=prompt,
      temperature=0,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=stop
    )
    return response["choices"][0]["text"]


if __name__ == '__main__':
    print(llm('>'))
