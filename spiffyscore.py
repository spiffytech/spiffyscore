#!/usr/bin/env python

from __future__ import division
import ipdb
import os
from pprint import pprint
import random
import sys
import time

from midiutil.MidiFile import MIDIFile as midifile
import parse
import topsort
import yaml

import tree

random.seed(time.time())
mymidi = midifile(15)

def main():
    composition = {
        "intro": {
            "intro": {
                "marimba": {
                    "channel": 15,
                    "octave": 3,
                    "duration": 20,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C/2 D/2 | F/2 D/2 | F/2 D/2 | C | (v)", "C/2 D/2 | F/2 D/2 | F/2 F/2 | C | (x)"],
                        "v": ["F/4 F/4 F/4 F/4 | F/4 F/4 D/2 | C/2 F/2 | C | (u)"],
                        "x": ["C2 | C2 | z2 | C | F | (v)"],
                    },
                },
            },
            "body": {
                "pan_flute": {
                    "channel": 8,
                    "octave": 5,
                    "duration": 80,
                    "vol_offset": -15,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C2' B2 | A3 D3 || B | C' | D | C2' C2' | z | (u)", "C2' C2' | C2' C2' | (x)"],
                        "v": ["G2 F2 | E2 F2 | D5 (u)", "B/4 C/4' B/4 A/4 | D2 D2 | z | (u)"],
                        "x": ["z8 | (v)"],
                    },
                },
                "taisho_koto": {
                    "channel": 11,
                    "octave": 5,
                    "duration": 80,
                    "sync": "pan_flute",
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C/2 F/2 | D/2 z/2 | z4 | (u)", "C/2 F/2 | G/2 F/2 | (u)", "A/2 F/2 z/2 C/2 | z | (v)"],
                        "v": ["z4 (x)"],
                        "x": ["C/2 C/2 | F/2 G/2 | F/2, G/2 | z/2 C/2 | (x)", "C/2 F/2 | D/2 C/4 z/4 | F/2 G/2 A/2 C/2 | (v)"],
                    },
                },
                "vibraphone": {
                    "channel": 14,
                    "vol_offset": 27,
                    "octave": 5,
                    "sync": "pan_flute",
                    "duration": 80,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["z4 (u)"],
                        "v": ["G2 F2 | E2 F2 | D5 (u)", "B/4 C/4' B/4 A/4 | D2 D2 | z | (u)"],
                        "x": ["z4 | (v)"],
                    },
                },
                "percusion": {
                    "channel": 9,  # Orchestra kit
                    "octave": 4,
                    "duration": 80,
                    "grammars": {
                        "u": ["A ^A (u)"]
                    }
                },
                "bass": {
                    "channel": 4,
                    "sync": "pan_flute",
                    "octave": 2,
                    "duration": 80,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C/2 C/2 C (u)"],
                    },
                },
            },
        },
        "section1": {
            "body": {
                "percusion": {
                    "channel": 9,  # Orchestra kit
                    "octave": 4,
                    "duration": 80,
                    "grammars": {
                        "u": ["A ^A (u)"]
                    }
                },
                "vibraphone": {
                    "channel": 14,
                    "vol_offset": 27,
                    "octave": 5,
                    "duration": 80,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C2' B2 | A3 D3 || B | C' | D | C2' C2' | z | (u)", "C2' C2' | C2' C2' | (x)"],
                        "v": ["G2 F2 | E2 F2 | D5 (u)", "B/4 C/4' B/4 A/4 | D2 D2 | z | (u)"],
                        "x": ["z4 | (v)"],
                    },
                },
                "bass": {
                    "channel": 4,
                    "sync": "vibraphone",
                    "octave": 2,
                    "duration": 80,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C/2 C/2 C (u)"],
                    },
                },
                "horn_timbre1": { 
                    "channel": 13,  # 'Atmosphere'
                    "octave": 2,
                    "duration": 80,
                    "vol_offset": -15,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["[C]4 [D]4 (u)"],
                    },
                },
            },
        },
        "section2": {
            "intro": {
                "reverse_cymbal": {
                    "channel": 5,
                    "octave": 3,
                    "duration": 3,
                    "grammars": {
                        "u": ["B3"]
                    }
                },
                "bass": {
                    "channel": 4,
                    "octave": 2,
                    "duration": 3,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C/2 C/2 C (u)"],
                    },
                },
                "percusion": {
                    "channel": 9,  # Orchestra kit
                    "octave": 4,
                    "duration": 3,
                    "vol_offset": -10,
                    "grammars": {
                        "u": ["E,, | z2 | (u)"]
                    }
                },
                "atmosphere1": {
                    "channel": 13,
                    "octave": 2,
                    "duration": 3,
                    "vol_offset": -15,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["[C]3 (u)"],
                    },
                },
            },
            "body": {
                "guitar": {  # Instrument 'melody'
                    "channel": 11,
                    "octave": 4,
                    "duration": 60,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C | F | D | C | D | z2 | (x)", "C | E | A | F | G | z | (v)"],
                        "v": ["A/2 D/2 | G/2 C/2 | F/2 B/2 | E/2 | z/2 | (u)"],
                        "x": ["A | C/2 C/2 | F/2 D/2 | (u)"],
                    },
                },
                "bass": {  # Instrument 'bass'
                    "channel": 4,
                    "sync": "guitar",
                    "octave": 2,
                    "duration": 60,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C/2 C/2 | C/2 z/2 | (u)"],
                    },
                },
                "percusion": {
                    "channel": 9,  # Orchestra kit
                    "octave": 4,
                    "duration": 60,
                    "vol_offset": -10,
                    "grammars": {
                        "u": ["^G,, | ^A,, | ^G,,/2 ^A,,/2 | E,, | z4 | (u)", "E,, | z4 | (u)"]
                    }
                },
                "atmosphere1": {
                    "channel": 13,
                    "octave": 2,
                    "duration": 60,
                    "vol_offset": -15,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["[C]4 [D]4 (u)"],
                    },
                },
            },
        },
