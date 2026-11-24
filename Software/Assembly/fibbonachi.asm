BBPLMain:
    LDR acc $0005
    STM acc $0500
    LDR acc $0000
    STM acc $0501
    LDR acc $0001
    STM acc $0502
    LDR acc $FFFF
    STM acc $0503
    LDM acc $0500
    PUSH acc
    LDM acc $0501
    PUSH acc
    LDM acc $0502
    PUSH acc
    JSR fibbonachiBBPL
    RSR
fibbonachiBBPL:
    POP r0
    POP acc
    STM acc $0500
    POP acc
    STM acc $0501
    POP acc
    STM acc $0502
    PUSH r0
    LDM acc $0500
    PUSH acc
fibbonachiLoop0:
    POP acc
    JEQ acc fibbonachiLoop0end
    SUB 1
    PUSH acc
    LDM acc $0502
    STM acc $0503
    LDM acc $0501
    PUSH r0
    LDM r0 $0502
    ADD r0
    STM acc $0502
    LDM acc $0503
    STM acc $0501
    JMP fibbonachiLoop0
fibbonachiLoop0end:
    POP r0
    LDM acc $0501
    PUSH acc
    PUSH r0
    RSR