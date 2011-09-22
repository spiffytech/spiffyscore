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
            "intro": {
                "melody": {  # Instrument 'melody'
                    "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 2",
                    "octave": 8,
                    "duration": 10,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["G/2 G/2 G/4 G/4 A/4 A/4 A/2 G G A A A3 (w)"],
                        "w": ["E E F F G/2 G/2 G3 (u)"],
                    },
                },
            },
            "body": {
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
        },
        "verse2": {
            "body": {
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
        },
    }
    print '''f1 0 512 10 1
f2 0 8192 10 .24 .64 .88 .76 .06 .5 .34 .08
f3 0 1025 10 1
t 0 100
    '''

    section_start = 0
    for section in ["verse1", "verse2"]:
        print "; Section " + section
        subsection_start = section_start
        section = composition[section]
        for subsection in ["intro", "body", "outro"]:
            try:
                print "; Subsection " + subsection
                subsection = section[subsection]
                instrs = []
                for instr in subsection:
                    print ";Instrument " + instr
                    instr = subsection[instr]
                    sync = None
                    max_time = instr["duration"]
                    instr_score = render_instr(instr, sync, max_time)
                    instrs.append(instr_score)
                    for line in generate_csound_score(instr_score, instr["score_line"], subsection_start):
                        print line
                longest_score = max(instrs, key=lambda i: score_len(i))
                subsection_start += score_len(longest_score)
                section_start += score_len(longest_score)
            except KeyError:
                pass
        


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
            score = choose_node(score, grammars, time_remaining, sync)
        except ValueError:
            break
    return score


def choose_node(score, grammars, time_remaining, sync):
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
    if sync:
        pass
    else:
        phrase = random.choice(options)
    score = score[:node_index-1] + phrase + score[node_index+1:]
    return score


def score_len(score):
    total = 0
    for n in score:
        if not isinstance(n, tree.Tree):
            total += n.duration
    return total


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
