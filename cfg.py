#!/usr/bin/env python

import os
import random
import sys
import time
random.seed(time.time())
import parse

def main():
    key = "A"
    note_grammars = {
        "u": ["I V V V I I IV u u", "I IV u u", "I VII IV u u"  , "e"],
        "e": [""],
    }
    chord_grammars = {
        "u": ['"I" "IV" "V" "IV" "I" u u', '"I" "VII" "IV" u u', '"I" "V" "IV" u u', "e"],
        "e": [""]
    }
    compose_piece(key, note_grammars)
    compose_piece(key, chord_grammars, chords=True)

def compose_piece(key, grammars, chords=False):
    score = ""
    while len(score.split()) < 10:
        score = "u u u"
        score = generate_score(score, grammars)
    score = parse.parse(score)
    score = transliterate_score(score, key, chords)
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


def generate_score(score, grammars):
    while 1:
        found_substitution = False
        for key,value in grammars.iteritems():
            if score.find(key) != -1:
                found_substitution = True
                while score.find(key) != -1:
                    score = score.replace(key, random.choice(grammars[key]), 1)
                    if len(score) > 200:
                        score = score.replace("u", "")
                        score = score.replace("e", "")
                        return score
        if found_substitution is False:
            break
    return score

def transliterate_score(score, key, chords=False):
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
    if chords is False:
        for i in range(len(score)):
            score[i].value = scale[scale_conversion[score[i].value]-1]
    else:
        for i in range(len(score)):
            chord = []
            root_note_index = scale.index(key) + scale_conversion[score[i].value]
            chord.append(scale[root_note_index])
            chord.append(scale[(root_note_index+3) % 8])
            chord.append(scale[(root_note_index+5) % 8])
            score[i].chord = chord
    return score


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
        if isinstance(token, parse.Chord):  # Chords
            for note in token.chord: 
                note = csound_note_values[note]
                csound_score.append("i2 %(time)f 1 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6" % {"time": t, "octave": random.choice([7,8]), "note": note})
            t += 1
        else:  # Individual notes
            note = csound_note_values[token.value]
            csound_score.append("i2 %(time)f 1 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6" % {"time": t, "octave": random.choice([8,9]), "note": note})
            t += .25
    return csound_score


if __name__ == "__main__": main() 
