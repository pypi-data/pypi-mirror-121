# -*- coding: utf-8 -*-

import time
import gym
import numpy as np
import scipy


def play_once(env, policy):
    '''执行一个回合悬崖寻路任务'''
    total_reward = 0
    state = env.reset()
    loc = np.unravel_index(state, env.shape) # 初始位置
    print(f'初始状态 = {state}, 初始位置 = {loc}')
    while True:
        action = np.random.choice(env.nA, p=policy[state])
        next_sate, reward, done, _ = env.step(action)
        loc = np.unravel_index(state, env.shape)
        print(f'动作 = {action}')
        print(f'新状态 = {state}, 新位置 = {loc}, 奖励 = {reward}')
        total_reward += reward
        if done:
            break
        state = next_sate
    return total_reward


def evaluate_bellman(env, policy, gamma=1):
    '''贝尔曼方程求解悬崖寻路问题状态价值和动作价值'''
    a, b = np.eye(env.nS), np.zeros((env.nS))
    for state in range(env.nS-1):
        for action in range(env.nA):
            pi = policy[state][action]
            for p, next_sate, reward, done in env.P[state][action]:
                a[state, next_sate] -= (pi * gamma * p)
                b[state] += (pi * reward * p)
    v = np.linalg.solve(a, b)
    q = np.zeros((env.nS, env.nA))
    for state in range(env.nS - 1):
        for action in range(env.nA):
            for p, next_state, reward, done in env.P[state][action]:
                q[state][action] += ((reward + gamma * v[next_sate]) * p)
    return v, q


def optimal_bellman(env, gamma=1):
    '''求解悬崖寻路问题贝尔曼最优方程'''
    p = np.zeros((env.nS, env.nA, env.nS))
    r = np.zeros((env.nS, env.nA))
    for state in range(env.nS-1):
        for action in range(env.nA):
            for prob, next_state, reward, done in env.P[state][action]:
                p[state, action, next_state] += prob
                r[state, action] += (reward * prob)
    c = np.ones(env.nS)
    a_ub = gamma * p.reshape(-1, env.nS) - np.repeat(
                                            np.eye(env.nS), env.nA, axis=0)
    b_ub = -r.reshape(-1)
    bounds = [(None, None),] * env.nS
    res = scipy.optimize.linprog(c, a_ub, b_ub, bounds=bounds,
                                 method='interior-point')
    v = res.x
    q = r + gamma * np.dot(p, v)
    return v, q
            

if __name__ == '__main__':
    strt_tm = time.time()
    
    # 悬崖寻路
    env = gym.make('CliffWalking-v0')
    
    print('悬崖寻路任务描述：')
    print(f'观测空间 = {env.observation_space}')
    print(f'动作空间 = {env.action_space}')
    print(f'状态数量 = {env.nS}, 动作数量 = {env.nA}')
    print(f'地图大小 = {env.shape}')
    
    # 最优策略
    actions = np.ones(env.shape, dtype=int)
    actions[-1, :] = 0
    actions[:, -1] = 2
    optional_policy = np.eye(4)[actions.reshape(-1)]
    
    # 最优策略一个回合
    total_reward = play_once(env, policy=optional_policy)
    print(f'总奖励 = {total_reward}')
    
    
    # 随机策略状态价值和动作价值求解
    policy = np.random.uniform(size=(env.nS, env.nA))
    policy = policy / np.sum(policy, axis=1)[:, np.newaxis]
    values_state, values_action = evaluate_bellman(env, policy)
    print(f'状态价值 = {values_state}')
    print(f'动作价值 = {values_action}')
    
    # 最优策略状态价值和动作价值求解
    values_state_best, values_action_best = evaluate_bellman(env,
                                                             optional_policy)
    print(f'最优状态价值 = {values_state_best}')
    print(f'最优动作价值 = {values_action_best}')
    
    
    # 贝尔曼最优方程求解
    values_state_optimal, values_action_optimal = optimal_bellman(env)
    print(f'最优状态价值 = {values_state_optimal}')
    print(f'最优动作价值 = {values_action_optimal}')
    
    # 最优策略
    optimal_actions = values_action_optimal.argmax(axis=1)
    print(f'求解最优策略 = {optimal_actions}')
    print(f'实际最优策略 = {actions.reshape(-1)}')
    
    
    print(f'used time: {round(time.time()-strt_tm, 6)}s.')
    
    
    
    
    
    
    
    
    
    
    
    
    
