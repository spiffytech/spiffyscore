#!/usr/bin/env python

from __future__ import division
import ipdb
import os
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
            "body": {
                "pan_flute": {  # Instrument 'melody'
                    "channel": 8,
                    "octave": 5,
                    "duration": 60,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C2' B2 | A3 D3 || B | C' | D | C2' C2' | z | (u)", "C2' C2' | C2' C2' | (x)"],
                        "v": ["G2 F2 | E2 F2 | D5 (u)", "B/4 C/4' B/4 A/4 | D2 D2 | z | (u)"],
                        "x": ["z4 | (v)"],
                    },
                },
                "bass": {
                    "channel": 4,
                    "sync": "pan_flute",
                    "octave": 2,
                    "duration": 60,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C/2 C/2 C/2 z/2 (u)"],
                    },
                },
                "horn_timbre1": { 
                    "channel": 13,
                    "octave": 2,
                    "duration": 60,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C4 D4 (u)"],
                    },
                },
                "horn_timbre2": {  
                    "channel": 13,
                    "octave": 2,
                    "duration": 60,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["G4 A4 (u)"],
                    },
                },
            },
        },
        "section1": {
            "body": {
                "guitar": {  # Instrument 'melody'
                    "channel": 6,
                    "octave": 5,
                    "duration": 60,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C | E | A | F | G | z | (u)", "C | E | A | F | G | z | (v)"],
                        "v": ["A/2 D/2 | G/2 C/2 | F/2 B/2 | E/2 | z/2 | (u)"],
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
                "horn_timbre1": {
                    "channel": 13,
                    "octave": 2,
                    "duration": 60,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["C4 D4 (u)"],
                    },
                },
                "horn_timbre2": { 
                    "channel": 13,
                    "octave": 2,
                    "duration": 60,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["G4 A4 (u)"],
                    },
                },
            },
        },
    }

    section_start = 0
    for section_name in ["intro", "section1"]:
        print "Section " + section_name
        subsection_start = section_start
        section = composition[section_name]
        for subsection in ["intro", "body", "outro"]:
            if not section.has_key(subsection):
                continue
            print "\tSubsection " + subsection
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
                    print "\t\t\tvolume offset = %d, nev volume = %d" % (instr["vol_offset"], volume)
                midify_instr_score(instr_score, track, instr["channel"], subsection_start, volume=volume)
            longest_score = max(instrs, key=lambda i: score_len(i))
            subsection_start += score_len(longest_score)
            section_start += score_len(longest_score)
            track += 1
    with open("out.mid", "wb") as outfile:
        mymidi.writeFile(outfile)



def render_instr(instr, syncs, max_time):
    for g in instr["grammars"]:
        for i in range(len(instr["grammars"][g])):
            instr["grammars"][g][i] = parse.parse(instr["grammars"][g][i], default_octave=instr["octave"])

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
        if isinstance(token, parse.Chord):  # Chords
            for note in token.chord: 
                note = get_midi_note(token.octave, note)
                mymidi.addNote(track=track, channel=channel,pitch=note, time=t, duration=token.duration, volume=volume)
        elif isinstance(token, parse.Note):  # Individual notes
            note = get_midi_note(token.octave, token.value)
            mymidi.addNote(track=track, channel=channel,pitch=note, time=t, duration=token.duration, volume=volume)
        elif isinstance(token, tree.Tree):
            continue
        t += token.duration

    return []


if __name__ == "__main__": main() 
