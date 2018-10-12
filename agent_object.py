from numpy.random import choice

class Agent(object):
	"""
	Encapsulates an agent
	"""
	def __init__(self, action_number=2, state_number=2, alpha=0.4):
		self.action_number = action_number
		self.state_number = state_number
		self.alpha = alpha
		self.last_action = "None"
		self.last_state = "None"
		self.actions = ["a" + str(x) for x in range(action_number)]
		self.action_rewards = {"s" + str(y):[1 for x in range(action_number)] for y in range(state_number)}
		self.action_choice = self.new_action_prob()
		self.last_movement = "None"
		self.movements = ["up", "down", "left", "right", "stay"]
		self.movement_choice = [0.2, 0.2, 0.2, 0.2, 0.2]

	def move(self):
		"""
		select a direction to move in
		"""
		self.last_movement = choice(self.movements, p=self.movement_choice)
		return(self.last_movement)


	def act(self, state):
		"""
		select an action to perform
		"""
		self.last_state = state
		action_probs = self.action_choice[state]
		self.last_action = choice(self.actions, p=action_probs)
		return(self.last_action)

	def update(self, reward):
		"""
		update the reward value associated with every state/action pair. Update action probabilities and movement probabilities accordingly
		"""
		rewards = self.action_rewards[self.last_state]
		action = int(self.last_action[1:])
		rewards[action] = reward * self.alpha + rewards[action] * (1 - self.alpha)
		self.action_rewards[self.last_state] = rewards
		self.action_choice = self.new_action_prob()
		self.movement_choice = self.new_movement_prob(reward)

	def update_external(self, reward, action, state):
		"""
		update reward values associated with state/action pairs from outside, i.e. when learning from someone else's actions and their consequences
		"""
		rewards = self.action_rewards[state]
		rewards[int(action[1:])] = reward * self.alpha + rewards[int(action[1:])] * (1 - self.alpha)
		self.action_rewards[state] = rewards
		self.action_choice = self.new_action_prob()

	def new_movement_prob(self, reward):
		"""
		create the new probability of moving in different predictions based on the reward gained on the previous move
		"""
		last_move_i = self.movements.index(self.last_movement)
		last_prob = self.movement_choice[last_move_i]
		new_prob = last_prob + self.alpha/2 * (reward - 1)
		move_choice = self.movement_choice
		move_choice[last_move_i] = new_prob
		move_choice = [max(0, x) for x in move_choice]
		total_prob = sum(move_choice)
		return([move_choice[x]/total_prob for x in range(5)])

	def new_action_prob(self):
		"""
		update the action probabilities given a new reward. The probabilities for each action given a state are the share of the reward accrued by that action given that state,
		relative to the total rewards accrued given the state
		"""
		action_probs = {}
		for i in range(self.state_number):
			state_i = "s" + str(i)
			total_reward = sum(self.action_rewards[state_i])
			action_probs[state_i] = [self.action_rewards[state_i][x]/total_reward for x in range(self.action_number)]
		return(action_probs)

if __name__ == "__main__":
	ag = Agent(2,3)
	ag.act("s1")

	correct_response = []

	for x in range(100):
		move = ag.move()
		state = choice(["s0", "s1", "s2"])
		action = ag.act(state)

		if state == "s0":
			if action == "a0":
				ag.update(3)
			else:
				ag.update(0)
		if state == "s1":
			if action == "a0":
				ag.update(0)
			else:
				ag.update(3)

		print("-----------------------------------------------------")
		print("move: ", move)
		print("state: ", state)
		print("action: ", action)
		print("movement choice: ")
		print(ag.movement_choice)
		print("action rewards: ")
		print(ag.action_rewards)
		print("action _choice: ")
		print(ag.action_choice)
		print("response_choice: ")
		print(ag.response_choice)
