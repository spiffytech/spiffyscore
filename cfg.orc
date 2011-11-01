sr=44100
ksmps=20
nchnls=1

gifn ftgen 105, 0, 524288, -1,  "samples/bass/1.05.wav", 0, 0, 1 ; Middle C
gifn ftgen 106, 0, 524288, -1,  "samples/bass/1.06.wav", 0, 0, 1 ; Middle C
gifn ftgen 107, 0, 524288, -1,  "samples/bass/1.07.wav", 0, 0, 1 ; Middle C
gifn ftgen 108, 0, 524288, -1,  "samples/bass/1.08.wav", 0, 0, 1 ; Middle C
gifn ftgen 109, 0, 524288, -1,  "samples/bass/1.09.wav", 0, 0, 1 ; Middle C
gifn ftgen 110, 0, 524288, -1,  "samples/bass/1.10.wav", 0, 0, 1 ; Middle C
gifn ftgen 111, 0, 524288, -1,  "samples/bass/1.11.wav", 0, 0, 1 ; Middle C
gifn ftgen 200, 0, 524288, -1,  "samples/bass/2.01.wav", 0, 0, 1 ; Middle C
gifn ftgen 201, 0, 524288, -1,  "samples/bass/2.02.wav", 0, 0, 1 ; Middle C
gifn ftgen 202, 0, 524288, -1,  "samples/bass/2.03.wav", 0, 0, 1 ; Middle C
gifn ftgen 203, 0, 524288, -1,  "samples/bass/2.04.wav", 0, 0, 1 ; Middle C
gifn ftgen 204, 0, 524288, -1,  "samples/bass/2.05.wav", 0, 0, 1 ; Middle C
gifn ftgen 206, 0, 524288, -1,  "samples/bass/2.06.wav", 0, 0, 1 ; Middle C
gifn ftgen 207, 0, 524288, -1,  "samples/bass/2.07.wav", 0, 0, 1 ; Middle C
gifn ftgen 208, 0, 524288, -1,  "samples/bass/2.08.wav", 0, 0, 1 ; Middle C
gifn ftgen 209, 0, 524288, -1,  "samples/bass/2.09.wav", 0, 0, 1 ; Middle C
gifn ftgen 210, 0, 524288, -1,  "samples/bass/2.10.wav", 0, 0, 1 ; Middle C
gifn ftgen 211, 0, 524288, -1,  "samples/bass/2.11.wav", 0, 0, 1 ; Middle C
gifn ftgen 300, 0, 524288, -1,  "samples/bass/3.00.wav", 0, 0, 1 ; Middle C
gifn ftgen 301, 0, 524288, -1,  "samples/bass/3.01.wav", 0, 0, 1 ; Middle C
gifn ftgen 302, 0, 524288, -1,  "samples/bass/3.02.wav", 0, 0, 1 ; Middle C
gifn ftgen 303, 0, 524288, -1,  "samples/bass/3.03.wav", 0, 0, 1 ; Middle C
gifn ftgen 304, 0, 524288, -1,  "samples/bass/3.04.wav", 0, 0, 1 ; Middle C
gifn ftgen 305, 0, 524288, -1,  "samples/bass/3.05.wav", 0, 0, 1 ; Middle C
gifn ftgen 306, 0, 524288, -1,  "samples/bass/3.06.wav", 0, 0, 1 ; Middle C
gifn ftgen 307, 0, 524288, -1,  "samples/bass/3.07.wav", 0, 0, 1 ; Middle C
gifn ftgen 308, 0, 524288, -1,  "samples/bass/3.08.wav", 0, 0, 1 ; Middle C
gifn ftgen 309, 0, 524288, -1,  "samples/bass/3.09.wav", 0, 0, 1 ; Middle C
gifn ftgen 310, 0, 524288, -1,  "samples/bass/3.10.wav", 0, 0, 1 ; Middle C
gifn ftgen 311, 0, 524288, -1,  "samples/bass/3.11.wav", 0, 0, 1 ; Middle C

instr 3
    inum = p5*100
    asig loscil 1, 1, inum, 1 
    outs asig
endin

instr 1
    asound pluck   p4, cpspch(p5), cpspch(p6), p7, p8 p9 p10
    out asound
endin

instr 2
    kenv linen p4, .1, p3, .2; envelope
    asound oscili kenv, cpspch(p5), p6; oscillator
    out asound
endin

instr 4
    aFMinst foscili p4, cpspch(p5), p6, p7, p8, p9
endin