#        "JollyRogerLagoon": {
#            "body": {
##                "piccolo": {
##                    "channel": 8,
##                    "octave": 6,
##                    "duration": 60,
##                    "grammars": {  # Notes for this instrument to use in this piece
##                        "u": ["F/8 z/8 F/8 z/8 C/8 z/8 C/8 | z2 | (u)"],
##                    },
##                },
#                "harp": {
#                    "channel": 14,
#                    "octave": 5,
#                    "duration": 60,
#                    "grammars": {  # Notes for this instrument to use in this piece
#                        "u": ["C/2 D/2 | E/2 F/2 | C/2 z/2 | z | (v)", " | (v)"],
#                    },
#                },
#                "violin": {
#                    "channel": 3,
#                    "octave": 4,
#                    "duration": 60,
#                    "vol_offset": -55,
#                    "grammars": {  # Notes for this instrument to use in this piece
#                        "u": ["C2 G2 F2 B,2 C3 (u)"],
#                    },
#                },
#            },
#        },
        "JollyRogerLagoon": {
            "body": {
                "harp": {
                    "channel": 14,
                    "octave": 3,
                    "duration": 70,
                    "sync": "marimba",
                    "vol_offset": 27,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["z (u)"],
                        "v": ["z (v)"],
                        "x": ["z (x)"],
                        "w": ["C | F/2 F/2 | D/2 D/2 C/2 C/2 | F | (w)"],
                    },
                },
                "percussion2": {
                    "channel": 12,
                    "octave": 4,
                    "duration": 70,
#                    "vol_offset": -20,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C | C | C/2 D/2 | C | z | (u)"],
                    },
                },
                "horn_timbre": {
                    "channel": 13,  # 'Atmosphere'
                    "octave": 2,
                    "duration": 70,
                    "vol_offset": -15,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["[C]4 [D]4 (u)"],
                    },
                },
                "percusion": {
                    "channel": 9,  # Orchestra kit
                    "octave": 4,
                    "duration": 70,
                    "grammars": {
                        "u": ["A ^A (u)"]
                    }
                },
                "marimba": {
                    "channel": 15,
                    "octave": 3,
                    "duration": 70,
                    "vol_offset": 10,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C/2 D/2 | F/2 D/2 | F/2 D/2 | C | z | (v)", "C/2 D/2 | F/2 D/2 | F/2 F/2 | C | z | (x)"],
                        "v": ["F/4 F/4 F/4 F/4 | F/4 F/4 D/2 | C/2 F/2 | C | z | (u)"],
                        "x": ["C2 | C2 | z2 | C | F | (w)"],
                        "w": [" z8 | (u)"],
                    },
                },
            },
        },
        "end": {
            "body": {
                "horn_timbre": {
                    "channel": 13,  # 'Atmosphere'
                    "octave": 2,
                    "duration": 40,
                    "vol_offset": -15,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["[C]4 [D]4 (u)"],
                    },
                },
                "percusion": {
                    "channel": 9,  # Orchestra kit
                    "octave": 4,
                    "duration": 40,
                    "grammars": {
                        "u": ["A ^A (u)"]
                    }
                },
                "pan_flute": {
                    "channel": 8,
                    "octave": 5,
                    "duration": 40,
                    "vol_offset": -15,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C2' B2 | A3 D3 || B | C' | D | C2' C2' | z | (u)", "C2' C2' | C2' C2' | (x)"],
                        "v": ["G2 F2 | E2 F2 | D5 (u)", "B/4 C/4' B/4 A/4 | D2 D2 | z | (u)"],
                        "x": ["z8 | (v)"],
                    },
                },
                "taisho_koto": {
                    "channel": 11,
                    "octave": 5,
                    "duration": 40,
                    "sync": "pan_flute",
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C/2 F/2 | D/2 z/2 | z4 | (u)", "C/2 F/2 | G/2 F/2 | (u)", "A/2 F/2 z/2 C/2 | z | (v)"],
                        "v": ["z4 (x)"],
                        "x": ["C/2 C/2 | F/2 G/2 | F/2, G/2 | z/2 C/2 | (x)", "C/2 F/2 | D/2 C/4 z/4 | F/2 G/2 A/2 C/2 | (v)"],
                    },
                },
            },
            "outro": {
                "horn_timbre": {
                    "channel": 13,  # 'Atmosphere'
                    "octave": 2,
                    "duration": 20,
                    "vol_offset": -15,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["[C]4 [D]4 (u)"],
                    },
                },
                "percusion": {
                    "channel": 9,  # Orchestra kit
                    "octave": 4,
                    "duration": 20,
                    "grammars": {
                        "u": ["A ^A (u)"]
                    }
                },
            },
        }
    }

    section_start = 0
    for section_name in ["intro", "section1", "section2", "JollyRogerLagoon", "end"]:
        print "Section", section_name, "at second", section_start
        subsection_start = section_start
        section = composition[section_name]
        for subsection in ["intro", "body", "outro"]:
            if not section.has_key(subsection):
                continue
            print "\tSubsection", subsection, "at", subsection_start
            subsection = section[subsection]

            unordered_instrs = []
            for instr in subsection:
                subsection[instr]["name"] = instr
                if not "sync" in subsection[instr].keys():
                    subsection[instr]["sync"] = None
                unordered_instrs.append([subsection[instr]["sync"], instr])
            ordered_instrs = topsort.topsort(unordered_instrs)
            ordered_instrs.remove(None)  # None used as a placeholder for sort order for instruments with no sync setting
            for sync_instr in ordered_instrs:
                if sync_instr not in subsection.keys():
                    raise KeyError("The sync instrument '%s' does not exist in this subsection" % sync_instr)

            instrs = []
            syncs = {}
            track = 0
            for instr in ordered_instrs:
                print "\t\tInstrument " + instr
