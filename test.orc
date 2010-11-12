sr=44100
ksmps=20
nchnls=1

instr 1
    asound oscili p4, cpspch(p5), p6
    out asound
endin
instr 2
    asound pluck   p4, cpspch(p5), cpspch(p6), p7, p8 p9 p10
    out asound
endin
instr 3
    asound pluck   p4, cpspch(p5), cpspch(p6), p7, p8 p9 p10
    out asound
endin
