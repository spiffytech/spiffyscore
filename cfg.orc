sr=44100
ksmps=20
nchnls=2

;isf sfload "samples/acoustic_grand_piano_ydp.sf2"
isf sfload "samples/default.sf2"
sfplist isf
sfpassign 0, isf
;gipre sfpreset 0, 0, isf, 0

;gienginenum1 fluidEngine
;isfnum1 fluidLoad "samples/default.sf2"

instr 1
;    kcps = 220
;    icps = 220
;    ifn  = 0
;    imeth = p4
;;    asig pluck 0.7, cpspch(p5), cpspch(p6), ifn, imeth, .1, 10
    asig pluck   p4, cpspch(p5), cpspch(p6), p7, p8 p9 p10
    outs asig,asig
endin

instr 2
    kenv linen p4, .1, p3, .2; envelope
    asound oscili kenv, cpspch(p5), p6; oscillator
    outs asound,asound
endin

instr 3
;    pylassigni "note", p5
;    pylruni "sample_file = 'samples/bass/%.2f.wav' % note"
;    Ssample_file pylevali "sample_file"

    Ssample_file sprintf "samples/bass/%.2f.wav", p5
    asig diskin2 Ssample_file, 1
    outs asig,asig
endin

instr 4
    aFMinst foscili p4, cpspch(p5), p6, p7, p8, p9
endin

;instr 5
;    Ssample_file sprintf "samples/violin/%.2f.wav", p5
;    asig mp3in Ssample_file, 1
;    outs asig,asig
;endin

instr 6
    mididefault 60, p3
    midinoteonkey p4, p5
    inum init p4
    ivel init p5
    ivel init ivel/127
    kamp linsegr 1, 1, 1, .1, 0
    kamp = kamp/1000
    kfreq init 1
    a1,a2 sfplay3 ivel, inum, kamp*ivel, kfreq, 0
    outs a1,a2
endin

;instr 7
;
;endin
