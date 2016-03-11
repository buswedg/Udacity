import random
import numpy as np
import itertools as iter
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # Initialize any additional variables here
        self.actions = ('forward','left','right',None) # set possible actions, first action is given priority
        self.states = list(iter.product(['forward','left','right'], # set possible waypoint state
                                        ['red','green'], # set possible light state
                                        [None,'forward','left','right'], # set possible oncoming traffic direction state
                                        [None,'forward','left','right'], # set possible right traffic direction state
                                        [None,'forward','left','right'])) # set possible left traffic direction state
        self.q_matrix = 10 * np.ones((len(self.states),len(self.actions))) # initialize q-matrix with values of 10.
        self.gamma = 0.05  # set discount factor
        self.alpha = 0.30  # set learning rate


    def reset(self, destination=None):
        self.planner.route_to(destination)
        # Prepare for a new trip; reset any variables here, if required
        self.cum_reward = 0 # initialize cumulative reward


    def update(self, t):
        deadline = self.env.get_deadline(self) # get current deadline value (time steps remaining)
        #location = self.env.agent_states[self]['location']
        #heading = self.env.agent_states[self]['heading']
        #light = self.env.agent_states[self]['light']

        # Update state
        self.next_waypoint = self.planner.next_waypoint()
        inputs = self.env.sense(self)
        self.state = (self.next_waypoint,
                         inputs['light'],
                         inputs['oncoming'],
                         inputs['right'],
                         inputs['left']) # get current state (traffic light and presence of cars)
        self.state_index = self.states.index(self.state) # get current state index value
        print(self.state_index, self.state)

        # Select action according to your policy
        # action = random.choice(self.actions) # action selection random (None, 'forward', 'left', 'right')
        action = self.actions[np.argmax(self.q_matrix[self.states.index(self.state)])] # action selection maximize learnt q-value (None, 'forward', 'left', 'right')
        action_index = self.actions.index(action) # get action index
        #print(action_index, action)

        # Execute action and get reward
        reward = self.env.act(self, action) # get action reward
        self.cum_reward += reward # track cumulative reward

        # Learn policy based on state, action, reward
        self.next_waypoint = self.planner.next_waypoint()
        inputs = self.env.sense(self)
        next_state = (self.next_waypoint,
                      inputs['light'],
                      inputs['oncoming'],
                      inputs['right'],
                      inputs['left']) # get next state (traffic light and presence of cars)
        next_state_index = self.states.index(next_state) # get current state index value
        #print(next_state_index, next_state)

        self.q_matrix[self.state_index,action_index] = \
            (1 - self.alpha) * self.q_matrix[self.state_index,action_index] + self.alpha * \
            (reward + self.gamma * np.max(self.q_matrix[next_state_index])) # derive q-value and update q-matrix based on state and action index
        #print(self.q_matrix[self.state_index,action_index])

        print("LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}, cum_reward = {}".format(deadline, inputs, action, reward, self.cum_reward))  # process the inputs and update the current state


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=1.0)  # reduce update_delay to speed up simulation
    sim.run(n_trials=10)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
