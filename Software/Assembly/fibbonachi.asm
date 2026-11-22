BBPLMain:
    LDR acc 5
    PUSH acc
    LDR acc 0
    PUSH acc
    LDR acc 2
    PUSH acc
    JSR fibbonachi
    RSR
fibbonachi:
    POP r0
    POP r1
    POP r2
    POP r3
    PUSH r0
    LDR acc r1
    PUSH acc
fibbonachiLoop0:
    POP acc
    JEQ acc fibbonachiLoop0end
    SUB 1
    PUSH acc
    LDR r4 r3
    LDR acc r2
    ADD r3
    LDR r3 acc
    LDR r2 r4
    JMP fibbonachiLoop0
fibbonachiLoop0end:
    POP r0
    LDR acc r2
    PUSH acc
    PUSH r0
    RSR