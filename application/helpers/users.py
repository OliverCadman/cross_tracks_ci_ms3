from datetime import date

def calculate_user_age(date_of_birth):
    today = date.today()
    return today.year - date_of_birth[0] - ((today.month, today.day) < (date_of_birth[1], date_of_birth[2]))