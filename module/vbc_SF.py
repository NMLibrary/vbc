#!/usr/bin/env python3
import random
from .vbc_class import Player
from .vbc_base import compare_value, base_push, base_push_index
from functools import cmp_to_key

def semifinal_seat_assign(semifinal_player):
    semifinal_player = sorted(semifinal_player, key = cmp_to_key(compare_player_seat))
    return semifinal_player

def compare_player_seat(player_a, player_b):
    return compare_value(player_a.semifinal_seat, player_b.semifinal_seat)

def semifinal_question_time():
    return random.uniform(7.5 - 4, 7.5 + 4)

def semifinal_compare_player(player_a, player_b):
    return compare_value(player_b.semifinal_point, player_a.semifinal_point) or compare_value(random.random(), random.random())

def semifinal_rank_sort(members):
    return sorted(members, key = cmp_to_key(semifinal_compare_player))

def semifinal_set1(players):
    for i, player in enumerate(players):
        player.point = 0
        player.miss = 0
        player.win = False
        player.lose = False
        player.result_str = ''
    time = 0
    while time < 5 * 60:
        answer_data = base_push(players)
        lamp_index = answer_data[0]
        correct = answer_data[1]
        time += semifinal_question_time()
        if lamp_index == -1:
            print('スルー')
            continue
        if correct:
            players[lamp_index].semifinal_point += 1
            players[lamp_index].point += 1
            print(players[lamp_index].name + '○')
            players[lamp_index].result_str += '○'
        else:
            players[lamp_index].semifinal_point -= 1
            players[lamp_index].miss += 1
            print(players[lamp_index].name + '×')
            players[lamp_index].result_str += 'x'
    remain_players = []
    losers = []
    players_sorted = semifinal_rank_sort(players)
    winner = players_sorted[0]
    players_sorted[0].win = True
    player_number = len(players)
    for i in range(player_number):
        if i > 0 and i <= 6:
            remain_players.append(players_sorted[i])
        if i > 6:
            losers.append(players_sorted[i])
    for player in players:
        player.score_str = str(player.semifinal_point) + 'p'
    for loser in losers:
        loser.lose = True
    print([player.name + ' ' + str(player.point) + '○ ' + str(player.miss) + '× ' + player.score_str for player in players])
    return winner, semifinal_seat_assign(remain_players), semifinal_seat_assign(losers), players

def semifinal_set2(players):
    for i, player in enumerate(players):
        player.win = False
        player.lose = False
        player.point = 0
        player.miss = 0
        player.result_str = ''
    time = 0
    while time < 5 * 60:
        answer_data = base_push(players)
        lamp_index = answer_data[0]
        correct = answer_data[1]
        time += semifinal_question_time()
        if lamp_index == -1:
            print('スルー')
            continue
        if correct:
            players[lamp_index].semifinal_point += 1
            players[lamp_index].point += 1
            print(players[lamp_index].name + '○')
            players[lamp_index].result_str += '○'
        else:
            players[lamp_index].semifinal_point -= 2
            players[lamp_index].miss += 1
            print(players[lamp_index].name + '×')
            players[lamp_index].result_str += 'x'
    remain_players = []
    losers = []
    players_sorted = semifinal_rank_sort(players)
    winner = players_sorted[0]
    players_sorted[0].win = True
    player_number = len(players)
    for i in range(player_number):
        if i > 0 and i <= 3:
            remain_players.append(players_sorted[i])
        if i > 3:
            losers.append(players_sorted[i])
    for player in players:
        player.score_str = str(player.semifinal_point) + 'p'
    for loser in losers:
        loser.lose = True
    print([player.name + ' ' + str(player.point) + '○ ' + str(player.miss) + '× ' + player.score_str for player in players])
    return winner, semifinal_seat_assign(remain_players), semifinal_seat_assign(losers), players

def semifinal_set3(players):
    for i, player in enumerate(players):
        player.win = False
        player.lose = False
        player.point = 0
        player.miss = 0
        player.result_str = ''
    time = 0
    while time < 5 * 60:
        answer_data = base_push(players)
        lamp_index = answer_data[0]
        correct = answer_data[1]
        time += semifinal_question_time()
        if lamp_index == -1:
            print('スルー')
            continue
        if correct:
            players[lamp_index].semifinal_point += 2
            players[lamp_index].point += 1
            print(players[lamp_index].name + '○')
            players[lamp_index].result_str += '○'
        else:
            players[lamp_index].semifinal_point -= 2
            players[lamp_index].miss += 1
            print(players[lamp_index].name + '×')
            players[lamp_index].result_str += 'x'
    losers = []
    players_sorted = semifinal_rank_sort(players)
    winner = players_sorted[0]
    players_sorted[0].win = True
    player_number = len(players)
    for i in range(player_number):
        if i > 0:
            losers.append(players_sorted[i])
    for player in players:
        player.score_str = str(player.semifinal_point) + 'p'
    for loser in losers:
        loser.lose = True
    print([player.name + ' ' + str(player.point) + '○ ' + str(player.miss) + '× ' + player.score_str for player in players])
    return winner, semifinal_seat_assign(losers), players