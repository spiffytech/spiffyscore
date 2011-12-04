#!/usr/bin/env python

import tree

from ply import lex, yacc
class Note():
    def __init__(self, value, duration=1, octave=8):
        self.duration = duration
        if value > 12:
            self.duration += 1
            value = value % 12
        self.value = value
        self.octave = octave
    def __repr__(self):
        return "Note %s %s %s" % (self.value, self.duration, self.octave)

class Chord():
    def __init__(self, notes, duration=1):
        self.notes = notes
        self.duration = duration
    def __repr__(self):
        return "Chord %s" % (self.notes)

class Rest():
    def __init__(self, duration=1):
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
        "BRACKET",
        "SYNCOPATE",
        "NODE",
    )

    t_ignore = " |"

    t_BASENOTE = r"[A-Ga-g]"
#    t_BASENOTE = r"I+V?|VI*|i+v?|vi*"
    t_ACCIDENTAL = r"\^{1}|_{1}|="
    t_REST = r"z"
    t_OCTAVE = r"'+|,+"
    t_CHORD_TYPE = r"m|7|m7|0|o|\+|mb5|sus|sus4|maj7|mmaj7|7sus4|dim|dim7|7b5|m7b5|6|b6|m6|mb6|46|maj9|9|add9|7b9|m9"
    t_BRACKET = r"\[|\]"
    t_SYNCOPATE = "\+|-"
    t_NODE = r"\([a-zA-Z0-9_-]+\)"

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
    lex.input(score)


    # Parse (yacc)

    def p_note_list(p):
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


    def p_chord_length(p):
        ''' chord : chord NOTE_LENGTH
        '''
        new_note = p[1]
        new_note.duration = p[2]
        p[0] = new_note


    def p_note_length(p):
        ''' note : note NOTE_LENGTH
        '''
        new_note = p[1]
        new_note.duration = p[2]
        p[0] = new_note


    def p_chord(p):
        '''chord : BRACKET note BRACKET
                 | BRACKET note CHORD_TYPE BRACKET
        '''

        if len(p) > 3:
            chorded_notes = []
            root_note = p[2].value
            for offset in [0, 4, 7]:
                chorded_notes.append(Note(root_note+offset, octave=p[2].octave))
            chord = Chord(notes=chorded_notes)
        else:  # This won'k work until the grammar is modified to rocognise multiple notes botween brackets
            chord = p[1:-2]
                

        p[0] = chord


    def p_note_syncopate(p):
        ''' note : note SYNCOPATE
        '''
        note.syncopate = p[2]


    def p_accidental(p):
        '''note : ACCIDENTAL note
        '''
        if p[1] == "^":
            p[2].value += 1
        else:
            p[2].value -= 1
        p[0] = p[2]

    def p_octave(p):
        '''note : note OCTAVE
        '''
        count = len(p[2])
        increment_or_decrement = 1 if p[2].startswith("'") else -1
        p[1].octave += (count * increment_or_decrement)
        p[0] = p[1]

    def p_note(p):
        '''note : BASENOTE
        '''
        notes = {
            "C": 0,
            "D": 2,
            "E": 4,
            "F": 5,
            "G": 7,
            "A": 9,
            "B": 11
        }
        n = notes[p[1]]
        p[0] = Note(n, octave=default_octave)

    def p_rest(p):
        ''' rest : REST
                 | REST NOTE_LENGTH
        '''
        p[0] = Rest()
        if len(p) > 2:
            p[0].duration = p[2]

    def p_node(p):
        '''node : NODE
        '''
        p[0] = tree.Tree(p[1].strip("(").strip(")"))


    def p_error(p):
#        import ipdb
#        ipdb.set_trace()
        print p
        raise Exception("Syntax error at '%s' of element type %s" % (p.value, p.type))
        
    yacc.yacc()

    return yacc.parse(score)
