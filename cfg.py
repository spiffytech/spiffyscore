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
    key = "A"
    bps = 60/60
    tempo = 1/bps
    max_duration = 1

    composition = {
        "overview": {
            "melody": {  # Instrument 'melody'
                "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 2",
                "octave": 8,
                "duration": 40,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ["C G/2 G/2 G/2 C B, F' C F C B F (u)"],
#                    "w": ['E/4 A/4 D/4 G/4 F/4 F/4 B2'],
                },
                "score": "u u",
            },
        },
    }
    print '''f1  0  512  10  1
            f2 0 8192 10 .24 .64 .88 .76 .06 .5 .34 .08
            f3 0 1025 10 1
    '''
    movement_start = 0


    max_t = 0  # max time encountered so far. Used for movement timing
    progression = "overview"
    for comp_name in progression.split():
        comp_start_time = max_t
        # We need an arbitrary grammar from this instrument to start the score with
        max_instr =  0
        movement_start += max_instr
        for instr_name, instr in composition[comp_name].iteritems():
            for grammar in instr["grammars"]:
                for g in range(len(instr["grammars"][grammar])):
                    instr["grammars"][grammar][g] = parse.parse(instr["grammars"][grammar][g], default_octave=instr["octave"])
            g = random.choice(instr["grammars"].keys())
            ins_score = random.choice(instr["grammars"][g])
#            ins_score = instr["grammars"][g]
            score_complete = False
            while score_complete is False:
                if score_len(ins_score) >= 50:
                    score_complete = True
                    break
                for i in range(len(ins_score)):
                    if isinstance(ins_score[i], tree.Tree):
                        unrolled_score = select_node(instr["grammars"][ins_score[i].name])
                        new_score = ins_score[:i-1] + unrolled_score + ins_score[i+i:]
                        ins_score = new_score
                    if i == len(ins_score):
                        score_complete = True
                        break
            

            ins_score = [n for n in ins_score if not isinstance(n, tree.Tree)]
            composition[comp_name][instr_name]["score"] = ins_score

            # Generate timestamps for the notes 
#            t = comp_start_time
#            for note in range(len(ins_score)):
#                ins_score[note].time = t
#                ins_score[note].duration *= tempo
#                t += score[note].duration
##                print "time difference =", t-comp_start_time
##                print "instrument duration =",composition[comp_name][instr_name]["duration"]
#                if (t-comp_start_time) > float(composition[comp_name][instr_name]["duration"]):
##                    print "here"
#                    ins_score = ins_score[:note]
#                    break
#                max_t = t if t > max_t else max_t
#            composition[comp_name][instr_name]["score"] = ins_score

    # Must be done after all note times keyed in, else you can't coordinate melodies with the rhythm chords
#    for comp_name in progression.split():
#        print "; Movement:", comp_name
#        for instr_name, instr in composition[comp_name].iteritems():
##            print "\nMovement %s instrument %s" % (comp_name, instr_name)
##            print composition[comp_name][instr_name]["score"] 
#            final_score = generate_csound_score(composition[comp_name][instr_name]["score"], composition[comp_name][instr_name]["score_line"])
#            for line in final_score:
#                print line

            if score_len(ins_score) > max_instr:
                max_instr = ins_score
            for line in generate_csound_score(composition[comp_name][instr_name]["score"], instr["score_line"], movement_start):
                print line


def score_len(score):
    total = 0
    for n in score:
        if not isinstance(n, tree.Tree):
            total += n.duration
    return total

def select_node(grammar):
    return random.choice(grammar)
            

def generate_score(score, grammars):
    pdb.set_trace()
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
    pdb.set_trace()
    for token in score:
        if isinstance(token, parse.Chord):  # Chords
            for note in token.chord: 
                note = csound_note_values[note]
                csound_score.append(score_line % {"time": t, "octave": token.octave, "note": note, "duration": token.duration})
        elif isinstance(token, parse.Note):  # Individual notes
            note = csound_note_values[token.value]
            csound_score.append(score_line % {"time": t, "octave": token.octave, "note": note, "duration": token.duration})
        t += token.duration
    return csound_score


if __name__ == "__main__": main() 
