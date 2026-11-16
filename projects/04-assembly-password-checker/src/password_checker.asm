; Educational password policy checker - NASM x86-64 Linux
; Reconstructed reference implementation, not the original university source.
%define SYS_read 0
%define SYS_write 1
%define SYS_exit 60
%define STDIN 0
%define STDOUT 1
%define MAX_INPUT 256

section .data
prompt db "Enter a dummy password to check: "
prompt_len equ $-prompt
warning db "Do not enter a real password; terminal echo is enabled.",10
warning_len equ $-warning
short_msg db "[FAIL] Minimum length is 12 characters.",10
short_len equ $-short_msg
upper_msg db "[FAIL] Add an uppercase letter.",10
upper_len equ $-upper_msg
lower_msg db "[FAIL] Add a lowercase letter.",10
lower_len equ $-lower_msg
digit_msg db "[FAIL] Add a digit.",10
digit_len equ $-digit_msg
special_msg db "[FAIL] Add a non-alphanumeric character.",10
special_len equ $-special_msg
pass_msg db "[PASS] Configured policy satisfied.",10
pass_len equ $-pass_msg
empty_msg db "[ERROR] Empty input.",10
empty_len equ $-empty_msg

section .bss
input resb MAX_INPUT
input_len resq 1
upper resb 1
lower resb 1
digit resb 1
special resb 1

section .text
global _start
_start:
    mov rax,SYS_write
    mov rdi,STDOUT
    mov rsi,prompt
    mov rdx,prompt_len
    syscall
    mov rax,SYS_write
    mov rdi,STDOUT
    mov rsi,warning
    mov rdx,warning_len
    syscall
    mov rax,SYS_read
    mov rdi,STDIN
    mov rsi,input
    mov rdx,MAX_INPUT
    syscall
    test rax,rax
    jle .empty
    mov [input_len],rax
    mov rcx,rax
    dec rcx
    cmp byte [input+rcx],10
    jne .cr
    dec qword [input_len]
.cr:
    mov rcx,[input_len]
    test rcx,rcx
    jz .empty
    dec rcx
    cmp byte [input+rcx],13
    jne .init
    dec qword [input_len]
.init:
    mov byte [upper],0
    mov byte [lower],0
    mov byte [digit],0
    mov byte [special],0
    xor rcx,rcx
.scan:
    cmp rcx,[input_len]
    jae .report
    mov al,[input+rcx]
    cmp al,'A'
    jb .lower_check
    cmp al,'Z'
    ja .lower_check
    mov byte [upper],1
.lower_check:
    cmp al,'a'
    jb .digit_check
    cmp al,'z'
    ja .digit_check
    mov byte [lower],1
.digit_check:
    cmp al,'0'
    jb .special_check
    cmp al,'9'
    ja .special_check
    mov byte [digit],1
.special_check:
    cmp al,'A'
    jb .mark_special
    cmp al,'Z'
    jbe .next
    cmp al,'a'
    jb .mark_special
    cmp al,'z'
    jbe .next
    cmp al,'0'
    jb .mark_special
    cmp al,'9'
    jbe .next
.mark_special:
    mov byte [special],1
.next:
    inc rcx
    jmp .scan
.report:
    xor r12,r12
    cmp qword [input_len],12
    jae .check_upper
    mov rsi,short_msg
    mov rdx,short_len
    call print
    inc r12
.check_upper:
    cmp byte [upper],1
    je .check_lower
    mov rsi,upper_msg
    mov rdx,upper_len
    call print
    inc r12
.check_lower:
    cmp byte [lower],1
    je .check_digit
    mov rsi,lower_msg
    mov rdx,lower_len
    call print
    inc r12
.check_digit:
    cmp byte [digit],1
    je .check_special
    mov rsi,digit_msg
    mov rdx,digit_len
    call print
    inc r12
.check_special:
    cmp byte [special],1
    je .finish
    mov rsi,special_msg
    mov rdx,special_len
    call print
    inc r12
.finish:
    test r12,r12
    jnz .failed
    mov rsi,pass_msg
    mov rdx,pass_len
    call print
    xor rdi,rdi
    jmp .exit
.failed:
    mov rdi,1
    jmp .exit
.empty:
    mov rsi,empty_msg
    mov rdx,empty_len
    call print
    mov rdi,2
.exit:
    mov rax,SYS_exit
    syscall
print:
    mov rax,SYS_write
    mov rdi,STDOUT
    syscall
    ret
