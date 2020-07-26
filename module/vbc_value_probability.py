#!/usr/bin/env python3
import math

def base_value(players, index, difficulty, slash_point):
    player = players[index]
    # return max(0, player.knowledge - difficulty) + max(0, player.speed - slash_point) ** 2 / 10
    return max(0, player.knowledge - difficulty) + max(0, player.speed - slash_point) * 2

def calculate_base_probability(base_value, knowledge, difficulty, speed, slash_point):
    # return base_value + (knowledge - difficulty) ** 2 / 100 + (speed - slash_point) ** 2 / 100
    return base_value + (knowledge - difficulty) * 0.1 + (speed - slash_point) * 0.05

def base_answer_probability(players, index, difficulty, slash_point):
    player = players[index]
    value = calculate_base_probability(0.5, player.knowledge, difficulty, player.speed, slash_point)
    return value

def ox_push_value(players, index, difficulty, slash_point):
    value = base_value(players, index, difficulty, slash_point)
    player = players[index]
    if 10 - player.miss >= 5:
        value *= 1.2
    elif 10 - player.miss == 1:
        value *= 0.75
    return value

def ox_answer_probability(players, index, difficulty, slash_point):
    winner_number = 0
    for player in players:
        if player.win:
            winner_number += 1
    player = players[index]
    value = calculate_base_probability(0.45, ox_knowledge_modify(player, winner_number), difficulty, player.speed, slash_point + 2)
    if 10 - player.miss >= 5:
        value /= 1.2
    elif 10 - player.miss == 1:
        value /= 0.75
    return value

def ox_knowledge_modify(player, winner_number):
    value = player.knowledge - 1
    if winner_number == 1:
        value -= 1
    return value

def updown_answer_probability(players, index, difficulty, slash_point):
    loser_number = 0
    for player in players:
        if player.lose:
            loser_number += 1
    player = players[index]
    value = calculate_base_probability(0.6, updown_ability_modify(player, loser_number), difficulty, player.speed, slash_point)
    value += loser_number * 0.08
    return value

def updown_ability_modify(player, loser_number):
    value = player.knowledge
    if player.point <= 4:
        value += 2.5
    elif player.point <= 7:
        value += 3
    else:
        value += 3.5
    value += loser_number
    return value

def swedish_push_value(players, index, difficulty, slash_point):
    value = base_value(players, index, difficulty, slash_point)
    player = players[index]
    miss_affordability = swedish_miss_affordability(player)
    if miss_affordability == 1:
        value *= 0.75
    return value

def swedish_answer_probability(players, index, difficulty, slash_point):
    value = base_answer_probability(players, index, difficulty, slash_point)
    player = players[index]
    miss_affordability = swedish_miss_affordability(player)
    if miss_affordability == 1:
        value /= 0.75
    return value

def swedish_miss_affordability(player):
    remain_miss = 10 - player.miss
    miss_count = swedish_miss_count(player.point)[0]
    miss_affordability = (remain_miss + miss_count - 1) // miss_count
    return miss_affordability

def swedish_miss_count(point):
    if (point == 0):
        return 1, 'x'
    elif (point <= 2):
        return 2, 'xx'
    elif (point <= 5):
        return 3, 'xxx'
    else:
        return 4, 'xxxx'

def by_push_value(players, index, difficulty, slash_point):
    value = base_value(players, index, difficulty, slash_point)
    player = players[index]
    if by_increase_required_correct(player) >= 4:
        value *= 0.75
    return value

def by_answer_probability(players, index, difficulty, slash_point):
    value = base_answer_probability(players, index, difficulty, slash_point)
    player = players[index]
    if by_increase_required_correct(player) >= 4:
        value /= 0.75
    return value

def by_increase_required_correct(player):
    now_required = by_required_correct(player.point, player.miss)
    miss_required = by_required_correct(player.point, player.miss - 1)
    return miss_required - now_required

def by_required_correct(point, miss):
    if miss == 0:
        return 10000000
    score = point * miss
    return (100 - score + miss - 1) // miss

def ex_answer_probability(players, index, difficulty, slash_point):
    remain_number = 0
    for player in players:
        if not player.win and not player.lose:
            remain_number += 1
    player = players[index]
    value = calculate_base_probability(0.5, ex_ability_modify(player), difficulty, player.speed, slash_point)
    if remain_number == 2:
        value += 0.2
    return value

def ex_ability_modify(player):
    value = player.knowledge
    if player.point <= 2:
        value += 2.5
    else:
        value += 3
    return value

def final_push_value(set):
    def push_value(players, index, difficulty, slash_point):
        player = players[index]
        value = max(0, player.knowledge - difficulty) + max(0, player.speed - slash_point) * 2
        if set - player.miss >= 3:
            value *= 1.5
        elif set - player.miss == 1:
            value *= 0.75
        return value
    return push_value

def final_answer_probability(set):
    def probability(players, index, difficulty, slash_point):
        remain_number = 0
        for player in players:
            if not player.win and not player.lose:
                remain_number += 1
        player = players[index]
        base_prob = 0.7 - math.sqrt(set - 1) * 0.2
        if remain_number == 2:
            base_prob += 0.1
        value = calculate_base_probability(base_prob, player.knowledge, difficulty, player.speed, slash_point)
        if set - player.miss >= 3:
            value /= 1.5
        elif set - player.miss == 1:
            value /= 0.75
        return value
    return probability
