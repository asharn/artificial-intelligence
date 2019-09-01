from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/restaurantnlu')
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter)

input_channel = SlackInput('xoxp-730844475953-725780115683-744762547604-7ad4579476499fc1a3e0cbfd05f40cee', #app verification token
							'xoxb-730844475953-737233566341-teokPo062uPF5Rq7pkRC9g5C', # bot verification token
							'LhTk3o9fLiYVu7KoIvaMkGqo', # slack verification token
							True)

agent.handle_channel(HttpInputChannel(5004, '/', input_channel))