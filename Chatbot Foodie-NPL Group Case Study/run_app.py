from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/restaurantnlu')
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter)

input_channel = SlackInput('xoxp-730844475953-725780115683-737693631968-4b069de8b4c0f72a0b3cf4ac6423eff0', #app verification token
							'xoxb-730844475953-737233566341-JNI3gEpFmKroP2mf6rAYplgv', # bot verification token
							'LhTk3o9fLiYVu7KoIvaMkGqo', # slack verification token
							True)

agent.handle_channel(HttpInputChannel(5004, '/', input_channel))