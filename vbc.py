#!/usr/bin/env python3
# モジュールのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import csv, random
import sys, codecs

from module.vbc_class import Player, third_round_course, get_course_str, Third_round_course_for_sort
from module.vbc_base import course_sort, rank_str, winner_rank_str, win_or_lose_mark, paper_color, calculate_course_priority
from module.vbc_2R import second_round
from module.vbc_3R_assign import third_round_assign, third_round_priority
from module.vbc_3R import third_round
from module.vbc_ex import extra_round_first, extra_round_second, semifinal_assign
from module.vbc_SF import semifinal_seat_assign, semifinal_set1, semifinal_set2, semifinal_set3
from module.vbc_F import final_set, final_set_string

# ファイル選択ダイアログの表示
root = tkinter.Tk()
root.withdraw()
fTyp = [("","*")]
iDir = os.path.abspath(os.path.dirname(__file__))
# tkinter.messagebox.showinfo('vbc','処理ファイルを選択してください！')
file_path = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)

out_file = codecs.open('vbc_log.txt', 'w', 'utf_8')
sys.stdout = out_file

players = []
with open(file_path, encoding='utf-8_sig') as file:
    reader = csv.reader(file)
    data = [row for row in reader]
    for i in range(48):
        row = data[i]
        courses_for_sort = []
        for j in range(4):
            course = Third_round_course_for_sort(third_round_course(j + 1), calculate_course_priority(float(row[j + 4])))
            courses_for_sort.append(course)
        courses_for_sort = course_sort(courses_for_sort)
        course_order = [course.course for course in courses_for_sort]
        player = Player(i + 1, row[1], float(row[2]), float(row[3]), course_order)
        players.append(player)
    player_49 = Player(49, data[48][1], 0, 0, [1, 2, 3, 4])
    players.append(player_49)

# 処理ファイル名の出力
# tkinter.messagebox.showinfo('vbc',file)

# 2R組分け
second_round_players = []
for i in range(4):
    second_round_players.append([])
for i in range(48):
    second_round_players[i % 4].append(players[i])

print('2R')
for i in range(4):
    print(str(i + 1) + '組目 ', end="")
    print([player.name for player in second_round_players[i]])

# 2Rの実行
second_round_winners = []
for i in range(4):
    print('2R ' + str(i + 1) + '組目 ', end="")
    print([player.name for player in second_round_players[i]])
    winners, players_2R = second_round(second_round_players[i])
    second_round_winners.append(winners)
    for j, player in enumerate(winners):
        player.history_str += ' ' + winner_rank_str(j + 1)

# Excelへの書き込み
with codecs.open('vbc_log_for_excel.csv', 'w', 'utf_8') as f:
    writer = csv.writer(f)
    writer.writerow(['順位', '名前', '2R結果'])
    for i in range(4):
        for j in range(12):
            player = players[j * 4 + i]
            writer.writerow([player.rank, player.name, player.result_str, player.history_str, win_or_lose_mark(player)])
    writer.writerow([49, players[48].name])

print('2R勝ち抜け者')
for i in range(4):
    print(str(i + 1) + '組目 ', end="")
    print([player.name for player in second_round_winners[i]])

# 3R組分け
third_round_member = third_round_priority(second_round_winners)

print('3R 組分け優先順')
print([player.name for player in third_round_member])

course_order, third_round_players = third_round_assign(third_round_member)

print('3R 組分け')
for i in range(4):
    print(str(i + 1) + 'コース目 ' + get_course_str(course_order[i]))
    print([player.name for player in third_round_players[i]])

# 3Rの実行
third_round_winners = []
third_round_players_for_log = [None] * 20
course_str_for_excel = [None] * 4
for i in range(4):
    print('3R' + str(i + 1) + 'コース目 ' + get_course_str(course_order[i]))
    print([player.name for player in third_round_players[i]])
    winners, players_3R = third_round(course_order[i], third_round_players[i])
    third_round_winners.append(winners)
    for j, player in enumerate(winners):
        player.history_str += winner_rank_str(j + 1)
    for j in range(5):
        third_round_players_for_log[(int(course_order[i]) - 1) * 5 + j] = players_3R[j]
    course_str_for_excel[int(course_order[i]) - 1] = winner_rank_str(i + 1)

# Excelへの書き込み
with codecs.open('vbc_log_for_excel.csv', 'a', 'utf_8') as f:
    writer = csv.writer(f)
    for i in range(4):
        writer.writerow([course_str_for_excel[i] + get_course_str(third_round_course(i + 1))])
        for j in range(5):
            player = third_round_players_for_log[i * 5 + j]
            writer.writerow([i * 5 + j + 1, player.name, player.result_str, player.score_str, player.history_str, win_or_lose_mark(player), paper_color(player.rank)])

print('3R勝ち抜け者')
for i in range(4):
    print(str(i + 1) + '組目 ' + get_course_str(course_order[i]) + ' ', end="")
    print([player.name for player in third_round_winners[i]])

# Extra Roundの実行
print('Extra Round 1st Step')
semifinal_players = semifinal_assign(third_round_winners)
extra_round_first_remain_players = extra_round_first(players, semifinal_players)

if len(extra_round_first_remain_players) == 0:
    print('敗者復活なし')
elif len(extra_round_first_remain_players) == 1:
    revival_player = extra_round_first_remain_players[0]
    print('敗者復活: ' + revival_player.name)
    revival_player.semifinal_seat = 4
    semifinal_players.append(revival_player)
    players[revival_player.rank - 1].history_str = rank_str(revival_player.rank) + ' Rev. '
