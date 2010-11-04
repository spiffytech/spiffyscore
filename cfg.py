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

score = "u"

print score
while 1:
    found_substitution = False
    for key,value in grammars.iteritems():
        print "key, value =", key, value
        if score.find(key) != -1:
            print "here"
            found_substitution = True
            while score.find(key) != -1:
                score = score.replace(key, random.choice(grammars[key]), 1)
                print score
                time.sleep(.25)
    if found_substitution is False:
        break
print score
