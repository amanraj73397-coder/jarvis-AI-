from database import create_user, verify_user


def signup_user(email, password):
    if not email or not password:
        return False, "Email aur password dono required hain."

    if len(password) < 6:
        return False, "Password kam se kam 6 characters ka hona chahiye."

    success = create_user(email, password)

    if not success:
        return False, "Ye email pehle se registered hai."

    return True, "Account successfully create ho gaya."


def login_user(email, password):
    if not email or not password:
        return False, "Email aur password dono required hain."

    if verify_user(email, password):
        return True, "Login successful."

    return False, "Email ya password galat hai."
