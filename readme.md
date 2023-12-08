# NLPDL Assignment 4: LLM as Agent

This is the code implementation of assignment 4 of NLPDL, PKU 2023 Fall.

# Installation

* Set up the AlfWorld environment following the [link](https://github.com/alfworld/alfworld)

* Install openai library: `pip install openai==0.28`

* Set openai api key: `export OPENAI_API_KEY='Your API KEY'`

For ones who are struggling with installing the AlfWorld environment, it's highly recommended to use Docker by the following commands.

Pull [vzhong's image](https://hub.docker.com/r/vzhong/alfworld): `docker pull vzhong/alfworld`

# Run Act framework

`python play.py --mode act`

One successful case is shown in `result_act.txt`.

# Run ReAct framework

`python play.py --mode react`

One successful case is shown in `result_react.txt`.

# Reference

[[ICLR 2023] ReAct: Synergizing Reasoning and Acting in Language Models](https://github.com/ysymyth/ReAct)

[ALFWorld: Aligning Text and Embodied Environments for Interactive Learning](https://github.com/alfworld/alfworld)

[openai-python](https://github.com/openai/openai-python)