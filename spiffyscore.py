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
                "lead_instr": {  # Instrument 'melody'
                    "channel": 6,
                    "octave": 4,
                    "duration": 30,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["A/2, B/2, C/2 D/2 (u)", "D2' D2' D2' D2' (x)"],
                        "v": ["C/2 C/2 C/2 C/2 (w)"],
                        "w": ["E/2 F/2 E/2 F/2 (u)"],
                        "x": ["z4 (v)"],
                    },
                },
                "follow_instr": {  # Instrument 'bass'
                    "channel": 4,
                    "sync": "lead_instr",
                    "octave": 2,
                    "duration": 30,
                    "grammars": {  # Notes for this instrument to use in this piece
                        "u": ["E F G E (v)"],
                        "v": ["G A A A (e)", "G A A A (v)"],
                        "e": ["B A G A (u)"],
                        "x": ["z4 (e)"],
                    },
                },
            },
        },
    }
    print '''f1 0 512 10 1
f2 0 8192 10 .24 .64 .88 .76 .06 .5 .34 .08
f3 0 1025 10 1
t 0 60
    '''

    section_start = 0
    for section in ["intro"]:
        print "; Section " + section
        subsection_start = section_start
        section = composition[section]
        for subsection in ["intro", "body", "outro"]:
            try:
                print "; Subsection " + subsection
                subsection = section[subsection]

                unordered_instrs = []
                for instr in subsection:
                    subsection[instr]["name"] = instr
                    if not "sync" in subsection[instr].keys():
                        subsection[instr]["sync"] = None
                    unordered_instrs.append([subsection[instr]["sync"], instr])
                ordered_instrs = topsort.topsort(unordered_instrs)
                ordered_instrs.remove(None)  # None used as a placeholder for sort order for instruments with no sync setting

                instrs = []
                syncs = {}
                track = 0
                for instr in ordered_instrs:
                    print ";Instrument " + instr
                    instr = subsection[instr]
                    max_time = instr["duration"]
                    instr_score, syncs = render_instr(instr, syncs, max_time)
                    instrs.append(instr_score)
                    midify_instr_score(instr_score, track, instr["channel"], subsection_start)
                longest_score = max(instrs, key=lambda i: score_len(i))
                subsection_start += score_len(longest_score)
                section_start += score_len(longest_score)
                track += 1
            except KeyError:
                pass
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


def midify_instr_score(score, track, channel, t):
    # Assume get_midi_note()
    global mymidi

    for token in score:
        if isinstance(token, parse.Chord):  # Chords
            for note in token.chord: 
                note = get_midi_note(token.octave, note)
                mymidi.addNote(track=track, channel=channel,pitch=note, time=t, duration=token.duration, volume=100)
        elif isinstance(token, parse.Note):  # Individual notes
            note = get_midi_note(token.octave, token.value)
            mymidi.addNote(track=track, channel=channel,pitch=note, time=t, duration=token.duration, volume=100)
        elif isinstance(token, tree.Tree):
            continue
        t += token.duration

    return []


if __name__ == "__main__": main() 
