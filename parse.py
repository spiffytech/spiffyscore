#!/usr/bin/env python

from ply import lex, yacc

# Tokenize (lex)
tokens = (
    "NOTE_LENGTH",
    "BASENOTE",
    "ACCIDENTAL",
    "REST",
    "OCTAVE",
    "CHORD_TYPE",
)

t_BASENOTE = r"[A-Ga-g]"
t_ACCIDENTAL = r"\^{1,2}|_{1,2}|="
t_REST = r"z"
t_OCTAVE = r"'+|,+"
t_CHORD_TYPE = r"m|7|m7|0|o|\+|mb5|sus|sus4|maj7|mmaj7|7sus4|dim|dim7|7b5|m7b5|6|b6|m6|mb6|46|maj9|9|add9|7b9|m9"

def t_NOTE_LENGTH(t):
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

#lex.input("GFG B'AB,, | g/2fg gab | GFG BAB | d2A AFD")
#s = "GFG B'AB,, | g/2fg gab | GFG BAB | d2A AFD"
s = "GF_G,"
lex.input(s)
for tok in iter(lex.token, None):
    print repr(tok.type), repr(tok.value)


# Parse (yacc)

class Note(object):
    def __init__(self, value, duration=.25, octave=8):
        self.value = value
        self.duration = duration
        self.octave = octave
    def __repr__(self):
        return "Note %s %s %s" % (self.value, self.duration, self.octave)

#def p_element(p):
#    "element : note_element"
#    p[0] = p[1]
#
#def p_note_element(p):
#    '''note_element : note_element note_stem
#                     | note_stem
#    '''
#    p[0] = p[1]
#
#def p_note_stem(p):
#    '''note_stem : note'''
#    p[0] = p[1]
#
#def p_note(p):
#    '''note : note_or_rest
#            | note_or_rest NOTE_LENGTH
#    '''
#    p[0] = p[1]
#
#def p_note_or_rest(p):
#    '''note_or_rest : pitch
#                    | REST
#    '''
#    p[0] = p[1]
#
#def p_pitch(p):

def p_pitch_list(p):
    '''score : score pitch
    '''
    p[0] = p[1] + [p[2]]

def p_sore(p):
    '''score : pitch
    '''
    p[0] = [p[1]]


def p_pitch_more(p):
    ''' score : pitch NOTE_LENGTH
    '''
    print "stuff"
    new_note = p[1]
    new_note.duration = p[2]
    p[0] = new_note

def p_pitch(p):
    '''pitch : BASENOTE
    '''
    p[0] = Note(p[1])

def p_accidental(p):
    '''pitch : ACCIDENTAL pitch
    '''
    p[2].accidental = p[1]
    p[0] = p[2]

def p_octave(p):
    '''pitch : pitch OCTAVE
    '''
    count = len(p[2])
    increment_or_decrement = 1 if p[2][0] == "," else -1
    octave = 8 + (count * increment_or_decrement)
    p[1].octave = octave
    p[0] = p[1]

def p_error(p):
    print "Syntax error at '%s' of element type %s" % (p.value, p.type)
    
yacc.yacc()

#print yacc.parse("GFG B'AB,, | g/2fg gab | GFG BAB | d2A AFD")
print yacc.parse(s)
