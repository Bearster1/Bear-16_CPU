KeyboardPointer     = $0000
ShiftFlag           = $0001

TermOut             = $6002
TermClock           = $6003

MemoryIn            = $6012
MemoryOut           = $6013
MemoryAddress       = $6014
MemoryClock         = $6015

KeyboardStart       = $7000
KeyboardEnd         = $7100

.org $8000

; Code conventions:
; Variables, zstrings and Bitmaps are named using Pascal Case
; Subroutines are named using Camel Case
; For things where it is either True or False use $FFFF for True and $0000 for False

start:
    LDR r0 KeyboardStart
    STM r0 KeyboardPointer ; Settup the KeyboardPointer

    PUSH NewLine
    JSR printString

    PUSH $0000
main:
    JSR keyboard

    JSR specialCharFix

    POP r0 ; Prevents writing of Null to the screen
    JEQ r0 main
    PUSH r0
    PUSH r0

    JSR outChar

    JSR commands

    JMP main

loop:
    JMP loop


commands:
    POP r0 ; This holds the return address
    POP r1 ; This holds the pressed key

    LDR acc r1 ; Jump to no enter if value isn't Enter
    SUB $000A
    JNE acc commandNoEnter

    ; This is enter true:

    POP acc ; This holds the second pressed key
    SUB "1"

    PUSH r0
    JEQ acc command1

    PUSH r0
    PUSH commandFail
    JSR printString

commandReturn:
    PUSH NewLine
    JSR printString

    POP r0

    JMP commandEnd

commandNoEnter:
    PUSH r1 ; Add the pressed key to the stack

commandEnd:
    PUSH r0 ; Push the return address
    
    RSR

command1:
    PUSH Message
    JSR printString

    JMP commandReturn


specialCharFix:
    POP r0
    POP r1 ; This is the character to check
    
    LDR acc r1
    SUB $00C0

    JGE acc specialCharTrue

    PUSH r1
    PUSH r0

    RSR

specialCharTrue:
    PUSH $0000
    PUSH r0

    RSR


outChar:
    POP r0
    POP r1 ; This is the character to output
    PUSH r0

.word $FF01
    STM r1 TermOut
    
    LDR r1 $FFFF
    STM r1 TermClock

    RSR

printString:
    POP r0
    POP acc ; This is the address of the string to output
    PUSH r0

printStringLoop:
    LDM r1 acc ; This takes the current character and places it into r1
    JEQ r1 printStringEnd

    ADD $0001

    PUSH acc
    PUSH r1 ; this is the character to output
    JSR outChar
    POP acc

    JMP printStringLoop

printStringEnd:
    RSR


inMem:
    ; On the stack the first thing is the data, the second is the address.

    POP r0
    POP r1 ; This is the data
    POP r2 ; This is the address
    PUSH r0

    STM r1 MemoryIn
    STM r2 MemoryAddress

    LDR r1 $FFFF
    STM r1 MemoryClock

    RSR

outMem:
    POP r0
    POP r1 ; This is the address
    ; Normally I would put PUSH r0 here to return the returnAddress to the stack but since I need to push a value to the stack I will not.

    STM r1 MemoryAddress
    LDM r1 MemoryOut ; This is the collected data

    PUSH r1 ; Push the data
    PUSH r0 ; Push the returnAddress

    RSR


keyboard:
    ; This will take the next key needed to be decoded and turn it into the ascii character
    ; This will be done through a bitmap

    LDM r1 KeyboardPointer ; r1 holds the address of the key that was pressed
    LDM r0 r1 ; r0 holds the key that was pressed

    JEQ r0 keyboardFinish

    LDR acc KeyboardMap
    ADD r0
    SUB $0001

    LDM r1 acc ; r1 holds the ascii code now

    LDM acc KeyboardPointer
    SUB KeyboardEnd
    JEQ keyboardPointerReset
keyboardReturn:

    LDM r0 ShiftFlag ; r0 holds the Condition of the Shift Flag

    JEQ r0 unshiftedKeyboard
    JNE r0 shiftedKeyboard

    RSR

keyboardPointerReset:
    LDR r0 KeyboardStart
    STM r0 KeyboardPointer ; Reset the KeyboardPointer

    JMP keyboardReturn

shiftedKeyboard:
    LDR acc r1 ; Acc holds the ascii code now

    AND $FF00

    LDR r0 $0008
    LDR r1 acc

shiftedKeyboardLoop:
    LDR acc r1
    RTS ; Right Shifts the Acc
    LDR r1 acc

    LDR acc r0
    SUB $0001
    LDR r0 acc

    JNE acc shiftedKeyboardLoop

    ; We now have the key in the second byte meaning it is ready to be returned

    PUSH r1 ; Push the ascii key
    PUSH r1 ; Push a duplicate
    JSR shiftCheck

    JMP keyboardEnd

