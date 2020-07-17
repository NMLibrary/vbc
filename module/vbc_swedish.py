#!/usr/bin/env python3
import random
from .vbc_class import Player
from .vbc_base import base_push, base_push_index, remain_rank_sort, third_question_time
from .vbc_value_probability import swedish_miss_count, swedish_push_value, swedish_answer_probability

def third_round_swedish(members):
    members_number = 5
    winners_number = 2
    assert len(members) == members_number, 'メンバーが' + str(members_number) + '人になっていません'
    points = [0] * members_number
    misses = [0] * members_number
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
        answer_data = base_push(members, swedish_push_value, swedish_answer_probability)
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
            if members[lamp_index].point == 10:
                winners.append(members[lamp_index])
                members[lamp_index].win = True
        else:
            miss_data = swedish_miss_count(members[lamp_index].point)
            members[lamp_index].miss += miss_data[0]
            print(members[lamp_index].name + miss_data[1])
            members[lamp_index].result_str += '(' + miss_data[1] + ')'
            if members[lamp_index].miss >= 10:
                losers.append(members[lamp_index])
                members[lamp_index].lose = True
    if len(winners) < winners_number:
        remain_players = []
        for player in members:
            if player.win == False and player.lose == False:
                remain_players.append(player)
        remain_player_sorted = remain_rank_sort(remain_players)
        for i in range(winners_number - len(winners)):
            winners.append(remain_player_sorted[i])
    for winner in winners:
        winner.win = True
    for player in members:
        player.score_str = str(player.point) + '○' + str(player.miss) + '×'
    print([player.name + ' ' + player.result_str + ' ' + player.score_str for player in members])
    return winners, members