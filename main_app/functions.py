def validate_password(password):
    if len(password) < 8:
        return None
    if password.lower() == password:
        return None
    if password.upper() == password:
        return None
    for char in password:
        if char.isdigit():
            break
    else:
        return None
    for char in password:
        if not char.isalnum():
            break
    else:
        return None
    return password
