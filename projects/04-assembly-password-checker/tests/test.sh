#!/usr/bin/env bash
set -euo pipefail

binary="./password_checker"
output="$(mktemp)"
trap 'rm -f "$output"' EXIT

run_case() {
  local input="$1"
  local expected_status="$2"
  local expected_text="$3"
  local actual_status=0
  printf '%s\n' "$input" | "$binary" >"$output" || actual_status=$?
  if [[ "$actual_status" -ne "$expected_status" ]]; then
    echo "Expected exit status $expected_status, got $actual_status for test input." >&2
    cat "$output" >&2
    exit 1
  fi
  if [[ -n "$expected_text" ]] && ! grep -Fq "$expected_text" "$output"; then
    echo "Expected output not found: $expected_text" >&2
    cat "$output" >&2
    exit 1
  fi
}

run_case 'StrongPass123!' 0 '[PASS]'
run_case 'abcdefghijk1!' 1 'uppercase letter'
run_case 'ABCDEF123456' 1 'lowercase letter'
run_case 'short' 1 'Minimum length'
run_case '' 2 'Empty input'

echo "5 assembly policy checks passed."
