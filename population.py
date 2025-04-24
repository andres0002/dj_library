import os 
import time
import django, random as rd
from random import random
from apps.book.models import Author

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_library.settings")

django.setup()

vocals = ['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U']
consonants = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', 'g', 'G', 'h', 'H',
                'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q',
                'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z'
            ]

def generate_string(length):
    if (length <= 0):
        return False

    random_string = ''

    for i in range(length):
        desition = rd.choice(('vocals', 'consonants'))

        if (random_string[-1:].lower() in vocals):
            desition = 'consonants'
        elif (random_string[-1:].lower() in consonants):
            desition = 'vocals'
        
        if (desition == 'vocals'):
            character = rd.choice(vocals)
        elif (desition == 'consonants'):
            character = rd.choice(consonants)

        random_string += character
    return random_string

def generate_number():
    return int(random()*10+1)

def generate_author(count):
    for i in range(count):
        random_name = generate_string(generate_number())
        random_last_name = generate_string(generate_number())
        random_nationality = generate_string(generate_number())
        random_description = generate_string(generate_number())

        Author.objects.create(
            name = random_name,
            lastname = random_last_name,
            nationality = random_nationality,
            description = random_description
        )

if (__name__ == "__main__"):
    num = int(input("Enter the number of authors you want to add: "))
    print("Loading....")
    start = time.strftime('%c')
    print(f'Start date and time of authors creation: {start}')
    generate_author(num)
    end = time.strftime('%c')
    print(f'End date and time of authors creation: {end}')