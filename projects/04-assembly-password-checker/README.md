# Assembly Password Policy Checker

A command-line password-policy evaluation exercise implemented with NASM on x86-64 Linux.

## Features

- Checks minimum length of 12 characters
- Detects uppercase and lowercase ASCII letters
- Detects numeric and non-alphanumeric characters
- Reports failed checks and program exit status

The program evaluates policy rules on input strings; it is not an account authentication or password storage system.

## Build and run

```bash
nasm -f elf64 src/password_checker.asm -o password_checker.o
ld password_checker.o -o password_checker
./password_checker
```

Use sample input rather than real credentials.

## Tests

The GitHub Actions workflow assembles and links the program and runs five policy smoke tests for accepted and rejected inputs. Test cases are in `tests/test.sh`.
