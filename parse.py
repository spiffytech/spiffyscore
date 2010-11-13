#!/usr/bin/env python

from ply import lex

tokens = (
    "NOTE",
    "REST",
    "SHARP",
    "FLAT",
    "OCTAVE",
    "NATURAL",
    "LENGTH",
)

t_NOTE = r"[A-Ga-g]"
t_REST = r"z"
t_SHARP = r"\^"
t_FLAT = r"_"
t_NATURAL = r"="
t_OCTAVE = r"'+|,+"

def t_LENGTH(t):
    r"/?\d+"
    multiplier = float(t.value.strip("/"))
    if t.value.startswith("/"):
        multiplier = 1/multiplier
    t.value = multiplier
    return t

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

t_ignore = " |"

lex.lex()

lex.input("GFG B'AB,, | g/2fg gab | GFG BAB | d2A AFD")
for tok in iter(lex.token, None):
    print repr(tok.type), repr(tok.value)
