#!/usr/bin/env python

from __future__ import division
import os
import random
import sys
import time
random.seed(time.time())

import parse
import topsort
import yaml

def main():
    key = "A"
    bps = 60/60
    tempo = 1/bps
    max_duration = 1

    composition = yaml.load(open("score.yaml"))

    max_t = 0  # max time encountered so far. Used for movement timing
    progression = "chorus"

    for movement in progression.split():
        for section in ["intro", "core", "outro"]:
            if section in composition[movement].keys():
                try:
                    render_order = topsort.topsort([[composition[movement][section][instrument]["sync"], instrument] if "sync" in composition[movement][section][instrument].keys() else [None, instrument] for instrument in composition[movement][section]])
                except topsort.CycleError as ex:
                    print "Your instruments are synced in a circle! This makes no sense!"
                    print movement, section
                    print ex
                    sys.exit(1)
                

#    for comp_name in progression.split():
#        comp_start_time = max_t
#        for instr_name, instr in composition[comp_name].iteritems():
#            generated_score = generate_score(instr["score"], instr["grammars"])  # Fill in the scores by generating them based on the grammars
##            print generated_score
#            score = parse.parse(generated_score, default_octave=instr["octave"])  # Return Node/Chord objects
#
#            # Generate timestamps for the notes 
#            t = comp_start_time
#            for note in range(len(score)):
#                score[note].time = t
#                score[note].duration *= tempo
#                t += score[note].duration
##                print "time difference =", t-comp_start_time
##                print "instrument duration =",composition[comp_name][instr_name]["duration"]
#                if (t-comp_start_time) > float(composition[comp_name][instr_name]["duration"]):
##                    print "here"
#                    score = score[:note]
#                    break
#                max_t = t if t > max_t else max_t
#            composition[comp_name][instr_name]["score"] = score

    # Must be done after all note times keyed in, else you can't coordinate melodies with the rhythm chords
    print '''f1  0  512  10  1
            f2 0 8192 10 .24 .64 .88 .76 .06 .5 .34 .08
            f3 0 1025 10 1
    '''
    for comp_name in progression.split():
        print "; Movement:", comp_name
        for instr_name, instr in composition[comp_name].iteritems():
            composition[comp_name][instr_name]["score"] = transliterate_score(composition[comp_name][instr_name]["score"], key)
#            print "\nMovement %s instrument %s" % (comp_name, instr_name)
#            print composition[comp_name][instr_name]["score"] 
            final_score = generate_csound_score(composition[comp_name][instr_name]["score"], composition[comp_name][instr_name]["score_line"])
            for line in final_score:
                print line
            

def make_scale(key):
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    scale = [key]
    pos = notes.index(key)
    progression = [2,2,1,2,2,2,1]
    for p in progression:
        pos = (pos + p) % 12
        scale.append(notes[pos])
    return scale


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

def transliterate_score(score, key):
    scale = make_scale(key)
    scale_conversion = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4,
        "V": 5,
        "VI": 6,
        "VII": 7,
        "VIII": 8,
    }
    keyed_score = []
    for i in range(len(score)):
        if isinstance(score[i], parse.Note):
            score[i].value = scale[scale_conversion[score[i].value]-1]
        elif isinstance(score[i], parse.Chord):
            chord = []
            root_note_index = scale.index(key) + scale_conversion[score[i].value]
            chord.append(scale[root_note_index])
            chord.append(scale[(root_note_index+3) % 8])
            if score[i].chord_type == "m":  # Minor chords, flat the 5th
                chord.append(scale[(root_note_index+4) % 8])
            else:
                chord.append(scale[(root_note_index+5) % 8])
            score[i].chord = chord
        elif isinstance(score[i], parse.Rest):
            pass
    return score


def generate_csound_score(score, score_line):
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
                csound_score.append(score_line % {"time": token.time, "octave": token.octave, "note": note, "duration": token.duration})
        elif isinstance(token, parse.Note):  # Individual notes
            note = csound_note_values[token.value]
            csound_score.append(score_line % {"time": token.time, "octave": token.octave, "note": note, "duration": token.duration})
    return csound_score


if __name__ == "__main__": main() 
