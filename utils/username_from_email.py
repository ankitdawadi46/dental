def get_username_from_email(email):
    if '@' in email:
        return email.split('@')[0]
    raise ValueError("Invalid email address")