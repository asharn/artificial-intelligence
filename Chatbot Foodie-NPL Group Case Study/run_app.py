from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/restaurantnlu')
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter)

input_channel = SlackInput('xoxp-730844475953-725780115683-739412025158-d93e4a27a55bf3760af40ab3dccd3342', #app verification token
							'xoxb-730844475953-737233566341-ry0DIDLBzrbH7IzOlnBAuE4R', # bot verification token
							'LhTk3o9fLiYVu7KoIvaMkGqo', # slack verification token
							True)

agent.handle_channel(HttpInputChannel(5004, '/', input_channel))