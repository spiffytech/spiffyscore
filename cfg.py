#!/usr/bin/env python

import os
import random
import sys
import time
random.seed(time.time())

grammars = {
    "u": ["I V I IV u", "e"],
    "e": [""],
}

# Generate the scale for the key we're in
comp_key = "C"
notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
scale = [comp_key]
pos = notes.index(comp_key)
progression = [2,2,1,2,2,2,1]
for p in progression:
    pos = (pos + p) % 12
    scale.append(notes[pos])

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

csound_note_values = {
    "C": "00",
    "C#": "01",
    "D": "02",
    "D#": "03",
    "E": "04",
    "F": "05",
    "F#": "06",
    "G": "07",
    "F#": "08",
    "A": "09",
    "A#": "10",
    "B": "11",
}


score = "u u u"
print score
while 1:
    found_substitution = False
    for key,value in grammars.iteritems():
        if score.find(key) != -1:
            found_substitution = True
            while score.find(key) != -1:
                score = score.replace(key, random.choice(grammars[key]), 1)
                print score
        #        time.sleep(.25)
    if found_substitution is False:
        break

csound_score = []
for token in score.split():
    csound_score.append(scale[scale_conversion[token]-1])

print csound_score

t = 0 
for token in csound_score:
    note = csound_note_values[token]
    print "i2 %f 2 7000 %d.%s %d.%s 0 6" % (t, random.choice([8,9]), note, random.choice([8,9]), note)
    t += .25
