#!/usr/bin/env python3
import random
from .vbc_class import Player, third_round_course
from .vbc_base import compare_value
from functools import cmp_to_key

def third_round_priority(players):
    third_round_member = []
    for i in range(4):
        for j, player in enumerate(players[i]):
            player.win_rank = j
            third_round_member.append(player)
    third_round_member = sorted(third_round_member, key = cmp_to_key(compare_player))
    return third_round_member

def third_round_assign(third_round_member):
    course_order = [third_round_course.ox, third_round_course.updown, third_round_course.swedish, third_round_course.by]
    random.shuffle(course_order)
    third_round_players = []
    end_course = []
    used = []
    for i, player in enumerate(third_round_member):
        used.append(False)
    for i in range(4):
        course = course_order[i]
        course_players = []
        hands = []
        for player in third_round_member:
            # print(hand_up(player, course, end_course))
            if hand_up(player, course, end_course):
                hands.append(True)
            else:
                hands.append(False)
        player_count = 0
        for i in range(len(third_round_member)):
            if (not used[i] and hands[i] and player_count < 5):
                course_players.append(third_round_member[i])
                player_count += 1
                used[i] = True
        for i in reversed(range(0, len(third_round_member))):
            if (not used[i] and not hands[i] and player_count < 5):
                course_players.append(third_round_member[i])
                player_count += 1
                used[i] = True
        course_players = sorted(course_players, key = cmp_to_key(compare_player))
        third_round_players.append(course_players)
        end_course.append(course)
    return course_order, third_round_players

def hand_up(player, course, end_course):
    for hope_course in player.third_round_course:
        # print(hope_course)
        if hope_course not in end_course:
            if hope_course == course:
                return True
            else:
                return False
    # ここに来たら本当はおかしい
    return True

def compare_player(player_a, player_b):
    return compare_value(player_a.win_rank, player_b.win_rank) or compare_value(player_a.rank, player_b.rank)



