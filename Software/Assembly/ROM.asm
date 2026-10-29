TermOut = $6002
TermClock = $6003


.org $8000
start:
    LDR acc message
    JSR printString

loop:
    JMP loop

printString:
    LDM r0 acc

    JEQ r0 printStringEnd

    ADD 1

    STM r0 TermOut

    LDR r0 1
    STM r0 TermClock

    JMP printString

printStringEnd:
    RSR

message:
.zstring "Hello World!"