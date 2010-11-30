sr=44100
ksmps=20
nchnls=1

instr 1
    asound pluck   p4, cpspch(p5), cpspch(p6), p7, p8 p9 p10
    out asound
endin

instr 2
    kenv linen p4, .1, p3, .2; envelope
    asound oscili kenv, cpspch(p5), p6; oscillator
    out asound
endin

instr 3
    asound foscili p4, cpspch(p5), 5, 2, 3, p9
    out asound
endin
