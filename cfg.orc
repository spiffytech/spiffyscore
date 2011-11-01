sr=44100
ksmps=20
nchnls=1

instr 3
    inum = p5*100
    if inum=105 then
        asig diskin2 "samples/bass/1.05.wav", 1
    elseif inum=106 then
        asig diskin2 "samples/bass/1.06.wav", 1
    elseif inum=107 then
        asig diskin2 "samples/bass/1.07.wav", 1
    elseif inum=108 then
        asig diskin2 "samples/bass/1.08.wav", 1
    elseif inum=108 then
        asig diskin2 "samples/bass/1.09.wav", 1
    elseif inum=110 then
        asig diskin2 "samples/bass/1.10.wav", 1
    elseif inum=111 then
        asig diskin2 "samples/bass/1.11.wav", 1
    elseif inum=200 then
        asig diskin2 "samples/bass/2.00.wav", 1
    elseif inum=201 then
        asig diskin2 "samples/bass/2.01.wav", 1
    elseif inum=202 then
        asig diskin2 "samples/bass/2.02.wav", 1
    elseif inum=203 then
        asig diskin2 "samples/bass/2.03.wav", 1
    elseif inum=204 then
        asig diskin2 "samples/bass/2.04.wav", 1
    elseif inum=205 then
        asig diskin2 "samples/bass/2.05.wav", 1
    elseif inum=206 then
        asig diskin2 "samples/bass/2.06.wav", 1
    elseif inum=207 then
        asig diskin2 "samples/bass/2.07.wav", 1
    elseif inum=208 then
        asig diskin2 "samples/bass/2.08.wav", 1
    elseif inum=209 then
        asig diskin2 "samples/bass/2.09.wav", 1
    elseif inum=210 then
        asig diskin2 "samples/bass/2.10.wav", 1
    elseif inum=211 then
        asig diskin2 "samples/bass/2.11.wav", 1
    elseif inum=300 then
        asig diskin2 "samples/bass/3.00.wav", 1
    elseif inum=301 then
        asig diskin2 "samples/bass/3.01.wav", 1
    elseif inum=302 then
        asig diskin2 "samples/bass/3.02.wav", 1
    elseif inum=303 then
        asig diskin2 "samples/bass/3.03.wav", 1
    elseif inum=304 then
        asig diskin2 "samples/bass/3.04.wav", 1
    elseif inum=305 then
        asig diskin2 "samples/bass/3.05.wav", 1
    elseif inum=306 then
        asig diskin2 "samples/bass/3.06.wav", 1
    elseif inum=307 then
        asig diskin2 "samples/bass/3.07.wav", 1
    elseif inum=308 then
        asig diskin2 "samples/bass/3.08.wav", 1
    elseif inum=309 then
        asig diskin2 "samples/bass/3.09.wav", 1
    elseif inum=310 then
        asig diskin2 "samples/bass/3.10.wav", 1
    elseif inum=311 then
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
