# Manual test plan

Use dummy strings only. Never use a real account password.

| Scenario | Example | Expected |
|---|---|---|
| All rules satisfied | CampusDemo#2026A | PASS |
| Too short | Ab1!short | Length failure |
| Missing uppercase | campusdemo#2026 | Uppercase failure |
| Missing lowercase | CAMPUSDEMO#2026 | Lowercase failure |
| Missing digit | CampusDemo#Strong | Digit failure |
| Missing special | CampusDemo2026A | Special failure |
| Empty | Press Enter | Empty-input error |

Assembly and runtime tests remain pending until NASM is available.
