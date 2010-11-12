#!/usr/bin/env python

import os
import random
import sys
import time
random.seed(time.time())

grammars = {
    "u": ["I V I IV u", "I IV", "I VII IV"  , "e"],
    "e": [""],
}


def main():
    score = "u u u"
    key = "G#"
    score = generate_score(score)
    score = keyify_score(score, key)
    score = generate_csound_score(score)
    print "f1  0   256 10  1 0 3   ; sine wave function table"
    for line in score:
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


def generate_score(score):
    while 1:
        found_substitution = False
        for key,value in grammars.iteritems():
            if score.find(key) != -1:
                found_substitution = True
                while score.find(key) != -1:
                    score = score.replace(key, random.choice(grammars[key]), 1)
        if found_substitution is False:
            break
    return score

def keyify_score(score, key):
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
    for token in score.split():
        keyed_score.append(scale[scale_conversion[token]-1])
    return keyed_score


def generate_csound_score(score):
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
    t = 0 
    csound_score = []
    for token in score:
        note = csound_note_values[token]
        csound_score.append("i2 %f 2 7000 %d.%s %d.%s 0 6" % (t, random.choice([8,9]), note, random.choice([8,9]), note))
        t += .25
    return csound_score


if __name__ == "__main__": main() 
