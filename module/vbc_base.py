#!/usr/bin/env python3
import random
from functools import cmp_to_key
from .vbc_value_probability import base_value, base_answer_probability

def base_push(member, func_value = base_value, func_probability = base_answer_probability):
    values = []
    difficulty = random.uniform(0, 10)
    slash_point = random.uniform(0, 10)
    for i, player in enumerate(member):
        value = func_value(member, i, difficulty, slash_point)
        if player.win or player.lose:
            value = 0
        values.append(value)
    lamp_index = base_push_index(values)
    if lamp_index == -1:
        return -1, True
    answer_probability = func_probability(member, lamp_index, difficulty, slash_point)
    answer_value = random.random()
    if answer_value <= answer_probability:
        return lamp_index, True
    else:
        return lamp_index, False

def base_push_index(values):
    values_sum = []
    for i, value in enumerate(values):
        if (i == 0):
            values_sum.append(value)
        else:
            values_sum.append(value + values_sum[-1])
    lamp = random.uniform(0, values_sum[-1])
    lamp_index = -1
    for index, sum in enumerate(values_sum):
        if lamp < sum:
            lamp_index = index
            break
    return lamp_index

def compare_value(a, b):
    if a == b:
        return 0
    if a < b:
        return -1
    else:
        return 1

def compare_player(player_a, player_b):
    return compare_value(player_b.point, player_a.point) or compare_value(player_a.miss, player_b.miss) or compare_value(random.random(), random.random())

def remain_rank_sort(members):
    return sorted(members, key = cmp_to_key(compare_player))

def third_question_time():
    return random.uniform(12.5 - 4, 12.5 + 4)

def compare_course(course_a, course_b):
    return compare_value(course_a.priority, course_b.priority)

def course_sort(courses):
    return sorted(courses, key = cmp_to_key(compare_course))

def calculate_course_priority(priority):
    return priority - random.uniform(0, priority)

def rank_str(rank):
    rank_last_two = rank % 100
    if rank_last_two >= 11 and rank_last_two <= 13:
        return str(rank) + 'th'
    elif rank % 10 == 1:
        return str(rank) + 'st'
    elif rank % 10 == 2:
        return str(rank) + 'nd'
    elif rank % 10 == 3:
        return str(rank) + 'rd'
    else:
        return str(rank) + 'th'

def winner_rank_str(rank):
    if rank == 1:
        return '①'
    elif rank == 2:
        return '②'
    elif rank == 3:
        return '③'
    elif rank == 4:
        return '④'
    elif rank == 5:
        return '⑤'
    else:
        return ''

def win_or_lose_mark(player):
    if player.win:
        return 1
    elif player.lose:
        return 2
    else:
        return 0

def paper_color(rank):
    if rank <= 4:
        return 1
    elif rank <= 12:
        return 2
    elif rank <= 24:
        return 3
    elif rank <= 48:
        return 4
    else:
        return 5
