#!/usr/bin/env python3
import random
from .vbc_class import Player
from .vbc_base import compare_value, base_push, base_push_index, remain_rank_sort
from functools import cmp_to_key
from .vbc_value_probability import final_push_value, final_answer_probability

def final_set(players, set_number):
    players_number = 3
    winners_number = 1
    assert len(players) == players_number, 'メンバーが' + str(players_number) + '人になっていません'
    for player in players:
        player.point = 0
        player.miss = 0
        player.win = False
        player.lose = False
        player.result_str = ''
    winner_index = -1
    losers = []
    while winner_index == -1 and len(losers) < players_number - winners_number:
        answer_data = base_push(players, final_push_value(set_number), final_answer_probability(set_number))
        lamp_index = answer_data[0]
        correct = answer_data[1]
        if lamp_index == -1:
            print('スルー')
            continue
        if correct:
            players[lamp_index].point += 1
            print(players[lamp_index].name + '○')
            players[lamp_index].result_str += '○'
            if players[lamp_index].point == 7:
                players[lamp_index].win = True
                winner_index = lamp_index
        else:
            players[lamp_index].miss += 1
            print(players[lamp_index].name + '×')
            players[lamp_index].result_str += 'x'
            if players[lamp_index].miss == set_number:
                losers.append(players[lamp_index])
                players[lamp_index].lose = True
    if winner_index == -1:
        for i, player in enumerate(players):
            if player.win == False and player.lose == False:
                winner_index = i
                player.win = True
    print([player.name + ' ' + player.result_str for player in players])
    players[winner_index].final_sets += 1
    return winner_index, players

def final_set_string(sets):
    if sets == 0:
        return '0Set'
    elif sets == 1:
        return '1Set'
    else:
        return str(sets) + 'Sets'