unshiftedKeyboard:
    LDR acc r1 ; Acc holds the ascii code now

    AND $00FF
    
    LDR r1 acc

    ; We now have the key in the second byte meaning it is ready to be returned

    PUSH r1 ; Push the ascii key
    PUSH r1 ; Push a duplicate
    JSR shiftCheck

    JMP keyboardEnd

keyboardEnd:
    POP r1 ; Grab the ascii key

    POP r0 ; Grab the return address
    PUSH r1 ; Push the ascii key
    PUSH r0 ; Push the return address

    LDM acc KeyboardPointer
    ADD $0001
    STM acc KeyboardPointer

    RSR

keyboardFinish:
    POP r0 ; Grab the return address
    PUSH $0000 ; Push the ascii key
    PUSH r0 ; Push the return address

    RSR

shiftCheck:
    POP r0
    POP r1
    PUSH r0

    LDR acc $00DB
    SUB r1

    JNE acc shiftFalse

    ; This is shift true:

    LDM acc ShiftFlag
    NOT
    STM acc ShiftFlag ; Flip the shift flag

    RSR

shiftFalse:
    RSR

KeyboardMap: ; This map will work where the first byte is the shifted character and the second byte is hte unshifted character. If the key doesn't have an ascii character it will just return $0000
.word $1B1B ; ESC
.word $C0C0 ; F1 Since F command characters don't have an ascii I am just using C0 to mean F1
.word $C1C1 ; F2
.word $C2C2 ; F3
.word $C3C3 ; F4
.word $C4C4 ; F5
.word $C5C5 ; F6
.word $C6C6 ; F7
.word $C7C7 ; F8
.word $C8C8 ; F9
.word $C9C9 ; F10
.word $CACA ; F11
.word $CBCB ; F12
.word $CCCC ; Print Screen
.word $CDCD ; Scroll Lock
.word $CECE ; Pause
.word $CFCF ; Insert
.word $D0D0 ; Home
.word $D1D1 ; Page Up
.word $7F7F ; Delete
.word $D3D3 ; End
.word $D4D4 ; Page Down
.word $D5D5 ; Num Lock
.word $D6D6 ; Left
.word $D7D7 ; Right
.word $D8D8 ; Up
.word $D9D9 ; Down

; These next characters have shifts attached so the format will be: Unshifted Character | Shifted Character
.word $AC60 ; ` | ¬
.word $2131 ; 1 | !
.word $2232 ; 2 | "
.word $A333 ; 3 | £
.word $2434 ; 4 | $
.word $2535 ; 5 | %
.word $5E36 ; 6 | ^
.word $2637 ; 7 | &
.word $2A38 ; 8 | *
.word $2839 ; 9 | (
.word $2930 ; 0 | )
.word $5F2D ; - | _
.word $2B3D ; = | +

.word $0808 ; Backspace
.word $0909 ; Tab

.word $4161 ; a | A
.word $4262 ; b | B
.word $4363 ; c | C
.word $4464 ; d | D
.word $4565 ; e | E
.word $4666 ; f | F
.word $4767 ; g | G
.word $4868 ; h | H 
.word $4969 ; i | I
.word $4A6A ; j | J
.word $4B6B ; k | K
.word $4C6C ; l | L
.word $4D6D ; m | M
.word $4E6E ; n | N
.word $4F6F ; o | O
.word $5070 ; p | P
.word $5171 ; q | Q
.word $5272 ; r | R
.word $5373 ; s | S
.word $5474 ; t | T
.word $5575 ; u | U
.word $5676 ; v | V
.word $5777 ; w | W
.word $5878 ; x | X
.word $5979 ; y | Y
.word $5A7A ; z | Z
.word $7B5B ; [ | { 
.word $7D5D ; ] | }

.word $DADA ; Caps Lock
.word $DBDB ; Shift
.word $0A0A ; Enter
.word $DDDD ; Control
.word $DEDE ; Left Windows
.word $DFDF ; Right Shift
.word $E0E0 ; Alt
.word $2020 ; Space
.word $E1E1 ; Menu
.word $E2E2 ; Right Control

.word $3A3B ; ; | :
.word $4027 ; ' | @
.word $7E23 ; # | ~
.word $7C5C ; \ | |
.word $3C2C ; , | <
.word $3E2E ; . | >
.word $3F2F ; / | ?

.word $2A2A ; *
.word $2B2B ; +
.word $2E2E ; .

Message:
.zstring "Hello, World!\n"
commandFail:
.zstring "This is not a recognised command!\n"
NewLine:
.zstring "> "


debug:
    PUSH r0
    PUSH r1

    PUSH "@"
    JSR outChar

    POP r1
    POP r0

    RSR