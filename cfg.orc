sr=44100
ksmps=20
nchnls=1

instr 1
;    kcps = 220
;    icps = 220
;    ifn  = 0
;    imeth = p4
;;    asig pluck 0.7, cpspch(p5), cpspch(p6), ifn, imeth, .1, 10
    asig pluck   p4, cpspch(p5), cpspch(p6), p7, p8 p9 p10
    out asig
endin

instr 2
    kenv linen p4, .1, p3, .2; envelope
    asound oscili kenv, cpspch(p5), p6; oscillator
    out asound
endin

instr 3
;    pylassigni "note", p5
;    pylruni "sample_file = 'samples/bass/%.2f.wav' % note"
;    Ssample_file pylevali "sample_file"

    Ssample_file sprintf "samples/bass/%.2f.wav", p5
    asig diskin2 Ssample_file, 1
    outs asig
endin

instr 4
    aFMinst foscili p4, cpspch(p5), p6, p7, p8, p9
endin

instr 5
    Ssample_file sprintf "samples/bass/%.2f.wav", p5
    asig diskin2 Ssample_file, 1
    outs asig
endin
