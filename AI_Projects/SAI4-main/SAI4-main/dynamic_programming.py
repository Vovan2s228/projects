#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dynamic Programming 
Practical for course 'Symbolic AI'
2020, Leiden University, The Netherlands
By Thomas Moerland
"""

import numpy as np
from world import World

class Dynamic_Programming:

    def __init__(self):
        self.V_s = None # will store a potential value solution table
        self.Q_sa = None # will store a potential action-value solution table
        
    def value_iteration(self,env,gamma = 1.0, theta=0.001):
        ''' Executes value iteration on env. 
        gamma is the discount factor of the MDP
        theta is the acceptance threshold for convergence '''

        print("Starting Value Iteration (VI)")
        # initialize value table
        V_s = np.zeros(env.n_states)
    
        ## IMPLEMENT YOUR VALUE ITERATION ALGORITHM HERE
        #print("You still need to implement value iteration!")
        delta = np.infty
        while delta > theta:
            delta = 0
            for state in env.states:
                x = V_s[state]
                y = -np.infty
                # update V(s) using the equation for value iteration
                for action in env.actions:
                    s_prime, r = env.transition_function(state, action)
                    temp = r + gamma * V_s[s_prime]
                    if temp > y:
                        y = temp
                V_s[state] = y
                delta = max(delta, abs(x - y))
            print('Delta/Error: ', delta) # this print statement is a part of the assignment

        self.V_s = V_s
        return

    def Q_value_iteration(self,env,gamma = 1.0, theta=0.001):
        ''' Executes Q-value iteration on env. 
        gamma is the discount factor of the MDP
        theta is the acceptance threshold for convergence '''

        print("Starting Q-value Iteration (QI)")
        # initialize state-action value table
        Q_sa = np.zeros([env.n_states,env.n_actions])

        ## IMPLEMENT YOUR Q-VALUE ITERATION ALGORITHM HERE
        #print("You still need to implement Q-value iteration!")
        delta = np.infty
        while delta > theta:
            delta = 0
            for state in env.states:
                for action_index in range(len(env.actions)):
                    x = Q_sa[state,action_index]
                    s_prime, r = env.transition_function(state, env.actions[action_index])
                    # update Q(s,a) using the q-value iteration equation
                    # over all actions, find max Q(s_prime, action_prime) called y
                    values = np.array([Q_sa[s_prime, a] for a in range(len(env.actions))])
                    y = np.max(values)
                    Q_sa[state, action_index] = r + gamma * y
                    delta = max(delta, abs(x - Q_sa[state, action_index]))
        self.Q_sa = Q_sa
        return
                
    def execute_policy(self,env,table='V'):
        ## Execute the greedy action, starting from the initial state
        env.reset_agent()
        print("Start executing. Current map:") 
        env.print_map()
        while not env.terminal:
            current_state = env.get_current_state() # this is the current state of the environment, from which you will act
            available_actions = env.actions
            # Compute action values
            if table == 'V' and self.V_s is not None:
                ## IMPLEMENT ACTION VALUE ESTIMATION FROM self.V_s HERE !!!
                #print("You still need to implement greedy action selection from the value table self.V_s!")

                # out of all possible s_prime from the current state, choose the action that leads to the one with the highest value
                state_value = -np.infty
                for action in available_actions:
                    s_prime, r = env.transition_function(current_state, action)
                    if r > 0: # final state, in this problem other states have reward -1
                        best_action = action
                        state_value = np.infty
                    elif self.V_s[s_prime] > state_value:
                        state_value = self.V_s[s_prime]
                        best_action = action

                greedy_action = best_action


            elif table == 'Q' and self.Q_sa is not None:
                ## IMPLEMENT ACTION VALUE ESTIMATION FROM self.Q_sa here !!!
                #print("You still need to implement greedy action selection from the state-action value table self.Q_sa!")

                # from the current state choose action for which Q(current state, action) is max
                state_value = -np.infty
                for action_index in range(len(available_actions)):
                    s_prime, r = env.transition_function(current_state, available_actions[action_index])
                    if r > 0: # final state
                        best_action = available_actions[action_index]
                        state_value = np.infty
                    elif self.Q_sa[current_state, action_index] > state_value:
                        state_value = self.Q_sa[current_state, action_index]
                        best_action = available_actions[action_index]

                greedy_action = best_action
                
                
            else:
                print("No optimal value table was detected. Only manual execution possible.")
                greedy_action = None


            # ask the user what he/she wants
            while True:
                if greedy_action is not None:
                    print('Greedy action= {}'.format(greedy_action))    
                    your_choice = input('Choose an action by typing it in full, then hit enter. Just hit enter to execute the greedy action:')
                else:
                    your_choice = input('Choose an action by typing it in full, then hit enter. Available are {}'.format(env.actions))
                    
                if your_choice == "" and greedy_action is not None:
                    executed_action = greedy_action
                    env.act(executed_action)
                    break
                else:
                    try:
                        executed_action = your_choice
                        env.act(executed_action)
                        break
                    except:
                        print('{} is not a valid action. Available actions are {}. Try again'.format(your_choice,env.actions))
            print("Executed action: {}".format(executed_action))
            print("--------------------------------------\nNew map:")
            env.print_map()
        print("Found the goal! Exiting \n ...................................................................... ")
    

def get_greedy_index(action_values):
    ''' Own variant of np.argmax, since np.argmax only returns the first occurence of the max. 
    Optional to uses '''
    return np.where(action_values == np.max(action_values))
    
if __name__ == '__main__':
    env = World('prison.txt') 
    DP = Dynamic_Programming()

    # Run value iteration
    input('Press enter to run value iteration')
    optimal_V_s = DP.value_iteration(env)
    input('Press enter to start execution of optimal policy according to V')
    DP.execute_policy(env, table='V') # execute the optimal policy
    
    # Once again with Q-values:
    input('Press enter to run Q-value iteration')
    optimal_Q_sa = DP.Q_value_iteration(env)
    input('Press enter to start execution of optimal policy according to Q')
    DP.execute_policy(env, table='Q') # execute the optimal policy

