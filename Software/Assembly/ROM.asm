ShiftFlag     = $0000

TermOut       = $6002
TermClock     = $6003
keyboardStart = $7000
keyboardEnd   = $7100

.org $8000

start:
    LDR r1 keyboardStart ; r1 is the KeyboardPointer

keyboardLoop:
    JSR keyboardInput

    JEQ r0 keyboardLoop

    JSR printChar

    JMP keyboardLoop

loop:
    JMP loop

outChar:
    STM r0 TermOut

    LDR r0 1
    STM r0 TermClock
    
    RSR

printChar:
    LDR acc r0
    PUSH acc

    SUB 8
    JEQ acc backspace

    JSR outChar
printCharReturn:
    POP acc
    RSR

backspace:
    LDR r0 8
    JSR outChar 
    LDR r0 " "
    JSR outChar
    LDR r0 8
    JSR outChar

    JMP printCharReturn

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

keyboardInput:
    LDM r0 r1 ; Load key pressed into r0
    JEQ r0 keyboardFinish

    JSR shiftCheck
    JNE acc keyboardReturn

    JSR letterCheck
    PUSH acc
    JSR spaceCheck

    POP r6
    OR r6
    PUSH acc

    JSR mappedCheck

    POP r6
    OR r6
    PUSH acc


    POP acc
    JEQ acc keyboardFinishFail

    LDR r0 r2 ; Load ascii into r0

keyboardReturn:
    LDR acc r1
    ADD 1
    LDR r1 acc
    SUB keyboardEnd
    JGE acc keyboardPointerReset

keyboardFinish:
    RSR
keyboardFinishFail:
    LDR r0 0
    JMP keyboardReturn

keyboardPointerReset:
    LDR r1 keyboardStart

    RSR


shiftCheck:
    ; $0048 is the key for shift
    ; $004C is the key for right shift

    ; ShiftFlag holds if shift has been pressed or not

    LDR acc r0
    SUB $0048
    JEQ acc shiftFlip

    LDR acc r0
    SUB $004C
    JEQ acc shiftFlip

    LDR acc 0

    RSR

shiftFlip:
    LDM acc ShiftFlag
    NOT
    STM acc ShiftFlag

    LDR acc $FFFF
    LDR r0 0

    RSR

letterCheck:
    LDR acc r0
    SUB $002B

    JLT acc letterReturn

    LDR acc r0
    SUB $0044

    JGT acc letterReturn

    LDM acc ShiftFlag
    JEQ acc letterUnshifted
    JNE acc letterShifted

letterReturn:
    LDR acc 0
    RSR

letterShifted:
    LDR acc r0
    ADD $0016

    LDR r2 acc

    LDR acc $FFFF

    RSR

letterUnshifted:
    LDR acc r0
    ADD $0036

    LDR r2 acc

    LDR acc $FFFF

    RSR

spaceCheck:
    ; $004E is the key for space
    LDR acc r0
    SUB $004E

    JNE acc spaceReturn

    LDR r2 $0020

    LDR acc $FFFF

    RSR
spaceReturn:
    LDR acc 0
    RSR

mappedCheck:
    ; $0029 is the key for backspace
    ; $002A is the key for tab
    ; $0049 is the key for enter

    ; $0058 is the key for *
    ; $0059 is the key for +
    ; $005A is the key for decimal .

    LDR r3 $0029
    LDR r4 $0008
    JSR mapFunc

    PUSH acc

    LDR r3 $002A
    LDR r4 $0009
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0049
    LDR r4 $000A
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0058
    LDR r4 "*"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0059
    LDR r4 "+"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $005A
    LDR r4 "."
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDM acc ShiftFlag
    JNE acc shiftedMapCheck

    ; $001C is the key for `
    ; $001D is the key for 1
    ; $001E is the key for 2
    ; $001F is the key for 3
    ; $0020 is the key for 4
    ; $0021 is the key for 5
    ; $0022 is the key for 6
    ; $0023 is the key for 7
    ; $0024 is the key for 8
    ; $0025 is the key for 9
    ; $0026 is the key for 0
    ; $0027 is the key for -
    ; $0028 is the key for =

    ; $0045 is the key for [
    ; $0046 is the key for ]

    ; $0051 is the key for ;
    ; $0052 is the key for '
    ; $0053 is the key for #
    ; $0054 is the key for \
    ; $0055 is the key for ,
    ; $0056 is the key for .
    ; $0057 is the key for /

    LDR r3 $001C
    LDR r4 "`"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $001D
    LDR r4 "1"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $001E
    LDR r4 "2"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $001F
    LDR r4 "3"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0020
    LDR r4 "4"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0021
    LDR r4 "5"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0022
    LDR r4 "6"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0023
    LDR r4 "7"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0024
    LDR r4 "8"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0025
    LDR r4 "9"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0026
    LDR r4 "0"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0027
    LDR r4 "-"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0028
    LDR r4 "="
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0045
    LDR r4 "["
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0046
    LDR r4 "]"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0051
    LDR r4 ";"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0052
    LDR r4 "'"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0053
    LDR r4 "#"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0054
    LDR r4 "\\"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0055
    LDR r4 ","
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0056
    LDR r4 "."
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0057
    LDR r4 "/"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    POP acc

    RSR

mapFunc:
    ; Uses r0 and r3 and r4
    ; r0 is the key, r3 is the mappedKey, r4 is the map
    ; if r0 is $0054 and r3 is $0054 then it will set r2 to r4
    LDR acc r0
    SUB r3
    JEQ acc mapEqual

    LDR acc 0
    RSR
mapEqual:
    LDR r2 r4

    LDR acc $FFFF
    RSR

shiftedMapCheck:
    ; $001C is the key for `
    ; $001D is the key for 1
    ; $001E is the key for 2
    ; $001F is the key for 3
    ; $0020 is the key for 4
    ; $0021 is the key for 5
    ; $0022 is the key for 6
    ; $0023 is the key for 7
    ; $0024 is the key for 8
    ; $0025 is the key for 9
    ; $0026 is the key for 0
    ; $0027 is the key for -
    ; $0028 is the key for =

    ; $0045 is the key for [
    ; $0046 is the key for ]

    ; $0051 is the key for ;
    ; $0052 is the key for '
    ; $0053 is the key for #
    ; $0054 is the key for \
    ; $0055 is the key for ,
    ; $0056 is the key for .
    ; $0057 is the key for /

    LDR r3 $001C
    LDR r4 "¬"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $001D
    LDR r4 "!"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $001E
    LDR r4 '"'
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $001F
    LDR r4 "£"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0020
    LDR r4 "$"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0021
    LDR r4 "%"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0022
    LDR r4 "^"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0023
    LDR r4 "&"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0024
    LDR r4 "*"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0025
    LDR r4 "("
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0026
    LDR r4 ")"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0027
    LDR r4 "_"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0028
    LDR r4 "+"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0045
    LDR r4 "{"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0046
    LDR r4 "}"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc
    
    LDR r3 $0051
    LDR r4 ":"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0052
    LDR r4 "@"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0053
    LDR r4 "~"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0054
    LDR r4 "|"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0055
    LDR r4 "<"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0056
    LDR r4 ">"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    LDR r3 $0057
    LDR r4 "?"
    JSR mapFunc

    POP r6
    OR r6
    PUSH acc

    POP acc

    RSR

debug:
    LDR r6 r0
    LDR r0 "@"
    JSR printChar
    LDR r0 r6

    RSR

message:
.zstring "Hello World!"