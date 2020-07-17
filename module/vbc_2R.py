#!/usr/bin/env python3
import random
from .vbc_class import Player
from .vbc_base import base_push, base_push_index, remain_rank_sort

def second_round(members):
    assert len(members) == 12, 'メンバーが12人になっていません'
    points = [3, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    misses = [0] * 12
    result_strs = ['●●●', '●●', '●●', '●', '●', '●', '', '', '', '', '', '']
    for i, player in enumerate(members):
        player.point = points[i]
        player.miss = misses[i]
        player.win = False
        player.lose = False
        player.result_str = result_strs[i]
    winners = []
    losers = []
    double_index = -1
    while len(winners) < 5 and len(losers) < 7:
        answer_data = base_push(members)
        lamp_index = answer_data[0]
        correct = answer_data[1]
        if lamp_index == -1:
            print('スルー')
            continue
        if correct:
            if lamp_index == double_index:
                members[lamp_index].point = min(5, members[lamp_index].point + 2)
                print(members[lamp_index].name + '◎')
                members[lamp_index].result_str += '◎◎'
            else:
                members[lamp_index].point += 1
                print(members[lamp_index].name + '○')
                members[lamp_index].result_str += '○'
            double_index = lamp_index
            if members[lamp_index].point == 5:
                winners.append(members[lamp_index])
                members[lamp_index].win = True
            # print('ok')
        else:
            members[lamp_index].miss += 1
            print(members[lamp_index].name + '×')
            members[lamp_index].result_str += 'x'
            if lamp_index == double_index:
                double_index = -1
            if members[lamp_index].miss == 2:
                losers.append(members[lamp_index])
                members[lamp_index].lose = True
            # print('ng')
        # print([player.point for player in members])
        # print([player.miss for player in members])
    if len(losers) == 7:
        remain_members = []
        for player in members:
            if player.point < 5 and player.miss < 2:
                remain_members.append(player)
        for player in remain_rank_sort(remain_members):
            winners.append(player)
    for winner in winners:
        winner.win = True
    # print([player.rank for player in winners])
    # print([player.rank for player in losers])
    print([player.name + ' ' + player.result_str for player in members])
    return winners, members