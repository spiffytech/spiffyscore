sr=44100
ksmps=20
nchnls=2

gifn ftgen 105, 0, 524288, -1,  "8.05.wav", 0, 0, 1 ; Middle C
gifn ftgen 106, 0, 524288, -1,  "8.06.wav", 0, 0, 1 ; Middle C
gifn ftgen 107, 0, 524288, -1,  "8.07.wav", 0, 0, 1 ; Middle C
gifn ftgen 108, 0, 524288, -1,  "8.08.wav", 0, 0, 1 ; Middle C
gifn ftgen 109, 0, 524288, -1,  "8.09.wav", 0, 0, 1 ; Middle C
gifn ftgen 110, 0, 524288, -1,  "8.10.wav", 0, 0, 1 ; Middle C
gifn ftgen 111, 0, 524288, -1,  "8.18.wav", 0, 0, 1 ; Middle C

instr 1
;    if p5=8.05 then
;        asig diskin "8.05.wav"
;    elseif p5=8.06 then
;        asig diskin "8.06.wav"
;    elseif p5=8.07 then
;        asig diskin "8.07.wav"
;    elseif p5=8.08 then
;        asig diskin "8.08.wav"
;    elseif p5=8.09 then
;        asig diskin "8.09.wav"
;    elseif p5=8.11 then
;        asig diskin "8.10.wav"
;    elseif p5=8.11 then
;        asig diskin "8.18.wav"
;    endif
    inum = p5*100
    asig loscil 1, 1, inum, 1 
    outs asig, asig
endin
