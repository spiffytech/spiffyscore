#!/usr/bin/env python

from __future__ import division
import os
import random
import sys
import time
random.seed(time.time())
import parse

def main():
    key = "A"
    bps = 60/60
    tempo = 1/bps
    max_duration = 1

    composition = {
        "intro1": {
            "rhythm": {
                "score_line": "i1 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6",
                "octave": 7,
                "duration": 4,
                "grammars": {
                    "u": ['"I" "ii"/4 "ii"/4 "IV"/2 "V"2 "IV" "ii" x u', '"I" "vii" "III" y u', '"I" "v" "IV" u u'],
                    "w": ['"i" "VII"2 "VI"/4 "V"/4 "i"/4 "VII"2 "VI" "V" w u'],
                    "x": ['"III/2" "VI"/2 "III"/2 "vii"2 "i"2 "V" u'],
                    "y": ['"I" "vi"2 "IV" "V" y y u'],
                },
                "score": "u x u y x w u",
            },
        },
        "intro2": {
            "rhythm": {
                "score_line": "i1 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6",
                "octave": 7,
                "duration": 8,
                "grammars": {
                    "u": ['"I" "ii"/4 "ii"/4 "IV"/2 "V"2 "IV" "ii" x u', '"I" "vii" "III" y u', '"I" "v" "IV" u u'],
                    "w": ['"i" "VII"2 "VI"/4 "V"/4 "i"/4 "VII"2 "VI" "V" w u'],
                    "x": ['"III/2" "VI"/2 "III"/2 "vii"2 "i"2 "V" u'],
                    "y": ['"I" "vi"2 "IV" "V" y y u'],
                },
                "score": "u x u y x w u",
            },
            "timbre": {
                "score_line": "i3 %(time)f %(duration)f 2000 %(octave)d.%(note)s 2 3 5 3",
                "octave": 6,
                "duration": 8,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ['I2 VII2 V2 VI2 I2 IV/2 V/2 III2 u', 'I2 IV2 V2 IV I V2 III2 II2 u']
                },
                "score": "u u u u u",
            },
        },
        "overview": {
            "melody": {  # Instrument 'melody'
                "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 2",
                "octave": 8,
                "duration": 40,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ["I V/2 V/2 V/2 I VII, IV' I IV I VII IV"],
                    "w": ['III/4 VI/4 II/4 V/4 VI/4 IV/4 VII2'],
                    "x": ['I/2 I/2 VI IV/2 V2 z I/2 I/2 VI IV/2 V'],
                },
                "score": "u u w w w w w x x",
            },
            "rhythm": {
                "score_line": "i1 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6",
                "octave": 7,
                "duration": 44,
                "grammars": {
                    "u": ['"I" "ii"/4 "ii"/4 "IV"/2 "V"2 "IV" "ii" x u', '"I" "vii" "III" y u', '"I" "v" "IV" u u'],
                    "w": ['"i" "VII"2 "VI"/4 "V"/4 "i"/4 "VII"2 "VI" "V" w u'],
                    "x": ['"III/2" "VI"/2 "III"/2 "vii"2 "i"2 "V" u'],
                    "y": ['"I" "vi"2 "IV" "V" y y u'],
                },
                "score": "u x u y x w u",
            },
            "timbre": {
                "score_line": "i3 %(time)f %(duration)f 2000 %(octave)d.%(note)s 2 3 5 3",
                "octave": 6,
                "duration": 44,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ['I2 VII2 V2 VI2 I2 IV/2 V/2 III2 u', 'I2 IV2 V2 IV I V2 III2 II2 u']
                },
                "score": "u u u u u",
            },
        },
        "a": {  # Movement block 'a' for reuse throughout the piece
            "melody": {  # Instrument 'melody'
                "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 2",
                "octave": 8,
                "duration": 40,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ["I V/2 V/2 V/2 I VII, IV' x", "I IV w", "I VII IV u"],
                    "w": ['VII I IV V VI VII I IV V VI VII u'],
                    "x": ['VI/4 III/4 II/4 I/4 w'],
                },
                "score": "u",
            },
            "rhythm": {
                "score_line": "i1 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6",
                "octave": 7,
                "duration": 48,
                "grammars": {
                    "u": ['"I" "ii"/4 "ii"/4 "IV"/2 "V"2 "IV" "ii" x u', '"I" "vii" "III" y u', '"I" "v" "IV" u u'],
                    "w": ['"i" "VII"2 "VI"/4 "V"/4 "i"/4 "VII"2 "VI" "V" w u'],
                    "x": ['"III/2" "VI"/2 "III"/2 "vii"2 "i"2 "V" u'],
                    "y": ['"I" "vi"2 "IV" "V" y y u'],
                },
                "score": "u x u y x w u",
            },
            "timbre": {
                "score_line": "i3 %(time)f %(duration)f 2000 %(octave)d.%(note)s 2 3 5 3",
                "octave": 6,
                "duration": 42,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ['I2 VII2 V2 VI2 I2 IV/2 V/2 III2 u', 'I2 IV2 V2 IV I V2 III2 II2 u']
                },
                "score": "u u u u u",
            },
        },
        "b": {  # Movement block 'a' for reuse throughout the piece
            "melody": {  # Instrument 'melody'
                "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 2",
                "octave": 8,
                "duration": 40,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ['I VII V III u', "y"],
                    "w": ['VII I IV V VI u', 'w'],
                    "x": ['VI/4 III/4 II/4 I/4 w', 'x x'],
                    "y": ["III/4 VI/4 II/4 V/4 VI/4 IV/4 VII2"],
                },
                "score": "w w x x w",
            },
            "rhythm": {
                "score_line": "i1 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6",
                "octave": 7,
                "duration": 44,
                "grammars": {
                    "u": ['"I" "V" "vi" "iii" "IV" "I" "IV" "V" u u', "y"],
                    "y": ['"I" "vi"2 "IV" "V" y y u'],
                },
                "score": "u u y y u",
            },
            "timbre": {
                "score_line": "i3 %(time)f %(duration)f 2000 %(octave)d.%(note)s 2 3 5 3",
                "octave": 6,
                "duration": 40,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ['I2 VII2 V2 VI2 I2 IV/2 V/2 III2 u', 'I2 IV2 V2 IV I V2 III2 II2 u']
                },
                "score": "u u u u u",
            },
        },
        "zelda1": {  # Movement block 'a' for reuse throughout the piece
            "melody": {  # Instrument 'melody'
                "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 2",
                "octave": 8,
                "duration": 50,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ['I VI/2 VI/2 IV/2 I VI/2 VI/2 IV/2 I VI/2 VI/2 IV/2 w', "y"],
                    "w": ['VII/2 I/2 II/2 V/2 u'],
                    "x": ['VI/4 III/4 II/4 I/4 w'],
                    "y": ["III/4 VI/4 II/4 V/4 VI/4 IV/4 VII2 x"],
                },
                "score": "w",
            },
            "rhythm": {
                "score_line": "i1 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6",
                "octave": 7,
                "duration": 54,
                "grammars": {
                    "u": ['"I"/2 "V"/2 "vi"/2 "iii"/2 "IV"/2 "I"/2 "IV"/2 "V"/2 u u', "y"],
                    "y": ['"I"/2 "vi" "IV"/2 "V"/2 y y u'],
                },
                "score": "u u y y u",
            },
            "timbre": {
                "score_line": "i3 %(time)f %(duration)f 2000 %(octave)d.%(note)s 2 3 5 3",
                "octave": 6,
                "duration": 54,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ['I2 VII2 V2 VI2 I2 IV/2 V/2 III2 u', 'I2 IV2 V2 IV I V2 III2 II2 u']
                },
                "score": "u u u u u",
            },
        },
        "zelda2": {  # Movement block 'a' for reuse throughout the piece
            "melody": {  # Instrument 'melody'
                "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 2",
                "octave": 8,
                "duration": 40,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ['I/2 I/2 VI IV/2 V2 z I/2 I/2 VI IV/2 V u', "w"],
                    "w": ['III/2 II/2 IV/2 III/2 V/2 IV/2 VI/2 V/2 w', 'u', 'x'],
                    "x": ['VII3 z2 V/4 IV/4 V/4 IV/4 V/4 VI/4 II/4 II/4 II/4 I/4 II/2 u', 'w'],
                },
                "score": "u",
            },
            "rhythm": {
                "score_line": "i1 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6",
                "octave": 7,
                "duration": 44,
                "grammars": {
                    "u": ['"I"/2 "V"/2 "vi"/2 "iii"/2 "IV"/2 "I"/2 "IV"/2 "V"/2 u u', "y"],
                    "y": ['"I"/2 "vi" "IV"/2 "V"/2 y y u'],
                },
                "score": "u u y y u",
            },
            "timbre": {
                "score_line": "i3 %(time)f %(duration)f 2000 %(octave)d.%(note)s 2 3 5 3",
                "octave": 6,
                "duration": 44,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ['I2 VII2 V2 VI2 I2 IV/2 V/2 III2 u', 'I2 IV2 V2 IV I V2 III2 II2 u']
                },
                "score": "u u u u u",
            },
        },
        "timbre_solo": {  # Movement block 'a' for reuse throughout the piece
            "rhythm": {
                "score_line": "i1 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6",
                "octave": 7,
                "duration": 30,
                "grammars": {
                    "u": ['"I"/2 "V"/2 "vi"/2 "iii"/2 "IV"/2 "I"/2 "IV"/2 "V"/2 u u', "y"],
                    "y": ['"I"/2 "vi" "IV"/2 "V"/2 y y u'],
                },
                "score": "u u y y u",
            },
            "timbre": {
                "score_line": "i3 %(time)f %(duration)f 2000 %(octave)d.%(note)s 2 3 5 3",
                "octave": 6,
                "duration": 30,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ['I VI/2 VI/2 IV/2 u', "y"],
                    "w": ['VII/2 I/2 II/2 V/2 u', 'w w', 'u x'],
                    "x": ['VI/4 III/4 II/4 I/4 w', 'x x', 'x u'],
                    "y": ["III/4 VI/4 II/4 V/4 VI/4 IV/4 VII2 w", 'y y'],
                },
                "score": "u",
            },
        },
        "outro1": {  # Movement block 'a' for reuse throughout the piece
            "melody": {  # Instrument 'melody'
                "score_line": "i2 %(time)f %(duration)f 7000 %(octave)d.%(note)s 2",
                "octave": 8,
                "duration": 20,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ['I VII V III u', "y"],
                    "w": ['VII I IV V VI u', 'w w'],
                    "x": ['VI/4 III/4 II/4 I/4 w', 'x x'],
                    "y": ["III/4 VI/4 II/4 V/4 VI/4 IV/4 VII2"],
                },
                "score": "w w x x w",
            },
            "rhythm": {
                "score_line": "i1 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6",
                "octave": 7,
                "duration": 26,
                "grammars": {
                    "u": ['"I" "V" "vi" "iii" "IV" "I" "IV" "V" u u', "y"],
                    "y": ['"I" "vi"2 "IV" "V" y y u'],
                },
                "score": "u u y y u",
            },
            "timbre": {
                "score_line": "i3 %(time)f %(duration)f 2000 %(octave)d.%(note)s 2 3 5 3",
                "octave": 6,
                "duration": 26,
                "grammars": {  # Notes for this instrument to use in this piece
                    "u": ['I2 VII2 V2 VI2 I2 IV/2 V/2 III2 u', 'I2 IV2 V2 IV I V2 III2 II2 u']
                },
                "score": "u u u u u",
            },
        },
        "outro2": {
            "rhythm": {
                "score_line": "i1 %(time)f %(duration)f 7000 %(octave)d.%(note)s %(octave)d.%(note)s 0 6",
                "octave": 7,
                "duration": 4,
                "grammars": {
                    "u": ['"I" "V" "vi" "iii" "IV" "I" "IV" "V" u u', "y"],
                    "y": ['"I" "vi"2 "IV" "V" y y u'],
                },
                "score": "u u y y u",
            },
        },
    }

    max_t = 0  # max time encountered so far. Used for movement timing
    progression = "intro1 intro2 overview a timbre_solo zelda1 b zelda2 outro1 outro2"
#    progression = "zelda1"
    for comp_name in progression.split():
        comp_start_time = max_t
        for instr_name, instr in composition[comp_name].iteritems():
            generated_score = generate_score(instr["score"], instr["grammars"])  # Fill in the scores by generating them based on the grammars
#            print generated_score
            score = parse.parse(generated_score, default_octave=instr["octave"])  # Return Node/Chord objects

            # Generate timestamps for the notes 
            t = comp_start_time
            for note in range(len(score)):
                score[note].time = t
                score[note].duration *= tempo
                t += score[note].duration
#                print "time difference =", t-comp_start_time
#                print "instrument duration =",composition[comp_name][instr_name]["duration"]
                if (t-comp_start_time) > float(composition[comp_name][instr_name]["duration"]):
#                    print "here"
                    score = score[:note]
                    break
                max_t = t if t > max_t else max_t
            composition[comp_name][instr_name]["score"] = score

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
