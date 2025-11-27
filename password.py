import re

def check_password_strength(password):
    strength = 0
    suggestions = []

    # Check length
    if len(password) >= 8:
        strength += 1
    else:
        suggestions.append("Use at least 8 characters.")

    # Check for lowercase letters
    if re.search(r"[a-z]", password):
        strength += 1
    else:
        suggestions.append("Add lowercase letters (a-z).")

    # Check for uppercase letters
    if re.search(r"[A-Z]", password):
        strength += 1
    else:
        suggestions.append("Add uppercase letters (A-Z).")

    # Check for digits
    if re.search(r"[0-9]", password):
        strength += 1
    else:
        suggestions.append("Add digits (0-9).")

    # Check for special characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        strength += 1
    else:
        suggestions.append("Add special characters (!@#$%^&* etc.).")

    # Final result
    if strength == 5:
        return "Strong password ✅", []
    elif strength >= 3:
        return "Moderate password ⚠️", suggestions
    else:
        return "Weak password ❌", suggestions

# Input from user
user_password = input("Enter your password: ")
strength_result, suggestion_list = check_password_strength(user_password)

print("\nPassword Strength:", strength_result)
if suggestion_list:
    print("Suggestions to improve your password:")
    for suggestion in suggestion_list:
        print("- " + suggestion)
