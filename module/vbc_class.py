#!/usr/bin/env python3
from enum import IntEnum
from .vbc_base import rank_str

class Player:
    def __init__(self, rank, name, knowledge, speed, third_round_course):
        self.rank = rank
        self.name = name
        self.knowledge = knowledge
        self.speed = speed
        self.win = False
        self.lose = False
        self.point = 0
        self.miss = 0
        self.win_rank = -1
        self.third_round_course = third_round_course
        self.result_str = ''
        self.semifinal_seat = 0
        self.semifinal_point = 0
        self.final_sets = 0
        self.score_str = ''
        self.history_str = rank_str(rank)

class third_round_course(IntEnum):
    ox = 1
    swedish = 2
    by = 3
    updown = 4

def get_course_str(course):
    if course == third_round_course.ox:
        return '10o10x'
    if course == third_round_course.updown:
        return '10 up-down'
    if course == third_round_course.swedish:
        return 'Swedish 10'
    if course == third_round_course.by:
        return '10 by 10'

class Third_round_course_for_sort:
    def __init__(self, course, priority):
        self.course = course
        self.priority = priority
