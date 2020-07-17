#!/usr/bin/env python3
import random
from .vbc_class import Player
from .vbc_base import base_push, base_push_index, third_question_time, compare_value
from functools import cmp_to_key
from .vbc_value_probability import by_push_value, by_answer_probability

def third_round_by(members):
    members_number = 5
    winners_number = 2
    assert len(members) == members_number, 'メンバーが' + str(members_number) + '人になっていません'
    points = [0] * members_number
    misses = [10] * members_number
    time = 0
    for i, player in enumerate(members):
        player.point = points[i]
        player.miss = misses[i]
        player.win = False
        player.lose = False
        player.result_str = ''
    winners = []
    losers = []
    while len(winners) < winners_number and len(losers) < members_number - winners_number and time < 15 * 60:
        answer_data = base_push(members, by_push_value, by_answer_probability)
        lamp_index = answer_data[0]
        correct = answer_data[1]
        time += third_question_time()
        if lamp_index == -1:
            print('スルー')
            continue
        if correct:
            members[lamp_index].point += 1
            print(members[lamp_index].name + '○')
            members[lamp_index].result_str += '○'
            if by_score(members[lamp_index]) >= 100:
                winners.append(members[lamp_index])
                members[lamp_index].win = True
        else:
            members[lamp_index].miss -= 1
            print(members[lamp_index].name + '×')
            members[lamp_index].result_str += 'x'
            if members[lamp_index].miss == 0:
                losers.append(members[lamp_index])
                members[lamp_index].lose = True
    # if len(losers) == members_number - winners_number:
    #     remain_players = []
    #     for player in members:
    #         if player.win == False and player.lose == False:
    #             remain_players.append(player)
    #     for player in by_remain_rank_sort(remain_players):
    #         winners.append(player)
    if len(winners) < winners_number:
        remain_players = []
        for player in members:
            if player.win == False and player.lose == False:
                remain_players.append(player)
        remain_player_sorted = by_remain_rank_sort(remain_players)
        for i in range(winners_number - len(winners)):
            winners.append(remain_player_sorted[i])
    for winner in winners:
        winner.win = True
    for player in members:
        player.score_str = str(by_score(player)) + 'p'
    print([player.name + ' ' + player.result_str + ' ' + player.score_str for player in members])
    return winners, members

def by_score(player):
    return player.point * player.miss

def by_compare_player(player_a, player_b):
    return compare_value(by_score(player_b), by_score(player_a)) or compare_value(random.random(), random.random())

def by_remain_rank_sort(members):
    return sorted(members, key = cmp_to_key(by_compare_player))