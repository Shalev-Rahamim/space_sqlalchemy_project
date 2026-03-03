from datetime import datetime


def get_non_empty_input(prompt_text):
    while True:
        user_input = input(prompt_text).strip()
        if user_input:
            return user_input
        print("❌ Error: Input cannot be empty. Please try again.")


def get_valid_int(prompt_text, min_val=0):
    while True:
        user_input = input(prompt_text).strip()
        try:
            value = int(user_input)
            if value < min_val:
                print(f"❌ Error: Value must be at least {min_val}.")
            else:
                return value
        except ValueError:
            print("❌ Error: Input must be a valid number.")


def get_optional_input(prompt_text):
    user_input = input(prompt_text).strip()
    return user_input if user_input else None


def get_valid_date(prompt_text):
    user_input = input(prompt_text).strip()
    if not user_input:
        return datetime.utcnow()

    try:
        return datetime.strptime(user_input, "%Y-%m-%d")
    except ValueError:
        print("⚠️ Invalid format (YYYY-MM-DD). Using today's date instead.")
        return datetime.utcnow()
