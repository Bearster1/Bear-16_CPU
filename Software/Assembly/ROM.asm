KeyboardPointer     = $0000
ShiftFlag           = $0001

StackStart          = $0100
StackEnd            = $0200

PrintStackPointer   = $02FF
PrintStackStart     = $0300
PrintStackEnd       = $0400

VariablesStart      = $0500
VariablesEnd        = $0600

TermOut             = $6002
TermClock           = $6003

MemoryIn            = $6012
MemoryOut           = $6013
MemoryAddress       = $6014
MemoryClock         = $6015

KeyboardStart       = $7000
KeyboardEnd         = $7100


CommandCount        = $0004 ; This is the number of commands in the bios | This is a constant number not an address

.org $8000

; Code conventions:
; Variables, zstrings and Bitmaps are named using Pascal Case
; Subroutines are named using Camel Case
; For things where it is either True or False use $FFFF for True and $0000 for False

start:
    LDR r0 KeyboardStart
    STM r0 KeyboardPointer ; Settup the KeyboardPointer
    
    LDR r0 PrintStackStart
    STM r0 PrintStackPointer ; Settup the PrintStackPointer

    PUSH BootupMessage
    JSR printStringLine
    PUSH NewLine
    JSR printString

main:
    JSR keyboard

    JSR specialCharFix

    POP r0 ; Prevents writing of Null to the screen
    JEQ r0 main
    
    PUSH r0
    PUSH r0 ; Push duplicate
    JSR outChar

    JSR commandCheck

    JMP main

loop:
    JMP loop


commandOUT:
    PUSH Message
    JSR printStringLine

    RSR

commandSEE:
    PUSH Message2
    JSR printStringLine

    RSR

commandBEAR:
    PUSH BearStartupMessage
    JSR printStringLine

    JSR BearCode

    RSR
commandBBPL:
    PUSH BBPLStartupMessage
    JSR printStringLine

    JSR BearCode

    RSR

commandCheck:
    POP r1
    POP r0
    PUSH r1

    LDR acc r0
    SUB "\n"
    JNE acc commandCheckEscapeNonEnter

    LDR r1 Commands ; this holds the first command
    LDR r2 CommandCount ; This holds the number of commands (And therefore the number of time to loop)

commandCheckLoop:
    PUSH r1 ; Save r1
    PUSH r2 ; Save r2

    PUSH PrintStackStart
    PUSH r1
    JSR compareStrings
    POP r0

    POP r2 ; Bring r2 back
    POP r1 ; Bring r1 back

    PUSH r0 ; Save r0
    PUSH r2 ; Save r2
    PUSH r1 ; This is the current command so you can find the next command

    JSR findStringEnd

    POP acc ; Grab the end of the string
    POP r2 ; Restore r2
    POP r0 ; Restore r0

    ADD $0001 ; add 1 so it gets to the next command
    LDR r1 acc

    LDR acc r2
    SUB $0001 ; Decrement r2 (Loop index)
    LDR r2 acc

    NOT ; Not the acc
    AND r0
    JNE acc commandCheckSucceed

    JNE r2 commandCheckLoop

commandCheckFail:
    PUSH CommandFail
    JSR printStringLine

    JMP commandCheckEscape

commandCheckSucceed:
    LDR acc CommandCount ; Grab command count
    SUB r2 ; Subtract r2 to get the index of commands
    SUB $0001 ; Subtract 1 to get to the 0 based index.
    ADD CommandMap ; Add to get to the command map position
    
    LDM r0 acc ; Grab the command jump address from the input.

    JSR r0

    JMP commandCheckEscape

commandCheckEscape:
    JSR printStackReset

    PUSH NewLine
    JSR printString

    RSR

commandCheckEscapeNonEnter:
    PUSH r0

    JSR printStackPush
    RSR


printStackReset:
    LDR r0 PrintStackStart ; Use r0 as the index pointer
    STM r0 PrintStackPointer ; Re-settup the PrintStackPointer

printStackResetLoop:
    *STM r0 $0000 ; Set to 0

    LDR acc r0 ; Increment r0
    ADD $0001
    LDR r0 acc

    LDR acc PrintStackEnd ; Load end to acc
    SUB r0 ; Subtract to figure out where we are
    JNE acc printStackResetLoop ; Jump back if not at the end

    RSR

printStackBackspaceHandler:
    JSR printStackPop
    POP r0

    RSR

printStackPush:
    POP r0
    POP r1 ; This is the data to push
    PUSH r0

    LDR acc r1
    SUB $0008 ; Subtract backspace key
    JEQ acc printStackBackspaceHandler

    LDM acc PrintStackPointer
    STM r1 acc

    ADD $0001
    AND $00FF
    ADD PrintStackStart

    STM acc PrintStackPointer

    RSR

printStackPop:
    LDM acc PrintStackPointer

    SUB $0001
    AND $00FF
    ADD PrintStackStart

    STM acc PrintStackPointer

    LDM r1 acc ; Grab the data
    *STM acc $0000 ; Set data to 0

    POP r0
    PUSH r1
    PUSH r0

    RSR

printStackPrint:
    PUSH PrintStackStart
    JSR printString


