#!/usr/bin/env bash
# Deterministic tests for Scenario 16 — Hangman Challenge.
# Usage: bash run_tests.sh   (run from the project folder)
# random.choice is patched from the command line; game code is not modified.

cd "$(dirname "$0")" || exit 1
export PYTHONIOENCODING=utf-8
PASS=0
FAIL=0
OUT=""

# play WORDS INPUT
#   WORDS: comma-separated secret words returned by random.choice, in round order.
#   INPUT: keystrokes, one per line (printf %b escapes).
play() {
    OUT=$(printf '%b' "$2" | python3 -c '
import sys, game
words = iter(sys.argv[1].split(","))
game.random.choice = lambda options: next(words)
game.HangmanGame().run()
' "$1" 2>&1)
}

ok()  { PASS=$((PASS + 1)); echo "  PASS: $1"; }
bad() { FAIL=$((FAIL + 1)); echo "  FAIL: $1"; }

# Output contains TEXT.
has() { grep -qF -- "$1" <<<"$OUT" && ok "has \"$1\"" || bad "missing \"$1\""; }
# Output does not contain TEXT.
lacks() { grep -qF -- "$1" <<<"$OUT" && bad "unexpected \"$1\"" || ok "no \"$1\""; }
# TEXT appears on exactly N lines.
count() {
    local n
    n=$(grep -cF -- "$2" <<<"$OUT")
    [ "$n" -eq "$1" ] && ok "\"$2\" x$1" || bad "\"$2\" expected x$1, got x$n"
}

PY="p\ny\nt\nh\no\nn\n"          # solves "python"
GR="g\nr\na\nv\ni\nt\ny\n"       # solves "gravity"

echo "1. Repeated incorrect guesses"
# Expect: first z costs one life; two repeats say "already tried", lives stay 5/6.
play python "technology\nnormal\nz\nz\nz\n/quit\n"
count 1 "Wrong: 'z' is not in the word."
count 2 "You already tried 'z'. No life lost."
has   "Lives: 5/6"
lacks "Lives: 4/6"

echo "2. Repeated correct guesses"
# Expect: p accepted once, repeats rejected, no life lost, status shown twice only.
play python "technology\nnormal\np\np\np\n/quit\n"
count 1 "Correct: 'p' is in the word."
count 2 "You already tried 'p'. No life lost."
count 2 "Lives: 6/6"
lacks "Lives: 5/6"

echo "3. Hints"
# Expect: hint shown once with -4 penalty (normal x2); second /hint refused;
# win gives (5 + 1 - 2) x 2 = 8.
play python "technology\nnormal\n/hint\n/hint\n${PY}n\n"
count 1 "Hint (-4 points if solved): A programming language named after a snake."
count 1 "Hint already used this round."
has   "Solved: python (+8 points)"
has   "Rounds played: 1  Won: 1  Best streak: 1  Final score: 8"

echo "4. Category changes and category preservation"
# Expect: unknown category re-asks; science chosen once then kept by Enter;
# scores 12 + 14 + 16 = 42.
play python,gravity,gravity "sports\ntechnology\n\n${PY}y\nscience\n\n${GR}y\n\n\n${GR}n\n"
has   "Unknown category 'sports'."
count 1 "New round: technology, normal (6 lives)."
count 2 "New round: science, normal (6 lives)."
count 2 "Solved: gravity"
has   "Rounds played: 3  Won: 3  Best streak: 3  Final score: 42"

echo "5. Difficulty changes (no state leakage)"
# Expect: unknown difficulty re-asks; easy 8 lives (one lost to z), then hard
# starts fresh at 4/4, normal at 6/6; scores 6 + 21 + 16 = 43.
play python,python,python "technology\nextreme\neasy\nz\n${PY}y\n\nhard\n${PY}y\n\nnormal\n${PY}n\n"
has   "Unknown difficulty 'extreme'."
has   "New round: technology, easy (8 lives)."
has   "Lives: 7/8"
has   "New round: technology, hard (4 lives)."
has   "Lives: 4/4  Score: 6  Streak: 1  Difficulty: hard"
has   "New round: technology, normal (6 lives)."
has   "Solved: python (+6 points)"
has   "Solved: python (+21 points)"
has   "Solved: python (+16 points)"
has   "Final score: 43"

echo "6. Multiple rounds and streak reset"
# Expect: win, win, loss (streak -> 0), win; best streak stays 2;
# scores 12 + 14 + 0 + 12 = 38.
play python,python,gravity,python "technology\nnormal\n${PY}y\n\n\n${PY}y\nscience\n\nb\nc\nd\ne\nf\nh\ny\ntechnology\n\n${PY}n\n"
has   "Out of lives. The word was: gravity"
has   "Lives: 6/6  Score: 26  Streak: 0  Difficulty: normal"
count 3 "Solved: python"
has   "Rounds played: 4  Won: 3  Best streak: 2  Final score: 38"

echo "7. Invalid input"
# Expect: blank, 'ab', '7', 'é' rejected with no life lost; unknown command
# reported; '  P  ' normalised to p; bad y/n answer re-asked.
play python "technology\nnormal\n\nab\n7\né\n/foo\n  P  \ny\nt\nh\no\nn\nmaybe\nn\n"
count 4 "Enter a single letter a-z."
count 1 "Unknown command '/foo'. Use /hint or /quit."
has   "Correct: 'p' is in the word."
count 1 "Please answer y or n."
lacks "Lives: 5/6"
has   "Rounds played: 1  Won: 1  Best streak: 1"

echo "8a. Quit at category prompt (q)"
# Expect: summary with zero rounds, no traceback.
play python "q\n"
has   "Rounds played: 0  Won: 0  Best streak: 0  Final score: 0"
lacks "Traceback"

echo "8b. Quit at difficulty prompt (/quit)"
play python "technology\n/quit\n"
lacks "New round"
has   "Rounds played: 0"

echo "8c. /quit mid-round after one completed round"
# Expect: abandoned round not counted; first win still in summary.
play python,python "technology\nnormal\n${PY}y\n\n\nz\n/quit\n"
has   "Round abandoned; it is not counted in the statistics."
has   "Rounds played: 1  Won: 1  Best streak: 1  Final score: 12"

echo "8d. End of input mid-round (EOF)"
# Expect: clean exit with summary, no traceback.
play python "technology\nnormal\na\n"
has   "Round abandoned"
has   "Session summary"
lacks "Traceback"

echo "9a. Boundary: lose on last life (hard)"
# Expect: lives 4 -> 1, repeat on 1 life is free, 4th distinct wrong ends round;
# lives never shown as 0.
play python "technology\nhard\na\nb\nc\nc\nd\nn\n"
has   "Lives: 1/4"
count 1 "You already tried 'c'. No life lost."
has   "Out of lives. The word was: python"
lacks "Lives: 0"
has   "Rounds played: 1  Won: 0  Best streak: 0  Final score: 0"

echo "9b. Boundary: win on last life (hard)"
# Expect: solve with 1/4 lives left; (5 + 1) x 3 = 18.
play python "technology\nhard\na\nb\nc\n${PY}n\n"
has   "Lives: 1/4"
has   "Solved: python (+18 points)"

echo "9c. Boundary: hint on a lost round at score 0"
# Expect: score stays 0 (penalty only reduces a win's reward), never negative.
play python "technology\nhard\n/hint\na\nb\nc\nd\nn\n"
has   "Hint (-6 points if solved)"
has   "Final score: 0"
lacks "Final score: -"

echo
echo "Passed: $PASS  Failed: $FAIL"
[ "$FAIL" -eq 0 ]
