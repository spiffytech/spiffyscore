#!/usr/bin/env python

from __future__ import division
import os
import ipdb
import random
import sys
import time

import parse
import topsort
import yaml

import tree

random.seed(time.time())

def main():
    composition = {
        "fm_test": {
            "intro": {
                "melody": {  # Instrument 'melody'
                    "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 2 6 5 1",
                    "octave": 8,
                    "duration": 10,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["G/2 G/2 | G/4 G/4 A/4 A/4 | A/2 A/2 | G | G | A | A | A3 (w)"],
                        "w": ["E | E | F | F | G/2 G/2 | G3 (u)"],
                    },
                },
            },
        },
        "verse1": {
            "intro": {
                "melody": {  # Instrument 'melody'
                    "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 1",
                    "octave": 8,
                    "duration": 10,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["G/2 G/2 | G/4 G/4 A/4 A/4 | A/2 A/2 | G | G | A | A | A3 (w)"],
                        "w": ["E | E | F | F | G/2 G/2 | G3 (u)"],
                    },
                },
            },
            "body": {
                "melody": {  # Instrument 'melody'
                    "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 1",
                    "octave": 8,
                    "duration": 10,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C | G/2 G/2 | G/2 G/2 | C | B, | F' | C | F | C | B | F | (w)"],
                        "w": ["E/4 A/4 D/4 G/4 | F/4 F/4 B2 | (u)"],
                    },
                },
            },
            "outro": {
                "melody": {  # Instrument 'melody'
                    "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 1",
                    "octave": 8,
                    "duration": 10,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C/4 C/4 C/4 C/4 | z2"],
                    },
                },
            },
        },
        "verse2": {
            "body": {
                "melody": {  # Instrument 'melody'
                    "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 1",
                    "octave": 8,
                    "duration": 30,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C | C | C | C | F/2 F/2 | F/2 F/2 | (u)", "D | D | G/2 A/2 | D | D | (u)"],
                    },
                },
                "harmony": {  # Instrument 'melody'
                    "score_line": "i3 %(time)f %(duration)f 4000 %(octave)d.%(note)s 2 3 5 3",
                    "octave": 8,
                    "duration": 30,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C | C | z | C | C | z/2 F/4 F/2 F/2 | F/2 F/2 | z (u)", "D | D | G/2 A/2 | D | D | z (u)"],
                    },
                },
                "percussion": {  # Instrument 'melody'
                    "score_line": "i1 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6",
                    "octave": 8,
                    "duration": 30,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C/4 C/4 C/4 C/4 | F/2 F/2 | F/2 F/2 | (u)", "D/4 D/4 G/4 A/4 | D | D | (v)"],
                        "v": ["C | D | E | F | E | D | C | (u)",],
                    },
                },
            },
            "outro": {
                "percussion": {  # Instrument 'melody'
                    "score_line": "i1 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6",
                    "octave": 8,
                    "duration": 30,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C/4 C/4 C/4 C/4"],
                    },
                },
            },
        },
        "sync_test": {
            "body": {
                "lead_instr": {  # Instrument 'melody'
                    "score_line": "i1 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6",
                    "octave": 8,
                    "duration": 30,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["D/4 D/4 D/4 D/4"],
                        "v": ["C/4 C/4 C/4 C/4"],
                    },
                },
                "follow_instr": {  # Instrument 'melody'
                    "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 1",
                    "sync": "lead_instr",
                    "octave": 8,
                    "duration": 30,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["D/4 D/4 D/4 D/4"],
                        "v": ["C/4 C/4 C/4 C/4"],
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
#    for section in ["verse1", "verse2"]:
    for section in ["sync_test"]:
        print "; Section " + section
        subsection_start = section_start
        section = composition[section]
        for subsection in ["intro", "body", "outro"]:
            try:
                print "; Subsection " + subsection
                subsection = section[subsection]

                unordered_instrs = []
                for instr in subsection:
                    if not "sync" in subsection[instr].keys():
                        subsection[instr]["sync"] = None
                    unordered_instrs.append([subsection[instr]["sync"], instr])
                ordered_instrs = topsort.topsort(unordered_instrs)
                ordered_instrs.remove(None)  # None used as a placeholder for sort order for instruments with no sync setting

                instrs = []
                syncs = {}
                for instr in ordered_instrs:
                    print ";Instrument " + instr
                    instr = subsection[instr]
#                    ipdb.set_trace()
                    max_time = instr["duration"]
                    instr_score, syncs = render_instr(instr, syncs, max_time)
                    instrs.append(instr_score)
                    for line in generate_csound_score(instr_score, instr["score_line"], subsection_start):
                        print line
                longest_score = max(instrs, key=lambda i: score_len(i))
                subsection_start += score_len(longest_score)
                section_start += score_len(longest_score)
            except KeyError:
                pass


def render_instr(instr, syncs, max_time):
    for g in instr["grammars"]:
        for i in range(len(instr["grammars"][g])):
            instr["grammars"][g][i] = parse.parse(instr["grammars"][g][i])
    score = []
    while True:
#        ipdb.set_trace()
        time_remaining = max_time - score_len(score)
        try:
            score, syncs = choose_node(score, instr, time_remaining, syncs)
        except ValueError:
            break
    return (score, syncs)


def choose_node(score, instr, time_remaining, syncs):
#    ipdb.set_trace()
    grammars = instr["grammars"]
    if time_remaining <= 0:
        raise ValueError("No time remaining in the score")

    if len(score) == 0:
        options = get_node_choices(instr, syncs, score_len(score))
        node = random.choice(options)
        phrase = random.choice(instr["grammars"][node])

    # Find the next node in the score that needs choosing
    node = None
    node_index = None
    for item in range(len(score)):
        if isinstance(score[item], tree.Tree):
            node = score[item].name
            node_index = item
    if node is None:
        raise ValueError("No more nodes to fill in")

    options = get_node_choices(instr, syncs, score_len(score))
    node = random.choice(options)
    phrase = random.choice(instr["grammars"][node])
    score = score[:node_index-1] + phrase + score[node_index+1:]
    return score


def get_node_choices(instr, syncs, current_time):
    # If this instrument should follow another, choose a grammar node from the correct instrument
#    ipdb.set_trace()
    grammars = instr["grammars"]
    options = []
    if instr["sync"] is not None:
        guiding_instr = instr["sync"]
        sync_node = get_sync_node_at_time(syncs[guiding_instr], current_time)
        if sync_node in instr["grammars"].keys():
            options.append(sync_node)
        else:
            for g in range(len(grammars[node])):
                if score_len(grammars[node][g]) <= time_remaining:
                    options.append(grammars[node][g])
    else:
        for g in range(len(grammars[node])):
            if score_len(grammars[node][g]) <= time_remaining:
                options.append(grammars[node][g])
    if len(options) == 0:
        raise ValueError("No available grammars that will fit in the score")
    return options


def get_sync_node_at_time(syncs, t):
    for s in len(syncs):
        if syncs[s]["time"] > t:
            return syncs[s]["node"]


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
