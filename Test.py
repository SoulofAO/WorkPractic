import re


def check_email(email):
    # Регулярное выражение для проверки почтового адреса
    pattern = r'^[\w\.-]+@[a-zA-Z\d-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern, email):
        return True
    else:
        return False


# Пример использования
email1 = "example@example.com"
email2 = "invalid_email.com"

if check_email(email1):
    print(f"{email1} - почтовый адрес валиден")
else:
    print(f"{email1} - почтовый адрес невалиден")

if check_email(email2):
    print(f"{email2} - почтовый адрес валиден")
else:
    print(f"{email2} - почтовый адрес невалиден")