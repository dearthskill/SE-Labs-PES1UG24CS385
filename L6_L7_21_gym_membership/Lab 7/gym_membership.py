import math

MAX_FIELD_LEN = 100        # longest plan code or BMI string accepted
MAX_MINUTES_LEN = 10_000   # longest workout list accepted


def parse_plan(code):
    """Parse "PLAN-MONTHS", e.g. "GOLD-12" -> ("GOLD", 12).

    PLAN must be ASCII letters and MONTHS a positive whole number.
    Returns None for any other input instead of raising.
    """
    if not isinstance(code, str) or len(code) > MAX_FIELD_LEN:
        return None
    parts = code.split('-')
    if len(parts) != 2:
        return None
    plan, months = parts[0].strip(), parts[1].strip()
    if not (plan.isascii() and plan.isalpha()):
        return None
    try:
        months = int(months)
    except ValueError:
        return None
    if months <= 0:
        return None
    return plan.upper(), months


def calculate_bmi(data):
    """Parse "WEIGHT,HEIGHT" (kg, m) and return the BMI rounded to 1 decimal.

    Both values must be finite and positive. Returns None for any other
    input, or if the result is not a finite number, instead of raising.
    """
    if not isinstance(data, str) or len(data) > MAX_FIELD_LEN:
        return None
    parts = data.split(',')
    if len(parts) != 2:
        return None
    try:
        weight, height = float(parts[0]), float(parts[1])
    except ValueError:
        return None
    if not (math.isfinite(weight) and math.isfinite(height)):
        return None
    if weight <= 0 or height <= 0:
        return None
    try:
        bmi = weight / (height ** 2)
    except (OverflowError, ZeroDivisionError):
        return None
    if not math.isfinite(bmi):
        return None
    return round(bmi, 1)


def average_workout(minutes):
    """Return the whole-number average of space-separated workout minutes.

    Every value must be a whole number >= 0 and there must be at least one.
    Returns None for any other input instead of raising.
    """
    if not isinstance(minutes, str) or len(minutes) > MAX_MINUTES_LEN:
        return None
    tokens = minutes.split()
    if not tokens:
        return None
    values = []
    for token in tokens:
        try:
            value = int(token)
        except ValueError:
            return None
        if value < 0:
            return None
        values.append(value)
    return sum(values) // len(values)


def show(label, result):
    if result is None:
        print(label, "Invalid input")
    else:
        print(label, result)


def main():
    print("==== Running parse_plan ====")
    user_input = input("Enter a plan code (e.g. GOLD-12): ")
    show("Plan and Months:", parse_plan(user_input))

    print("\n==== Running calculate_bmi ====")
    user_input = input("Enter weight and height (e.g. 70,1.75): ")
    show("BMI:", calculate_bmi(user_input))

    print("\n==== Running average_workout ====")
    user_input = input("Enter workout minutes separated by spaces (e.g. 45 60 30): ")
    show("Average Minutes:", average_workout(user_input))


if __name__ == "__main__":
    main()