lenString:
    ; This finds the length of a string and returns it
    POP r0
    POP r1 ; This is the address of the string

    LDR r2 $0000 ; This holds the amount of characters in the string
lenStringLoop:
    LDM acc r1
    JEQ acc lenStringEnd

    LDR acc r2
    ADD $0001
    LDR r2 acc

    LDR acc r1
    ADD $0001
    LDR r1 acc

    JMP lenStringLoop

lenStringEnd:
    PUSH r2
    PUSH r0 ; Returns the return address

    RSR


compareStrings:
    ; This compares two strings
    POP r0
    POP r1 ; This is the First string
    POP r2 ; This is the Second string
    PUSH r0

    PUSH r1 ; This is the First string
    PUSH r2 ; This is the Second string
    PUSH r1; Push a duplicate
    PUSH r2; Push a duplicate
    
    JSR lenString

    POP r0 ; This is the result of lenString
    POP acc ; This is the First String
    PUSH r0 ; Put lenString below First String
    PUSH acc ; Put the second string on the top to be used by the next lenString

    JSR lenString
    POP acc ; This holds the result of second lenString
    POP r0 ; This holds the result of first lenString

    SUB r0 ; Subtract the two lenStrings

    POP r1
    POP r2
    JNE acc compareStringFail

    LDR r3 $0000 ; Load r3 with 0 as the index pointer

compareStringLoop:
    LDR acc r1 ; Load first character ; Put start address into acc
    ADD r3 ; Add index pointer
    LDM r4 acc ; Load r4 with data at address acc

    LDR acc r2 ; Load second character
    ADD r3
    LDM acc acc
    
    SUB r4 ; Compare by subtraction
    JNE acc compareStringFail

    LDR acc r3 ; Increment r3
    ADD $0001
    LDR r3 acc

    SUB r0 ; Subtract r0 to see how many characters are left and jump if not zero
    JNE acc compareStringLoop

    ; If haven't gone to compareStringFail that means it is true.
compareStringSuceed:
    POP r0
    PUSH $FFFF
    PUSH r0

    RSR

compareStringFail:
    POP r0
    PUSH $0000
    PUSH r0

    RSR


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


findStringEnd:
    POP r0
    POP acc ; This is the string
    PUSH r0

findStringEndLoop:
    LDM r1 acc
    JEQ r1 findStringEndEnd

    ADD $0001

    JMP findStringEndLoop

findStringEndEnd:
    POP r0
    PUSH acc
    PUSH r0

    RSR

outChar:
    POP r0
    POP r1 ; This is the character to output
    PUSH r0

    STM r1 TermOut
    
    LDR r1 $FFFF
    STM r1 TermClock

    RSR

printStringLine:
    ; This subroutine is to print string and a new line
    LDR r2 printStringLineEnd
    JMP printStringContinue

printString:
    LDR r2 printStringEnd
printStringContinue:
    POP r0
    POP acc ; This is the address of the string to output
    PUSH r0

printStringLoop:
    LDM r1 acc ; This takes the current character and places it into r1
    JEQ r1 r2

    ADD $0001

    PUSH acc
    PUSH r1 ; this is the character to output
    JSR outChar
    POP acc

    JMP printStringLoop

printStringEnd:
    RSR
printStringLineEnd:
    PUSH "\n"
    JSR outChar
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

BootupMessage:
.zstring "Bear-BIOS"
Message:
.zstring "Hello, World!"
Message2:
.zstring "Goodbye, World!"
BearStartupMessage:
.zstring "Welcome to Bear:"
BBPLStartupMessage:
.zstring "Welcome to Basic Bear Programming Language:"
CommandFail:
.zstring "This is not a recognised command!"
NewLine:
.zstring "> "

Commands: ; These are the command strings
.zstring "OUT"
.zstring "SEE"
.zstring "BEAR"
.zstring "BBPL"

CommandMap: ; These are the command jump addresses
.word commandOUT
.word commandSEE
.word commandBEAR
.word commandBBPL

BearCode:
    ; Place the assembly code generated from the Bear Compiler here:
BearCodeMain:
  push 5
  push 0
  push 1
  JSR fibbonachi
  pop r0
.word $FF00
  
  RSR

fibbonachi:
  pop r0
  pop r1
  STM r1 $0503
  pop r1
  STM r1 $0502
  pop r1
  STM r1 $0501
  push r0
  
  LDM r1 $0500
  push r1
loop0Start:
  pop r1
  JEQ r1 loop0End
  push r1
  
  LDM r1 $0502
  push r1
  
  pop r1
  STM r1 $0503
  
  LDM r1 $0501
  push r1
  LDM r1 $0502
  push r1

  pop r1
  pop acc
  ADD r1
  push acc
  
  pop r1
  STM r1 $0502
  
  LDM r1 $0503
  push r1
  
  pop r1
  STM r1 $0501
  
  pop acc
  SUB 1
  push acc
  JMP loop0Start

loop0End:
  LDM r1 $0501
  pop r0
  push r1
  push r0
  
  RSR

BBPLCode:
    ; Place the code generated from the BBPL compiler here:
BBPLMain:
    LDR acc 5
    PUSH acc
    LDR acc 0
    PUSH acc
    LDR acc 2
    PUSH acc
    JSR fibbonachi
    POP r0

.word $FF00
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