import random
from .words import words
import json

data = words

def randomword():
    random_word = random.choice(data)
    return random_word

# make word mask function - Mathstronauts library
def wordmask(word):
    #TODO: allow user to specify number of mask letters
    a = random.randint(0, len(word)-1)
    b = random.randint(0, len(word)-1)
    while(a==b):
        b = random.randint(0, len(word)-1)
    wordmask = ""
    for i in range(len(word)):
        if i == a or i == b:
            wordmask += "_"
        else:
            wordmask += word[i]
    return wordmask


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

from datetime import *

# convert all dictionary items to string
def dict_str(dictionary):
    keys_values = dictionary.items()
    new_dict = {
        str(key): str(value) for key, value in keys_values
    }
    return new_dict

# convert from epoch to standard time
def convert_time(time):
    standard_time = datetime.fromtimestamp(time)
    return standard_time

def time_format(time_var):
    int_type = isinstance(time_var, int)
    if int_type == True:  # if the variable is in epoch time, it will be read as an integer and needs to be converted
        time_standard = datetime.fromtimestamp(time_var)
    else:  # else the variable is already in standard time
        time_standard = time_var

    hour = time_standard.strftime('%I')
    minute = time_standard.strftime('%M')
    period = time_standard.strftime('%p')

    combine_time = f"{hour}:{minute} {period}"
    return combine_time

def date_format(date_var):
    int_type = isinstance(date_var, int)
    if int_type == True:  # if the variable is in epoch time, it will be read as an integer and needs to be converted
        date_standard = datetime.fromtimestamp(date_var)
    else:  # else the variable is already in standard time
        date_standard = date_var

    date = date_standard.strftime('%x')
    return date