#                if instr == "guitar":
#                    ipdb.set_trace()
                instr = subsection[instr]
                max_time = instr["duration"]
                instr_score, syncs = render_instr(instr, syncs, max_time)
                instrs.append(instr_score)

                volume = 100
                if instr.has_key("vol_offset"):
                    volume += instr["vol_offset"]
                mymidi.addTrackName(track, 0, instr["name"])
                midify_instr_score(instr_score, track, instr["channel"], subsection_start, volume=volume)
                track += 1
            longest_score = max(instrs, key=lambda i: score_len(i))
            subsection_start += score_len(longest_score)
            section_start += score_len(longest_score)
    with open("out.mid", "wb") as outfile:
        mymidi.writeFile(outfile)



def render_instr(instr, syncs, max_time):
    for g in instr["grammars"]:
        for i in range(len(instr["grammars"][g])):
            try:
                instr["grammars"][g][i] = parse.parse(instr["grammars"][g][i], default_octave=instr["octave"])
            except topsort.CycleError:
                print "Your syncs created a loop! Fix it."
                sys.exit(1)

    score= []
    try:
        score, syncs = choose_phrase(instr, syncs, 0, max_time, None)

        while True:
            score_index_to_replace = None
            for item in range(len(score)):  # Optimize this by caching the index of the last node I replaced and startng there
                if isinstance(score[item], tree.Tree):  # Also, make this use the find_next_node() function (or whatever I called it)
                    score_index_to_replace = item
            if score_index_to_replace is None:
                raise ValueError("No more nodes to fill in")

            time_remaining = max_time - score_len(score)
            new_phrase, syncs = choose_phrase(instr, syncs, score_len(score), time_remaining, score)
            score = score[:score_index_to_replace] + new_phrase + score[score_index_to_replace+1:]

    except ValueError:
        return (score, syncs)


