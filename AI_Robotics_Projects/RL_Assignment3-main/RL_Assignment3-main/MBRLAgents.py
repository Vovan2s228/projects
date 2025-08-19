#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model-based Reinforcement Learning policies
Practical for course 'Reinforcement Learning',
Bachelor AI, Leiden University, The Netherlands
By Thomas Moerland
"""
import numpy as np
from queue import PriorityQueue
from MBRLEnvironment import WindyGridworld
import random

class DynaAgent:

    def __init__(self, n_states, n_actions, learning_rate, gamma):
        self.n_states = n_states
        self.n_actions = n_actions
        self.learning_rate = learning_rate
        self.gamma = gamma
        # Initialize Q-values, transition counts, and reward sums
        self.Q_sa = np.zeros((n_states, n_actions))
        self.n_sa_s = np.zeros((n_states, n_actions, n_states))
        self.R_sa_s = np.zeros((n_states, n_actions, n_states))
        # Keep track of observed (state,action) pairs for planning
        self.observed_sa = set()

    def select_action(self, s, epsilon):
        # ε-greedy action selection
        if np.random.rand() < epsilon:
            return np.random.randint(self.n_actions)
        else:
            # Greedy action (break ties randomly)
            best_actions = np.flatnonzero(self.Q_sa[s] == np.max(self.Q_sa[s]))
            return np.random.choice(best_actions)

    def update(self, s, a, r, done, s_next, n_planning_updates):
        # Update model with observed transition
        self.n_sa_s[s, a, s_next] += 1
        self.R_sa_s[s, a, s_next] += r
        self.observed_sa.add((s, a))
        # Q-learning update on real experience
        if done:
            target = r
        else:
            target = r + self.gamma * np.max(self.Q_sa[s_next])
        self.Q_sa[s, a] += self.learning_rate * (target - self.Q_sa[s, a])
        # Planning updates (Dyna-Q style)
        for _ in range(n_planning_updates):
            if not self.observed_sa:
                break
            # Sample a random previously observed (s,a)
            s_p, a_p = random.choice(list(self.observed_sa))
            counts = self.n_sa_s[s_p, a_p]
            total = counts.sum()
            if total == 0:
                continue
            # Sample next state from estimated transition model
            probabilities = counts / total
            s_prime = np.random.choice(self.n_states, p=probabilities)
            # Predicted reward = average of observed rewards for (s_p,a_p,s_prime)
            r_pred = self.R_sa_s[s_p, a_p, s_prime] / self.n_sa_s[s_p, a_p, s_prime]
            # Q update using simulated experience
            target_model = r_pred + self.gamma * np.max(self.Q_sa[s_prime])
            self.Q_sa[s_p, a_p] += self.learning_rate * (target_model - self.Q_sa[s_p, a_p])

    def evaluate(self, eval_env, n_eval_episodes=30, max_episode_length=100):
        returns = []
        for i in range(n_eval_episodes):
            s = eval_env.reset()
            R_ep = 0
            for t in range(max_episode_length):
                a = np.argmax(self.Q_sa[s])  # Greedy action
                s_prime, r, done = eval_env.step(a)
                R_ep += r
                if done:
                    break
                s = s_prime
            returns.append(R_ep)
        return np.mean(returns)

class PrioritizedSweepingAgent:

    def __init__(self, n_states, n_actions, learning_rate, gamma, priority_cutoff=0.01):
        self.n_states = n_states
        self.n_actions = n_actions
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.priority_cutoff = priority_cutoff
        self.queue = PriorityQueue()
        # Initialize Q-values, transition counts, and reward sums
        self.Q_sa = np.zeros((n_states, n_actions))
        self.n_sa_s = np.zeros((n_states, n_actions, n_states))
        self.R_sa_s = np.zeros((n_states, n_actions, n_states))
        # Predecessor list for prioritized sweeping: for each state, which (s,a) lead to it
        self.predecessors = {s: set() for s in range(n_states)}

    def select_action(self, s, epsilon):
        # ε-greedy action selection
        if np.random.rand() < epsilon:
            return np.random.randint(self.n_actions)
        else:
            best_actions = np.flatnonzero(self.Q_sa[s] == np.max(self.Q_sa[s]))
            return np.random.choice(best_actions)

    def update(self, s, a, r, done, s_next, n_planning_updates):
        # Update model with observed transition
        self.n_sa_s[s, a, s_next] += 1
        self.R_sa_s[s, a, s_next] += r
        # Update predecessors of s_next
        self.predecessors[s_next].add((s, a))
        # Q-learning update on real experience
        if done:
            target = r
        else:
            target = r + self.gamma * np.max(self.Q_sa[s_next])
        old_Q = self.Q_sa[s, a]
        self.Q_sa[s, a] += self.learning_rate * (target - self.Q_sa[s, a])
        # Compute priority for (s,a)
        p = abs(target - old_Q)
        if p > self.priority_cutoff:
            # Use negative priority because Python's PriorityQueue pops smallest first
            self.queue.put((-p, (s, a)))
        # Perform K planning steps with prioritized sweeping
        for _ in range(n_planning_updates):
            if self.queue.empty():
                break
            _, (s_p, a_p) = self.queue.get()
            counts = self.n_sa_s[s_p, a_p]
            total = counts.sum()
            if total == 0:
                continue
            probabilities = counts / total
            s_prime = np.random.choice(self.n_states, p=probabilities)
            # Predicted reward for (s_p, a_p, s_prime)
            r_pred = self.R_sa_s[s_p, a_p, s_prime] / self.n_sa_s[s_p, a_p, s_prime]
            old_Q_sim = self.Q_sa[s_p, a_p]
            # Update Q for simulated experience
            target_sim = r_pred + self.gamma * np.max(self.Q_sa[s_prime])
            self.Q_sa[s_p, a_p] += self.learning_rate * (target_sim - self.Q_sa[s_p, a_p])
            # Update priorities for predecessors of state s_p
            for (s_bar, a_bar) in self.predecessors[s_p]:
                r_bar = self.R_sa_s[s_bar, a_bar, s_p] / self.n_sa_s[s_bar, a_bar, s_p]
                p_bar = abs(r_bar + self.gamma * np.max(self.Q_sa[s_p]) - self.Q_sa[s_bar, a_bar])
                if p_bar > self.priority_cutoff:
                    self.queue.put((-p_bar, (s_bar, a_bar)))

    def evaluate(self, eval_env, n_eval_episodes=30, max_episode_length=100):
        returns = []
        for i in range(n_eval_episodes):
            s = eval_env.reset()
            R_ep = 0
            for t in range(max_episode_length):
                a = np.argmax(self.Q_sa[s])  # Greedy action
                s_prime, r, done = eval_env.step(a)
                R_ep += r
                if done:
                    break
                s = s_prime
            returns.append(R_ep)
        return np.mean(returns)

def test():
    n_timesteps = 10001
    gamma = 1.0

    # Algorithm parameters
    policy = 'dyna'  # or 'ps'
    epsilon = 0.1
    learning_rate = 0.2
    n_planning_updates = 3

    # Plotting parameters
    plot = True
    plot_optimal_policy = True
    step_pause = 0.0001

    # Initialize environment and policy
    env = WindyGridworld()
    if policy == 'dyna':
        pi = DynaAgent(env.n_states, env.n_actions, learning_rate, gamma)
    elif policy == 'ps':
        pi = PrioritizedSweepingAgent(env.n_states, env.n_actions, learning_rate, gamma)
    else:
        raise KeyError(f'Policy {policy} not implemented')

    s = env.reset()
    continuous_mode = False

    for t in range(n_timesteps):
        a = pi.select_action(s, epsilon)
        s_next, r, done = env.step(a)
        pi.update(s, a, r, done, s_next, n_planning_updates)

        # Render environment
        if plot:
            env.render(Q_sa=pi.Q_sa, plot_optimal_policy=plot_optimal_policy,
                       step_pause=step_pause)

        # User input for step-by-step or continuous run
        if not continuous_mode:
            key_input = input("Press 'Enter' to execute next step, press 'c' to run full algorithm")
            continuous_mode = (key_input == 'c')

        if done:
            s = env.reset()
        else:
            s = s_next

if __name__ == '__main__':
    test()
