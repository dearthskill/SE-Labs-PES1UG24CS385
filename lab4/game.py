import random
import string
from words import WORDS, HINTS
from stats import SessionStats

# Round rules for each difficulty: starting lives and score multiplier.
DIFFICULTIES = {
    "easy": {"lives": 8, "multiplier": 1},
    "normal": {"lives": 6, "multiplier": 2},
    "hard": {"lives": 4, "multiplier": 3},
}
BASE_POINTS = 5
HINT_PENALTY = 2
MENU_QUIT = {"q", "/quit"}


class HangmanGame:
    def __init__(self):
        # Session state: carried across every round of the run.
        self.score = 0
        self.streak = 0
        self.stats = SessionStats()
        self.category = "technology"
        self.difficulty = "normal"
        # Round state: reset by start_round().
        self.secret = ""
        self.guessed = set()
        self.wrong = set()
        self.lives = DIFFICULTIES[self.difficulty]["lives"]
        self.hint_used = False

    def start_round(self):
        self.secret = random.choice(WORDS[self.category])
        self.guessed.clear()
        self.wrong.clear()
        self.lives = DIFFICULTIES[self.difficulty]["lives"]
        self.hint_used = False

    def masked(self):
        return " ".join(ch if ch in self.guessed else "_" for ch in self.secret)

    def won(self):
        return all(ch in self.guessed for ch in set(self.secret))

    def guess(self, letter):
        if len(letter) != 1 or letter not in string.ascii_lowercase:
            return "Invalid input: enter a single letter a-z."
        if letter in self.guessed or letter in self.wrong:
            return f"You already tried '{letter}'. Nothing changed."
        if letter in self.secret:
            self.guessed.add(letter)
            return f"Correct: '{letter}' is in the word."
        self.wrong.add(letter)
        self.lives -= 1
        return f"Wrong: '{letter}' is not in the word. You lose 1 life."

    def use_hint(self):
        if self.hint_used:
            return None
        self.hint_used = True
        return HINTS.get(self.secret, "No hint available.")

    def hint_cost(self):
        return HINT_PENALTY * DIFFICULTIES[self.difficulty]["multiplier"]

    def round_points(self):
        # Called after a win, once the streak includes this round.
        multiplier = DIFFICULTIES[self.difficulty]["multiplier"]
        points = (BASE_POINTS + self.streak) * multiplier
        if self.hint_used:
            points -= self.hint_cost()
        return points

    def finish_round(self, won):
        """Apply the result of a completed round to session state."""
        points = 0
        if won:
            self.streak += 1
            points = self.round_points()
            self.score += points
        else:
            self.streak = 0
        self.stats.record(won, self.streak)
        return points

    def ask(self, prompt):
        """Read one normalised line; None means input ended (treated as quit)."""
        try:
            return input(prompt).strip().lower()
        except EOFError:
            print()
            return None

    def play_round(self):
        """Play one round. Returns False if the player quit mid-round."""
        self.start_round()
        max_lives = DIFFICULTIES[self.difficulty]["lives"]
        while self.lives > 0 and not self.won():
            print("\nWord:", self.masked())
            print("Wrong:", " ".join(sorted(self.wrong)) or "-")
            print(f"Lives: {self.lives}/{max_lives}  Score: {self.score}  "
                  f"Streak: {self.streak}  [{self.category}, {self.difficulty}]")
            raw = self.ask("Letter, /hint, or /quit: ")
            if raw is None or raw == "/quit":
                print("Round abandoned. The word was:", self.secret)
                return False
            if raw == "/hint":
                hint = self.use_hint()
                if hint is None:
                    print("Hint already used this round. Nothing changed.")
                else:
                    print(f"Hint (costs {self.hint_cost()} points if you win): {hint}")
                continue
            if raw.startswith("/"):
                print(f"Unknown command '{raw}'. Use /hint or /quit.")
                continue
            print(self.guess(raw))

        won = self.won()
        old_streak = self.streak
        points = self.finish_round(won)
        if won:
            print(f"Solved: {self.secret} (+{points} points)")
        else:
            print("Out of lives. The word was:", self.secret)
            if old_streak:
                print(f"Streak of {old_streak} reset to 0.")
        return True

    def choose_option(self, label, options, current):
        """Prompt until a valid option is chosen. Enter keeps the current one.
        Returns None if the player quits."""
        while True:
            raw = self.ask(f"Choose {label} [Enter = {current}] or q: ")
            if raw is None or raw in MENU_QUIT:
                return None
            if raw == "":
                return current
            if raw in options:
                return raw
            print(f"Unknown {label} '{raw}'. Choose from: {', '.join(options)}.")

    def ask_yes_no(self, prompt):
        while True:
            raw = self.ask(prompt)
            if raw is None or raw in ("n", "no"):
                return False
            if raw in ("y", "yes"):
                return True
            print("Please answer y or n.")

    def print_summary(self):
        s = self.stats
        print("\n=== Session summary ===")
        print(f"Final score: {self.score}  Current streak: {self.streak}")
        print(f"Rounds played: {s.rounds}  Rounds won: {s.wins}  Best streak: {s.best_streak}")

    def run(self):
        print("Hangman Challenge")
        print("A session consists of multiple rounds.")
        while True:
            print("\nCategories:", ", ".join(WORDS))
            category = self.choose_option("category", list(WORDS), self.category)
            if category is None:
                break
            self.category = category
            print("Difficulties:", ", ".join(
                f"{name} ({rule['lives']} lives, x{rule['multiplier']} points)"
                for name, rule in DIFFICULTIES.items()))
            difficulty = self.choose_option("difficulty", list(DIFFICULTIES), self.difficulty)
            if difficulty is None:
                break
            self.difficulty = difficulty
            if not self.play_round():
                break
            if not self.ask_yes_no("Another round? [y/n]: "):
                break
        self.print_summary()
