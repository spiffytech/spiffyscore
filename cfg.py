#!/usr/bin/env python

import os
import random
import sys
import time
random.seed(time.time())
import parse

def main():
    key = "A"

    composition = {
        "a": {  # Movement block 'a' for reuse throughout the piece
            "melody": {  # Instrument 'melody'
                "csound_parameters": {
                    "instrument": 1,
                },
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ["I V V V I I IV u u", "I IV u u", "I VII IV u u"  , "e"],
#                    "u": ["I I I I u u", "e"],
                    "e": [""],
                },
                "score": "u u u u u",
            },
            "rhythm": {
                "csound_parameters": {
                    "instrument": 1,
                },
                "grammars": {
#                    "u": ['"I" "ii"/4 "ii"/4 "IV"/2 "V"2 "IV" "I" u u', '"I" "vii" "IV" u u', '"I" "v" "IV" u u', "e"],
                    "u": ['"i" "I" "ii" "II" "v" "V" u', "e"],
                    "e": [""]
                },
                "score": "u u u",
            },
        },
        "b": {
            "melody": {  # Instrument 'melody'
                "csound_parameters": {
                    "instrument": 1,
                },
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ["I V I I/2 IV/2 u u", "I2 IV u u", "I IV IV VI V u u" , "e"],
#                    "u": ["I IV I V u u u", "e"],
                    "e": [""],
                },
                "score": "u u u",
            },
            "rhythm": {
                "csound_parameters": {
                    "instrument": 1,
                },
                "grammars": {
                    "u": ['"I" "IV"/2 "V"2 "IV" "I" u u', '"I" "VII" "IV" u u', '"I" "V" "IV" u u', "e"],
                    "e": [""]
                },
                "score": "u u u",
            },
        },
    }

    max_t = 0  # max time encountered so far. Used for movement timing
    progression = "a b"
    for comp_name in progression.split():
        instr_start_time = max_t
        for instr_name, instr in composition[comp_name].iteritems():
            generated_score = generate_score(instr["score"], instr["grammars"])  # Fill in the scores by generating them based on the grammars
            score = parse.parse(generated_score)  # Return Node/Chord objects

            # Generate timestamps for the notes 
            t = instr_start_time
            for note in range(len(score)):
                score[note].time = t
                t += score[note].duration
                max_t = t if t > max_t else max_t
#                print "end note,", max_t
            composition[comp_name][instr_name]["score"] = score
#            print "end instr,", max_t

    # Must be done after all note times keyed in, else you can't coordinate melodies with the rhythm chords
    for comp_name in progression.split():
        for instr_name, instr in composition[comp_name].iteritems():
            composition[comp_name][instr_name]["score"] = transliterate_score(composition[comp_name][instr_name]["score"], key)
#            print "\nMovement %s instrument %s" % (comp_name, instr_name)
#            print composition[comp_name][instr_name]["score"] 
            print "f1  0   256 10  1 0 3   ; sine wave function table"
            final_score = generate_csound_score(composition[comp_name][instr_name]["score"])
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
                    if len(score.split()) > 20:
                        score = score.replace("u", "")
                        score = score.replace("e", "")
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
        else:
            chord = []
            root_note_index = scale.index(key) + scale_conversion[score[i].value]
            chord.append(scale[root_note_index])
            if score[i].chord_type == "m":  # Minor chords, flat the 3rd
                chord.append(scale[(root_note_index+2) % 8])
            else:
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
    csound_score = []
    for token in score:
        if isinstance(token, parse.Chord):  # Chords
            for note in token.chord: 
                note = csound_note_values[note]
                csound_score.append("i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6" % {"time": token.time, "octave": random.choice([7,8]), "note": note, "duration": token.duration})
        else:  # Individual notes
            note = csound_note_values[token.value]
            csound_score.append("i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6" % {"time": token.time, "octave": random.choice([8,9]), "note": note, "duration": token.duration})
    return csound_score


if __name__ == "__main__": main() 
