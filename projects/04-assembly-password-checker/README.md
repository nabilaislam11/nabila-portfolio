# Password Checking tool using Assembly language for secure authentication

A NASM x86-64 Linux reference program inspired by the academic project title **Password Checking Tool using Assembly Language for Secure Authentication**.

## Implemented policy checks
- Minimum length of 12 characters
- Uppercase ASCII letter
- Lowercase ASCII letter
- Numeric digit
- Non-alphanumeric ASCII character
- Per-rule failure messages and process exit statuses

## Build
```bash
nasm -f elf64 src/password_checker.asm -o password_checker.o
ld password_checker.o -o password_checker
./password_checker
```

Use dummy test strings only. Terminal echo is enabled.

## Scope and provenance
This is a reconstructed reference implementation, not a verified copy of the original university source. It is a policy checker, not a complete authentication system; it does not store credentials or perform password hashing.

## Validation status
GitHub Actions successfully assembled and linked the NASM source on Ubuntu and passed 5 policy smoke tests (valid policy, missing uppercase, missing lowercase, short input, and empty input). Broader testing, terminal input hardening, and security review remain outside this educational demonstration.

## Original academic project: source and attribution

Original title documented in the pre-employment CV. No original source or submission has been verified; this directory holds a later NASM reference implementation.

This was collaborative academic work. Specific individual implementation responsibilities are pending confirmation. The implementation and tests documented in this directory describe a later independently reconstructed reference build, not a copy of the historical submission. No original group files have been imported into this repository.
