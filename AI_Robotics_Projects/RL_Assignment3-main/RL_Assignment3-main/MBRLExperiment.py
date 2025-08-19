#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MBRLExperiment.py

Run experiments for DynaAgent and PrioritizedSweepingAgent as specified.
"""

import time
import numpy as np
from MBRLEnvironment import WindyGridworld
from MBRLAgents import DynaAgent, PrioritizedSweepingAgent
from Helper import LearningCurvePlot, smooth

def run_repetitions(agent_class, n_repetitions, n_timesteps, eval_interval, 
                    epsilon, learning_rate, gamma, n_planning_updates, wind_proportion):
    """
    Run multiple independent repetitions of training an agent and record 
    its performance (mean return) every eval_interval steps.
    """
    times = np.arange(0, n_timesteps, eval_interval)
    n_points = len(times)
    returns = np.zeros((n_repetitions, n_points))
    for i in range(n_repetitions):
        env = WindyGridworld(wind_proportion=wind_proportion)
        agent = agent_class(env.n_states, env.n_actions, learning_rate, gamma)
        s = env.reset()
        eval_index = 0
        for t in range(n_timesteps):
            a = agent.select_action(s, epsilon)
            s_next, r, done = env.step(a)
            agent.update(s, a, r, done, s_next, n_planning_updates)
            if t % eval_interval == 0:
                eval_env = WindyGridworld(wind_proportion=wind_proportion)
                returns[i, eval_index] = agent.evaluate(
                    eval_env, n_eval_episodes=30, max_episode_length=100)
                eval_index += 1
            if done:
                s = env.reset()
            else:
                s = s_next
    avg_returns = np.mean(returns, axis=0)
    return times, avg_returns

def main():
    # Experiment parameters
    n_timesteps = 10001
    eval_interval = 250
    n_repetitions = 20
    gamma = 1.0
    learning_rate = 0.2
    epsilon = 0.1

    wind_proportions = [0.9, 1.0]

    # Store average returns for each agent, wind, and planning
    results = {'dyna': {}, 'ps': {}}

    # Compute Q-learning baseline (DynaAgent with 0 planning) for each wind
    for wind in wind_proportions:
        times, avg_returns = run_repetitions(
            DynaAgent, n_repetitions, n_timesteps, eval_interval,
            epsilon, learning_rate, gamma, 0, wind)
        results['dyna'].setdefault(wind, {})[0] = (times, avg_returns)

    # Run experiments for DynaAgent (planning 1,3,5) and PSAgent (planning 1,3,5)
    for wind in wind_proportions:
        # DynaAgent
        for n_planning in [1, 3, 5]:
            times, avg_returns = run_repetitions(
                DynaAgent, n_repetitions, n_timesteps, eval_interval,
                epsilon, learning_rate, gamma, n_planning, wind)
            results['dyna'][wind][n_planning] = (times, avg_returns)
        # Prioritized Sweeping Agent
        results['ps'].setdefault(wind, {})
        for n_planning in [1, 3, 5]:
            times, avg_returns = run_repetitions(
                PrioritizedSweepingAgent, n_repetitions, n_timesteps, eval_interval,
                epsilon, learning_rate, gamma, n_planning, wind)
            results['ps'][wind][n_planning] = (times, avg_returns)

    # Create learning curve plots for each agent and wind
    for agent_key, agent_label in [('dyna', 'dyna'), ('ps', 'ps')]:
        for wind in wind_proportions:
            title = f"{agent_label.capitalize()} Agent (wind={wind})"
            lc_plot = LearningCurvePlot(title=title)
            # Q-learning baseline curve (from DynaAgent with 0 planning)
            times, returns_baseline = results['dyna'][wind][0]
            smoothed_baseline = smooth(returns_baseline, window=5)
            lc_plot.add_curve(times, smoothed_baseline, label='Q-learning')
            # Add agent-specific curves
            if agent_key == 'dyna':
                for n_planning in [1, 3, 5]:
                    _, avg_ret = results['dyna'][wind][n_planning]
                    smoothed = smooth(avg_ret, window=5)
                    label = f"Dyna (planning={n_planning})"
                    lc_plot.add_curve(times, smoothed, label=label)
            else:
                for n_planning in [1, 3, 5]:
                    _, avg_ret = results['ps'][wind][n_planning]
                    smoothed = smooth(avg_ret, window=5)
                    label = f"PS (planning={n_planning})"
                    lc_plot.add_curve(times, smoothed, label=label)
            filename = f"learning_curve_{agent_label}_wind{wind}".replace('.', '_') + '.png'
            lc_plot.save(name=filename)
            print(f"Saved learning curve for {agent_label} (wind={wind}) to {filename}")

    # Determine best planning config (highest final return) for each agent and wind
    best_plans = {'dyna': {}, 'ps': {}}
    for wind in wind_proportions:
        # Best for Dyna (exclude 0)
        best_val = -np.inf
        best_plan = None
        for n_planning in [1, 3, 5]:
            _, avg_ret = results['dyna'][wind][n_planning]
            final_ret = avg_ret[-1]
            if final_ret > best_val:
                best_val = final_ret
                best_plan = n_planning
        best_plans['dyna'][wind] = best_plan
        # Best for PS
        best_val = -np.inf
        best_plan = None
        for n_planning in [1, 3, 5]:
            _, avg_ret = results['ps'][wind][n_planning]
            final_ret = avg_ret[-1]
            if final_ret > best_val:
                best_val = final_ret
                best_plan = n_planning
        best_plans['ps'][wind] = best_plan

    # Combined learning curves (Q, best Dyna, best PS) for each wind
    for wind in wind_proportions:
        title = f"Comparison (wind={wind})"
        lc_plot = LearningCurvePlot(title=title)
        times = results['dyna'][wind][0][0]
        # Q-learning
        returns_q = results['dyna'][wind][0][1]
        smoothed_q = smooth(returns_q, window=5)
        lc_plot.add_curve(times, smoothed_q, label='Q-learning')
        # Best Dyna
        best_dyna = best_plans['dyna'][wind]
        returns_dyna = results['dyna'][wind][best_dyna][1]
        smoothed_dyna = smooth(returns_dyna, window=5)
        lc_plot.add_curve(times, smoothed_dyna, label=f"Dyna (planning={best_dyna})")
        # Best PS
        best_ps = best_plans['ps'][wind]
        returns_ps = results['ps'][wind][best_ps][1]
        smoothed_ps = smooth(returns_ps, window=5)
        lc_plot.add_curve(times, smoothed_ps, label=f"PS (planning={best_ps})")
        filename = f"learning_curve_comparison_wind{wind}".replace('.', '_') + '.png'
        lc_plot.save(name=filename)
        print(f"Saved comparison learning curve for wind={wind} to {filename}")

    # Measure runtime for single repetition (n_repetitions=1) of each algorithm
    print("\nMeasuring runtimes (single repetition, n_timesteps=10001)...")
    runtimes = {'0.9': {}, '1.0': {}}
    for wind in wind_proportions:
        wind_key = str(wind)
        # Q-learning (DynaAgent with 0 planning)
        start = time.perf_counter()
        run_repetitions(DynaAgent, 1, n_timesteps, eval_interval,
                        epsilon, learning_rate, gamma, 0, wind)
        end = time.perf_counter()
        runtimes[wind_key]['Q-learning'] = end - start
        # Best Dyna
        best_dyna = best_plans['dyna'][wind]
        start = time.perf_counter()
        run_repetitions(DynaAgent, 1, n_timesteps, eval_interval,
                        epsilon, learning_rate, gamma, best_dyna, wind)
        end = time.perf_counter()
        key_dyna = f"Dyna (plan={best_dyna})"
        runtimes[wind_key][key_dyna] = end - start
        # Best PS
        best_ps = best_plans['ps'][wind]
        start = time.perf_counter()
        run_repetitions(PrioritizedSweepingAgent, 1, n_timesteps, eval_interval,
                        epsilon, learning_rate, gamma, best_ps, wind)
        end = time.perf_counter()
        key_ps = f"PS (plan={best_ps})"
        runtimes[wind_key][key_ps] = end - start

    # Print runtimes clearly
    print("\nAverage runtime per single repetition (seconds):")
    for wind in wind_proportions:
        wind_key = str(wind)
        key_dyna = f"Dyna (plan={best_plans['dyna'][wind]})"
        key_ps = f"PS (plan={best_plans['ps'][wind]})"
        print(f"Wind {wind}:")
        print(f"  Q-learning: {runtimes[wind_key]['Q-learning']:.4f} s")
        print(f"  {key_dyna}: {runtimes[wind_key][key_dyna]:.4f} s")
        print(f"  {key_ps}: {runtimes[wind_key][key_ps]:.4f} s")

if __name__ == '__main__':
    main()


