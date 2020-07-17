#!/usr/bin/env python3
import random
from .vbc_class import Player
from .vbc_base import base_push, base_push_index, remain_rank_sort
import math
from .vbc_value_probability import base_value, ex_answer_probability

def semifinal_assign(third_round_winners):
    players = []
    for i in range(4):
        third_round_winners[i][0].semifinal_seat = 3 - i
        players.append(third_round_winners[i][0])
        third_round_winners[i][1].semifinal_seat = 5 + i
        players.append(third_round_winners[i][1])
    return players

def extra_round_first(players, winners):
    for player in players:
        player.lose = False
    for player in winners:
        players[player.rank - 1].lose = True
    remain_players = [player for player in players if player.lose == False]
    question_count = 0
    while len(remain_players) >= 13:
        question_count += 1
        difficulty = difficulty_almost_linear(question_count)
        for player in remain_players:
            value = player.knowledge - difficulty + random.uniform(-2, 2)
            if (value < 0):
                player.lose = True
        remain_players = [player for player in remain_players if player.lose == False]
        print(str(question_count) + '問目: 残り' + str(len(remain_players)) + '人')
    return remain_players

def difficulty_sigmoid(x):
    modified_x = x - 5
    value = 1 / (1 + math.exp(-4 * modified_x)) * 10
    return value

def difficulty_almost_linear(x):
    value = x / 1.8 + random.uniform(-1, 1) + 2
    return value

def extra_round_second(players):
    players_number = len(players)
    winners_number = 1
    points = [0] * players_number
    misses = [0] * players_number
    for i, player in enumerate(players):
        player.point = points[i]
        player.miss = misses[i]
        player.win = False
        player.lose = False
        player.result_str = ''
    winners = []
    losers = []
    while len(winners) < winners_number and len(losers) < players_number - winners_number:
        answer_data = base_push(players, base_value, ex_answer_probability)
        lamp_index = answer_data[0]
        correct = answer_data[1]
        if lamp_index == -1:
            print('スルー')
            continue
        if correct:
            players[lamp_index].point += 1
            print(players[lamp_index].name + '○')
            players[lamp_index].result_str += '○'
            if players[lamp_index].point == 5:
                winners.append(players[lamp_index])
                players[lamp_index].win = True
        else:
            players[lamp_index].miss += 1
            print(players[lamp_index].name + '×')
            players[lamp_index].result_str += 'x'
            losers.append(players[lamp_index])
            players[lamp_index].lose = True
    if len(losers) == players_number - winners_number:
        remain_players = []
        for player in players:
            if player.point < 5 and player.miss < 1:
                remain_players.append(player)
        for player in remain_rank_sort(remain_players):
            winners.append(player)
    print([player.name + ' ' + player.result_str for player in players])
    return winners[0]