else:
    print('勝ち抜け者')
    print([player.name for player in extra_round_first_remain_players])

    print('2nd Step')
    revival_player = extra_round_second(extra_round_first_remain_players)
    print('敗者復活: ' + revival_player.name)
    revival_player.semifinal_seat = 4
    semifinal_players.append(revival_player)
    players[revival_player.rank - 1].history_str = rank_str(revival_player.rank) + ' Rev. '

# Semifinalの実行
semifinal_players = semifinal_seat_assign(semifinal_players)
final_players = []
print('準決勝 第1セット')
print([player.name for player in semifinal_players])
winner, remain_players, losers, sf1_players = semifinal_set1(semifinal_players)
final_players.append(winner)
players[winner.rank - 1].history_str += winner_rank_str(1)
print('1抜け ' + winner.name)
print('敗退 ', end="")
print([player.name for player in losers])

sf1_players_for_excel = [None] * 9
for player in sf1_players:
    sf1_players_for_excel[player.semifinal_seat] = player
# Excelへの書き込み
with codecs.open('vbc_log_for_excel.csv', 'a', 'utf_8') as f:
    writer = csv.writer(f)
    writer.writerow(['SF Set1'])
    for i in range(9):
        player = sf1_players_for_excel[i]
        if player != None:
            writer.writerow([i + 1, player.name, str(player.point) + '○', str(player.miss) + '×', player.score_str, win_or_lose_mark(player)])
        else:
            writer.writerow([i + 1, '', '', '', '', ''])

# SF第2セット
print('第2セット')
print([player.name for player in remain_players])
winner, remain_players, losers, sf2_players = semifinal_set2(remain_players)
final_players.append(winner)
players[winner.rank - 1].history_str += winner_rank_str(2)
print('2抜け ' + winner.name)
print('敗退 ', end="")
print([player.name for player in losers])

sf2_players_for_excel = [None] * 9
for player in sf2_players:
    sf2_players_for_excel[player.semifinal_seat] = player
# Excelへの書き込み
with codecs.open('vbc_log_for_excel.csv', 'a', 'utf_8') as f:
    writer = csv.writer(f)
    writer.writerow(['SF Set2'])
    for i in range(9):
        player = sf2_players_for_excel[i]
        if player != None:
            writer.writerow([i + 1, player.name, str(player.point) + '○', str(player.miss) + '×', player.score_str, win_or_lose_mark(player)])
        else:
            writer.writerow([i + 1, '', '', '', '', ''])

# SF第3セット
print('第3セット')
print([player.name for player in remain_players])
winner, losers, sf3_players = semifinal_set3(remain_players)
final_players.append(winner)
players[winner.rank - 1].history_str += winner_rank_str(3)
print('3抜け ' + winner.name)
print('敗退 ', end="")
print([player.name for player in losers])

sf3_players_for_excel = [None] * 9
for player in sf3_players:
    sf3_players_for_excel[player.semifinal_seat] = player
# Excelへの書き込み
with codecs.open('vbc_log_for_excel.csv', 'a', 'utf_8') as f:
    writer = csv.writer(f)
    writer.writerow(['SF Set3'])
    for i in range(9):
        player = sf3_players_for_excel[i]
        if player != None:
            writer.writerow([i + 1, player.name, str(player.point) + '○', str(player.miss) + '×', player.score_str, win_or_lose_mark(player)])
        else:
            writer.writerow([i + 1, '', '', '', '', ''])
    writer.writerow(['SF 結果'])
    for i in range(9):
        player = sf1_players_for_excel[i]
        if player != None:
            writer.writerow([i + 1, player.history_str, win_or_lose_mark(player), paper_color(player.rank)])
        else:
            writer.writerow([i + 1, '', '', ''])

final_results_for_excel = []
final_results_color_for_excel = []
for i in range(3):
    final_results_for_excel.append([''] * 9)
    final_results_for_excel[i][0] = str(i + 1)
    final_results_for_excel[i][1] = final_players[i].name
    final_results_color_for_excel.append([''] * 8)
    final_results_color_for_excel[i][0] = str(i + 1)
# Finalの実行
print('決勝')
print([player.name for player in final_players])
for i in range(7):
    print('Set' + str(i + 1))
    winner_index, final_players = final_set(final_players, i + 1)
    winner = final_players[winner_index]
    print(winner.name + ' ' + final_set_string(winner.final_sets))
    for j, player in enumerate(final_players):
        final_results_for_excel[j][i + 2] = player.result_str
        final_results_color_for_excel[j][i + 1] = win_or_lose_mark(player)
    if winner.final_sets == 3:
        print([player.name + ' ' + final_set_string(player.final_sets) for player in final_players])
        print('優勝: ' + winner.name)
        players[winner.rank - 1].history_str += winner_rank_str(1)
        break

# Excelへの書き込み
with codecs.open('vbc_log_for_excel.csv', 'a', 'utf_8') as f:
    writer = csv.writer(f)
    writer.writerow(['Final'])
    for i in range(3):
        final_results_for_excel[i].append(players[final_players[i].rank - 1].history_str)
        final_results_for_excel[i].append(str(win_or_lose_mark(final_players[i])))
        final_results_for_excel[i].append(paper_color(final_players[i].rank))
        writer.writerow(final_results_for_excel[i])
    for i in range(3):
        writer.writerow(final_results_color_for_excel[i])