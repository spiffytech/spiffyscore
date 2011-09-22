#!/usr/bin/env python

from __future__ import division
import os
import pdb
import random
import sys
import time
import parse

import tree

random.seed(time.time())

def main():
    composition = {
        "verse1": {
            "melody": {  # Instrument 'melody'
                "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 2",
                "octave": 8,
                "duration": 10,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ["C G/2 G/2 G/2 C B, F' C F C B F (w)"],
                    "w": ["E/4 A/4 D/4 G/4 F/4 F/4 B2 (u)"],
                },
            },
        },
        "verse2": {
            "melody": {  # Instrument 'melody'
                "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 2",
                "octave": 8,
                "duration": 10,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ["C C C C F/2 F/2 F/2 (u)", "D D G/2 A/2 D D (u)"],
                },
            },
            "harmony": {  # Instrument 'melody'
                "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 2",
                "octave": 8,
                "duration": 10,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ["C C C C F/2 F/2 F/2 (u)", "D D G/2 A/2 D D (u)"],
                },
            },
        },
    }
    print '''f1 0 512 10 1
f2 0 8192 10 .24 .64 .88 .76 .06 .5 .34 .08
f3 0 1025 10 1
t 0 60
    '''

    start = 0
    for section in ["verse1", "verse2"]:
        section = composition[section]
#        for subsection in section
        instrs = []
        for instr in section.values():
            sync = None
            max_time = instr["duration"]
            instr_score = render_instr(instr, sync, max_time)
            instrs.append(instr_score)
            for line in generate_csound_score(instr_score, instr["score_line"], start):
                print line
        longest_score = max(instrs, key=lambda i: score_len(i))
        start = score_len(longest_score)
        


def render_instr(instr, sync, max_time):
    grammars = instr["grammars"]
    for g in instr["grammars"]:
        for i in range(len(grammars[g])):
            grammars[g][i] = parse.parse(grammars[g][i])
    init_node = random.choice(instr["grammars"].keys())
    init_score = random.choice(instr["grammars"][init_node])
    score = init_score
    while True:
        time_remaining = max_time - score_len(score)
        try:
            score = choose_node(score, grammars, time_remaining)
        except ValueError:
            break
    return score


def choose_node(score, grammars, time_remaining):
    if time_remaining <= 0:
        raise ValueError("No time remaining in the score")
    node = None
    node_index = None
    for item in range(len(score)):
        if isinstance(score[item], tree.Tree):
            node = score[item].name
            node_index = item
    if node is None:
        raise ValueError("No more nodes to fill in")
    options = []
    for g in range(len(grammars[node])):
        if score_len(grammars[node][g]) <= time_remaining:
            options.append(grammars[node][g])
    if len(options) == 0:
        raise ValueError("No available grammars that will fit in the score")
    phrase = random.choice(options)
    score = score[:node_index-1] + phrase + score[node_index+1:]
    return score

            
            



#    movement_start = 0
#    progression = "verse1 verse2"
#    for comp_name in progression.split():
#        # We need an arbitrary grammar from this instrument to start the score with
#        max_instr =  0
#        for instr_name, instr in composition[comp_name].iteritems():
#            for grammar in instr["grammars"]:
#                for g in range(len(instr["grammars"][grammar])):
#                    instr["grammars"][grammar][g] = parse.parse(instr["grammars"][grammar][g], default_octave=instr["octave"])
#            g = random.choice(instr["grammars"].keys())
#            ins_score = random.choice(instr["grammars"][g])
##            ins_score = instr["grammars"][g]
#            score_complete = False
#            while score_complete is False:
#                if score_len(ins_score) >= instr["duration"]:
#                    score_complete = True
#                    break
#                for i in range(len(ins_score)):
#                    if isinstance(ins_score[i], tree.Tree):
#                        unrolled_score = select_node(instr["grammars"][ins_score[i].name])
#                        new_score = ins_score[:i-1] + unrolled_score + ins_score[i+1:]
#                        ins_score = new_score
#                    if i == len(ins_score):
#                        score_complete = True
#                        break
#            
#
#            ins_score = [n for n in ins_score if not isinstance(n, tree.Tree)]
#            composition[comp_name][instr_name]["score"] = ins_score
#
#            if score_len(ins_score) > max_instr:
#                max_instr = score_len(ins_score)
#            for line in generate_csound_score(composition[comp_name][instr_name]["score"], instr["score_line"], movement_start):
#                print line
#
#        movement_start += max_instr


def score_len(score):
    total = 0
    for n in score:
        if not isinstance(n, tree.Tree):
            total += n.duration
    return total

def select_node(grammar):
    return random.choice(grammar)
            

def generate_score(score, grammars):
    while 1:
        found_substitution = False
        for key,value in grammars.iteritems():
            if score.find(key) != -1:
                found_substitution = True
                while score.find(key) != -1:
                    score = score.replace(key, random.choice(grammars[key]), 1)
#                    print scoe
                    if len(score.split()) > 2000:
                        for k in grammars.keys():
                            score = score.replace(k, "")
                        return score
        if found_substitution is False:
            break
    return score


def generate_csound_score(score, score_line, t):
    csound_note_values = {
        "C": "00",
        "C#": "01",
        "D": "02",
        "D#": "03",
        "E": "04",
        "F": "05",
        "F#": "06",
        "G": "07",
        "G#": "08",
        "A": "09",
        "A#": "10",
        "B": "11",
    }
    csound_score = []
    for token in score:
        if isinstance(token, parse.Chord):  # Chords
            for note in token.chord: 
                note = csound_note_values[note]
                csound_score.append(score_line % {"time": t, "octave": token.octave, "note": note, "duration": token.duration})
        elif isinstance(token, parse.Note):  # Individual notes
            note = csound_note_values[token.value]
            csound_score.append(score_line % {"time": t, "octave": token.octave, "note": note, "duration": token.duration})
        elif isinstance(token, tree.Tree):
            continue
        t += token.duration
    return csound_score


if __name__ == "__main__": main() 
