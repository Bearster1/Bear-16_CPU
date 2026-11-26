Fizz = 3
Buzz = 5
BBPLMain:
    LDR acc ","
    PUSH acc
    LDR acc 5
    PUSH acc
    LDR acc 9
    PUSH acc
    LDR acc ","
    PUSH acc
    LDR acc 'h'
    PUSH acc
    LDR acc ','
    PUSH acc
    LDR acc "#"
    PUSH acc
    LDR acc "'"
    PUSH acc
    JSR printNum
    LDR acc $0000
    STM acc $0500
    LDR acc $0000
    STM acc $0501
    LDR acc $0000
    STM acc $0502
    LDR acc $0000
    STM acc $0503
    LDR acc $0000
    STM acc $0504
    LDR acc 20
    PUSH acc
fizzbuzzloop:
    POP acc
    JEQ acc fizzbuzzloopend
    SUB 1
    PUSH acc
    LDM acc $0504
    ADD 1
    STM acc $0504
    LDR acc 0
    STM acc $0503
    LDM acc $0504
    PUSH acc
    LDR acc Fizz
    PUSH acc
    JSR mod
    POP r0
fizz:
    LDR acc r0
    SUB 0
    JEQ acc fizztrue
    JMP fizzend
fizztrue:
        PUSH FizzWord
        JSR printString
    LDR acc 1
    STM acc $0503
fizzend:
    LDM acc $0504
    PUSH acc
    LDR acc Buzz
    PUSH acc
    JSR mod
    POP r0
buzz:
    LDR acc r0
    SUB 0
    JEQ acc buzztrue
    JMP buzzend
buzztrue:
        PUSH BuzzWord
        JSR printString
    LDM acc $0503
    ADD 1
    STM acc $0503
buzzend:
fizzbuzzstate:
    LDM acc $0503
    SUB 2
    JNE acc fizzbuzzstatetrue
    JMP fizzbuzzstateend
fizzbuzzstatetrue:
    LDM acc $0504
    PUSH acc
    JSR printNum
fizzbuzzstateend:
    PUSH "\n"
    JSR outChar
    JMP fizzbuzzloop
fizzbuzzloopend:
mod:
    POP r0
    POP acc
    STM acc $0501
    POP acc
    STM acc $0502
    PUSH r0
modLoop:
    LDM acc $0501
    PUSH r0
    LDM r0 $0502
    SUB r0
    JGE acc modLooptrue
    JMP modLoopend
modLooptrue:
    LDM acc $0501
    PUSH r0
    LDM r0 $0502
    SUB r0
    STM acc $0501
    JMP modLoop
modLoopend:
    POP r0
    LDM acc $0501
    PUSH acc
    PUSH r0
    RSR
printNum:
    POP r0
    POP acc
    STM acc $0500
    PUSH r0
    LDM acc $0500
    AND $F000
    LDR r0 acc
    LDR acc 12
    PUSH acc
firstHexLoop:
    POP acc
    JEQ acc firstHexLoopend
    SUB 1
    PUSH acc
    LDR acc r0
    RTS
    LDR r0 acc
    JMP firstHexLoop
firstHexLoopend:
    LDR acc r0
    PUSH acc
    JSR outHex
    LDM acc $0500
    AND $F00
    LDR r0 acc
    LDR acc 8
    PUSH acc
secondHexLoop:
    POP acc
    JEQ acc secondHexLoopend
    SUB 1
    PUSH acc
    LDR acc r0
    RTS
    LDR r0 acc
    JMP secondHexLoop
secondHexLoopend:
    LDR acc r0
    PUSH acc
    JSR outHex
    LDM acc $0500
    AND $F0
    LDR r0 acc
    LDR acc 4
    PUSH acc
thirdHexLoop:
    POP acc
    JEQ acc thirdHexLoopend
    SUB 1
    PUSH acc
    LDR acc r0
    RTS
    LDR r0 acc
    JMP thirdHexLoop
thirdHexLoopend:
    LDR acc r0
    PUSH acc
    JSR outHex
    LDM acc $0500
    AND $F
    LDR r0 acc
    LDR acc r0
    PUSH acc
    JSR outHex
    POP r0
    PUSH r0
    RSR
outHex:
    POP r0
    POP r1
    PUSH r0
    LDR acc r1
    AND $F
    LDR r1 acc
nums:
    LDR acc r1
    SUB $A
    JLT acc numstrue
    JMP numsend
numstrue:
    LDR acc r1
    ADD $30
    LDR r2 acc
        PUSH r1
        PUSH r2
        JSR outChar
        POP r1
numsend:
lets:
    LDR acc r1
    SUB 9
    JGT acc letstrue
    JMP letsend
letstrue:
    LDR acc r1
    ADD 7
    LDR r2 acc
        PUSH r2
        JSR outChar
letsend:
    POP r0
    PUSH r0
    RSR
FizzWord:
.zstring "Fizz"
BuzzWord:
.zstring "Buzz"