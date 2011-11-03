sr=44100
ksmps=20
nchnls=1

instr 3
    if p5=1.05 then
        asig diskin2 "samples/bass/1.05.wav", 1
    elseif p5=1.06 then
        asig diskin2 "samples/bass/1.06.wav", 1
    elseif p5=1.07 then
        asig diskin2 "samples/bass/1.07.wav", 1
    elseif p5=1.08 then
        asig diskin2 "samples/bass/1.08.wav", 1
    elseif p5=1.08 then
        asig diskin2 "samples/bass/1.09.wav", 1
    elseif p5=1.10 then
        asig diskin2 "samples/bass/1.10.wav", 1
    elseif p5=1.11 then
        asig diskin2 "samples/bass/1.11.wav", 1
    elseif p5=2.00 then
        asig diskin2 "samples/bass/2.00.wav", 1
    elseif p5=2.01 then
        asig diskin2 "samples/bass/2.01.wav", 1
    elseif p5=2.02 then
        asig diskin2 "samples/bass/2.02.wav", 1
    elseif p5=2.03 then
        asig diskin2 "samples/bass/2.03.wav", 1
    elseif p5=2.04 then
        asig diskin2 "samples/bass/2.04.wav", 1
    elseif p5=2.05 then
        asig diskin2 "samples/bass/2.05.wav", 1
    elseif p5=2.06 then
        asig diskin2 "samples/bass/2.06.wav", 1
    elseif p5=2.07 then
        asig diskin2 "samples/bass/2.07.wav", 1
    elseif p5=2.08 then
        asig diskin2 "samples/bass/2.08.wav", 1
    elseif p5=2.09 then
        asig diskin2 "samples/bass/2.09.wav", 1
    elseif p5=2.10 then
        asig diskin2 "samples/bass/2.10.wav", 1
    elseif p5=2.11 then
        asig diskin2 "samples/bass/2.11.wav", 1
    elseif p5=3.00 then
        asig diskin2 "samples/bass/3.00.wav", 1
    elseif p5=3.01 then
        asig diskin2 "samples/bass/3.01.wav", 1
    elseif p5=3.02 then
        asig diskin2 "samples/bass/3.02.wav", 1
    elseif p5=3.03 then
        asig diskin2 "samples/bass/3.03.wav", 1
    elseif p5=3.04 then
        asig diskin2 "samples/bass/3.04.wav", 1
    elseif p5=3.05 then
        asig diskin2 "samples/bass/3.05.wav", 1
    elseif p5=3.06 then
        asig diskin2 "samples/bass/3.06.wav", 1
    elseif p5=3.07 then
        asig diskin2 "samples/bass/3.07.wav", 1
    elseif p5=3.08 then
        asig diskin2 "samples/bass/3.08.wav", 1
    elseif p5=3.09 then
        asig diskin2 "samples/bass/3.09.wav", 1
    elseif p5=3.10 then
        asig diskin2 "samples/bass/3.10.wav", 1
    elseif p5=3.11 then
        asig diskin2 "samples/bass/3.11.wav", 1
    endif
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

instr 5
    if p5=3.07 then
        asig diskin2 "samples/violin/3.07.wav", 1
    elseif p5=3.08 then
        asig diskin2 "samples/violin/3.08.wav", 1
    elseif p5=3.08 then
        asig diskin2 "samples/violin/3.09.wav", 1
    elseif p5=3.10 then
        asig diskin2 "samples/violin/3.10.wav", 1
    elseif p5=3.11 then
        asig diskin2 "samples/violin/3.11.wav", 1
    elseif p5=4.00 then
        asig diskin2 "samples/violin/4.00.wav", 1
    elseif p5=4.01 then
        asig diskin2 "samples/violin/4.01.wav", 1
    elseif p5=4.02 then
        asig diskin2 "samples/violin/4.02.wav", 1
    elseif p5=4.03 then
        asig diskin2 "samples/violin/4.03.wav", 1
    elseif p5=4.04 then
        asig diskin2 "samples/violin/4.04.wav", 1
    elseif p5=4.05 then
        asig diskin2 "samples/violin/4.05.wav", 1
    elseif p5=4.06 then
        asig diskin2 "samples/violin/4.06.wav", 1
    elseif p5=4.07 then
        asig diskin2 "samples/violin/4.07.wav", 1
    elseif p5=4.08 then
        asig diskin2 "samples/violin/4.08.wav", 1
    elseif p5=4.09 then
        asig diskin2 "samples/violin/4.09.wav", 1
    elseif p5=4.10 then
        asig diskin2 "samples/violin/4.10.wav", 1
    elseif p5=4.11 then
        asig diskin2 "samples/violin/4.11.wav", 1
    elseif p5=5.00 then
        asig diskin2 "samples/violin/5.00.wav", 1
    elseif p5=5.01 then
        asig diskin2 "samples/violin/5.01.wav", 1
    elseif p5=5.02 then
        asig diskin2 "samples/violin/5.02.wav", 1
    elseif p5=5.03 then
        asig diskin2 "samples/violin/5.03.wav", 1
    elseif p5=5.04 then
        asig diskin2 "samples/violin/5.04.wav", 1
    elseif p5=5.05 then
        asig diskin2 "samples/violin/5.05.wav", 1
    elseif p5=5.06 then
        asig diskin2 "samples/violin/5.06.wav", 1
    elseif p5=5.07 then
        asig diskin2 "samples/violin/5.07.wav", 1
    elseif p5=5.08 then
        asig diskin2 "samples/violin/5.08.wav", 1
    elseif p5=5.09 then
        asig diskin2 "samples/violin/5.09.wav", 1
    elseif p5=5.10 then
        asig diskin2 "samples/violin/5.10.wav", 1
    elseif p5=5.11 then
        asig diskin2 "samples/violin/5.11.wav", 1
    endif
    outs asig
endin
