#!/usr/bin/env python3
from .vbc_class import third_round_course
from .vbc_ox import third_round_ox
from .vbc_swedish import third_round_swedish
from .vbc_by import third_round_by
from .vbc_updown import third_round_updown

def third_round(course, members):
    winners = []
    players_3R = []
    if (course == third_round_course.ox):
        winners, players_3R = third_round_ox(members)
    elif (course == third_round_course.swedish):
        winners, players_3R = third_round_swedish(members)
    elif (course == third_round_course.by):
        winners, players_3R = third_round_by(members)
    else:
        winners, players_3R = third_round_updown(members)
    return winners, players_3R