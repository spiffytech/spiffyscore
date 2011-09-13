#!/usr/bin/env python

import tree

from ply import lex, yacc
class Note():
    def __init__(self, value, duration=.25, octave=8):
        self.value = value
        self.duration = duration
        self.octave = octave
        self.accidental = None
    def __repr__(self):
        return "Note %s %s %s" % (self.value, self.duration, self.octave)

class Chord():
    def __init__(self, value, duration=.5, chord_type="major", octave=5):
        self.value = value
        self.duration = duration
        self.chord_type = chord_type
        self.octave = octave
    def __repr__(self):
        return "Chord %s %s %s" % (self.value, self.duration, self.chord_type, self.octave)


class Rest():
    def __init__(self, duration=.25):
        self.duration = duration
    def __repr__(self):
        return "Rest node %s" % self.duration


def parse(score, default_octave=8):
    # Tokenize (lex)
    tokens = (
        "NOTE_LENGTH",
        "BASENOTE",
        "ACCIDENTAL",
        "REST",
        "OCTAVE",
        "CHORD_TYPE",
        "QUOTE",
        "NODE",
    )

    t_ignore = " |"

    #t_BASENOTE = r"[A-Ga-g]"
#    t_BASENOTE = r"I+V?|VI*|i+v?|vi*"
    t_BASENOTE = r"[A-Ga-g]"
    t_ACCIDENTAL = r"\^{1,2}|_{1,2}|="
    t_REST = r"z"
    t_OCTAVE = r"'+|,+"
    t_CHORD_TYPE = r"m|7|m7|0|o|\+|mb5|sus|sus4|maj7|mmaj7|7sus4|dim|dim7|7b5|m7b5|6|b6|m6|mb6|46|maj9|9|add9|7b9|m9"
    t_QUOTE = '"'
    t_NODE = r"([a-zA-Z0-9_-]+)"

    def t_NOTE_LENGTH(t):
        r"/?\d+"
        multiplier = float(t.value.strip("/"))
        if t.value.startswith("/"):
            multiplier = 1/multiplier
        t.value = multiplier
        return t

    def t_error(t):
        raise TypeError("Unknown text '%s'" % (t.value,))

    lex.lex()

    #lex.input("GFG B'AB,, | g/2fg gab | GFG BAB | d2A AFD")
    #s = "GFG B'AB,, | g/2fg gab | GFG BAB | d2A AFD"
    #s = '''I IV V VI I "I" "ii"/2'''
    #s = "GF_G,/2"
    lex.input(score)
    #for tok in iter(lex.token, None):
    #    print repr(tok.type), repr(tok.value)


    # Parse (yacc)


    def p_pitch_list(p):
        '''score : score note
            | score chord
            | score rest
            | score node
        '''
        p[0] = p[1] + [p[2]]

    def p_score(p):
        '''score : note
            | chord
            | rest
            | node
        '''
        p[0] = [p[1]]


    def p_note(p):
        '''note : pitch
        '''
        p[0] = p[1]


    def p_note_length(p):
        ''' note : note NOTE_LENGTH
        '''
        new_note = p[1]
        new_note.duration = p[2]
        p[0] = new_note

    def p_chord_length(p):
        ''' chord : chord NOTE_LENGTH
        '''
        new_note = p[1]
        new_note.duration = p[2]
        p[0] = new_note


    def p_chord(p):
        '''chord : QUOTE pitch QUOTE
                | QUOTE pitch CHORD_TYPE QUOTE
        '''
        pitch = p[2].value
        pitch = pitch.upper()
        p[0] = Chord(value=pitch, octave=default_octave)
        if len(p) > 3:
            p[0].chord_type = p[3]


    def p_accidental(p):
        '''pitch : ACCIDENTAL pitch
        '''
        p[2].accidental = p[1]
        p[0] = p[2]

    def p_pitch_octave(p):
        '''pitch : pitch OCTAVE
        '''
        count = len(p[2])
        increment_or_decrement = 1 if p[2].startswith("'") else -1
        p[1].octave += (count * increment_or_decrement)
        p[0] = p[1]

    def p_pitch(p):
        '''pitch : BASENOTE
        '''
        p[0] = Note(p[1], octave=default_octave)

    def p_rest(p):
        ''' rest : REST
                | REST NOTE_LENGTH
        '''
        p[0] = Rest()
        if len(p) > 2:
            p[0].duration = p[2]

    def node(p):
        '''node: NODE
        '''
        p[0] = tree.tree(node.strip("(").strip(")"))


    def p_error(p):
        raise Exception("Syntax error at '%s' of element type %s" % (p.value, p.type))
        
    yacc.yacc()

    #print yacc.parse("GFG B'AB,, | g/2fg gab | GFG BAB | d2A AFD")
    return yacc.parse(score)
