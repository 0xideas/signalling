from agent_object import Agent
from numpy.random import choice
import numpy as np


class Environment(object):
	"""
	holds an environment in the form of a board on which the agents move, and enables the movement, action and learning of the agents on the board
	"""
	def __init__(self, dimensions, agent_number, action_number, state_number):
		assert dimensions[0] * dimensions[1] >= agent_number
		self.dimensions = dimensions
		self.agent_number = agent_number
		self.action_number = action_number
		self.state_number = state_number
		self.states = ["s" + str(x) for x in range(state_number)]
		self.agents = {"A" + str(x): Agent(action_number, state_number) for x in range(agent_number)}
		self.fields = [(x,y) for x in range(dimensions[0]) for y in range(dimensions[1])]
		agent_location_id = [choice(np.arange(dimensions[0]*dimensions[1]), replace=False) for x in range(agent_number)]
		self.agent_locations = [self.fields[x] for x in agent_location_id]
		self.agent_actions = ["None" for x in self.agents]

		self.original_states = ["os0", "os1"]

	def move_all(self):
		"""
		let every agent select a direction to move in and update location
		"""
		for agent_id in self.agents:
			agent = self.agents[agent_id]
			move = agent.move()
			agent_i = int(agent_id[1:])
			new_loc = self.move_agent(self.agent_locations[agent_i], move)
			self.agent_locations[agent_i] = new_loc

	def move_agent(self, original_location, move):
		"""
		move an individual agent
		"""

		location = tuple(original_location)
		if move == "up":
			location = (location[0] - 1, location[1])
		elif move == "down":
			location = (location[0] + 1, location[1])
		elif move == "left":
			location = (location[0], location[1] - 1)
		elif move == "right":
			location = (location[0], location[1] + 1)

		if 0 <= location[0] < self.dimensions[0] and 0 <= location[1] < self.dimensions[1] and location not in self.agent_locations:
			return location
		else:
			return tuple(original_location)

	def print_board(self):
		"""
		print board with the locations of the agents
		"""

		board = np.zeros(self.dimensions)
		x = 0
		for location in self.agent_locations:
			#one cannot see the first agent
			board[location] = x + 1
			x += 1
		print(board)

	def act_all(self):
		"""
		let every agent select an action and add them to the list of agent actions
		"""
		self.agent_actions = [str("None") for x in self.agent_actions]
		for agent_id in self.agents:
			original_state = choice(self.original_states)
			agent_i = int(agent_id[1:])
			agent = self.agents[agent_id]
			state = choice(self.states)
			action = agent.act(state)

			self.agent_actions[agent_i] = action

	def update_all(self):
		"""
		update every agent with the reward associated with performing an action given a state. The reward is the square of the mean probability
		of choosing that action given that state for the neighbours of the agent in question. Furthermore, the agent learns that given another
		state, the current action is not desirable.
		"""
		for agent_id in self.agents:
			agent = self.agents[agent_id]
			state = agent.last_state
			action = agent.last_action
			neighbour_ids = self.get_neighbours(agent_id)
			neighbours = [self.agents[neighbour_id] for neighbour_id in neighbour_ids]

			neighbour_actions = []
			for neighbour in neighbours:
				positive = neighbour.action_choice[state][int(action[1:])]
				neighbour_actions.append(positive/len(neighbour_ids))

			update_value = (sum(neighbour_actions) + 2/3)**5
			print(update_value)

			for other_state in agent.action_choice.keys():
				if other_state != state:
					agent.update_external(1/update_value, action, other_state)

			agent.update(update_value)

	def get_neighbours(self, agent_id):
		"""
		get the neighbours of a given agents
		"""
		agent_i = int(agent_id[1:])
		neighbour_ids = []
		agent_location = self.agent_locations[agent_i]
		for location in self.agent_locations:
			cond1 = (abs(location[0] - agent_location[0]) == 1) and (location[1] == agent_location[1])
			cond2 = (abs(location[1] - agent_location[1]) == 1) and (location[0] == agent_location[0])
			if location != agent_location and (cond1 or cond2):
				neighbour = self.agent_locations.index(location)
				neighbour_ids.append("A" + str(neighbour))
		#self.agents[agent_id].neighbours = neighbours
		return(neighbour_ids)






if __name__ == '__main__':
	env = Environment((5,5), 5, 3, 3)
	env.print_board()

	for x in range(2000):
		print('_______________ step {} ________________'.format(x))
		env.move_all()
		env.act_all()
		env.update_all()
		env.print_board()

	for agent_id in sorted(list(env.agents.keys())):
		print("A" + str(int(agent_id[1:]) + 1), "______________________________________________________")
		agent = env.agents[agent_id]
		for key in sorted(list(agent.action_choice.keys())):
			print("situation", key, "---")
			print(agent.action_choice[key])