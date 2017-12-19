import json
import time

def file_to_json(filename):
    try:
        file = open(filename, 'r')
        contents = str(file.read())
        posts = json.loads(contents)
        file.close()
        return posts
    except FileNotFoundError:
        print("No such file: " + filename)
        exit(1)

def format_phonenumber(phonenumber):
    formatted_number = ""
    for digit in phonenumber:
        if digit.isdigit():
            formatted_number += digit

    if len(formatted_number) == 10:
        formatted_number = "1" + formatted_number
    elif len(formatted_number) != 11:
        return "Invalid Number"
    return formatted_number

def formated_delay(delay):
    formatted_delay = ""
    for digit in delay:
        if digit.isdigit():
            formatted_delay += digit

    if len(formatted_delay) < 1:
        return "Invalid Digit"
    return formatted_delay

def json_to_file(json_obj, filename):
    try:
        file = open(filename, 'w')
        json.dump(json_obj, file, sort_keys=True, indent=4, separators=(',', ': '))
        file.close()
    except FileNotFoundError:
        print("No such file: " + filename)
        exit(1)

def date_sent():
    """
    The time the messsage is sent.
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def update_history(delay, phonenumber, digits_pressed):
    """
    Updates history json file.
    """
    filename = "mysite/call_history.json"

    call_history = file_to_json(filename)

    history_string = "Date: " + date_sent() + "| Delay: " + str(delay) + "| Phone Number: " + phonenumber + "| Number Entered: " + digits_pressed

    call_history['history'].append([history_string, str(digits_pressed), phonenumber])

    json_to_file(call_history, filename)