def choose_phrase(instr, syncs, current_time, time_remaining, score):
    '''Filters grammars for ones that match the sync option, and phrases that fit the time remaining in the score'''
    time_filtered_grammars = {}
    for grammar in instr["grammars"]:
         fitting_phrases = get_phrases_that_fit(instr["grammars"][grammar], time_remaining)
         if len(fitting_phrases) > 0:
            time_filtered_grammars[grammar] = fitting_phrases
    if len(time_filtered_grammars.keys()) == 0:
        raise ValueError("No available grammars that will fit in the score")

    grammar = None
#    if instr["name"] == "taisho_koto":
#        ipdb.set_trace()

    if instr["sync"] is not None:
        guiding_instr = instr["sync"]
        sync_node = get_sync_node_at_time(syncs[guiding_instr], current_time)
        if sync_node in time_filtered_grammars.keys():
            grammar = sync_node
        else:
            grammar = random.choice(time_filtered_grammars.keys())
    if score is None:
        grammar = random.choice(time_filtered_grammars.keys())
    elif instr["sync"] is None:
        grammar = get_next_node(score);
        if grammar not in instr["grammars"].keys():
            raise Exception("You tried to direct a grammar to a node that doesn't exist")

    if grammar not in time_filtered_grammars.keys():
        return [], syncs

    phrases = time_filtered_grammars[grammar]
    if instr["name"] not in syncs.keys():
        syncs[instr["name"]] = []
    syncs[instr["name"]].append({"node": grammar, "time": current_time})

    return random.choice(phrases), syncs


def get_phrases_that_fit(grammar, time_remaining):
    valid_phrases = []
    for phrase in grammar:
        if score_len(phrase) <= time_remaining:
            valid_phrases.append(phrase)
    return valid_phrases


def get_sync_node_at_time(syncs, t):
    for s in range(len(syncs)):
        if syncs[s]["time"] >= t:
            return syncs[s]["node"]

def get_next_node(score):
    for token in score:
        if isinstance(token, tree.Tree):
            return token.name


def score_len(score):
    total = 0
    for n in score:
        if not isinstance(n, tree.Tree):
            total += n.duration
    return total


def get_midi_note(octave, note):
    return note + 12 * (octave+1)


def midify_instr_score(score, track, channel, t, volume):
    # Assume get_midi_note()
    global mymidi

    for token in score:
        if isinstance(token, parse.Chord):
            for note in token.notes: 
                note = get_midi_note(note.octave, note.value)
                mymidi.addNote(track=track, channel=channel,pitch=note, time=t, duration=token.duration, volume=volume)
        elif isinstance(token, parse.Note):  # Individual notes
            note = get_midi_note(token.octave, token.value)
            mymidi.addNote(track=track, channel=channel,pitch=note, time=t, duration=token.duration, volume=volume)
        elif isinstance(token, tree.Tree):
            continue
        t += token.duration

    return []


if __name__ == "__main__": main() 
