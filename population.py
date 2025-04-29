# py
import os
import time
from random import randint as rd_randint, choice as rd_choice
# django
import django
# third

# 1. configurar DJANGO_SETTINGS_MODULE.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_library.settings.dev")

# 2. ejecutar django.setup().
# para poder utilizar el orm de django.
django.setup() # simula instalación de django de forma externa, para poder acceder a toda la info.

# 3. ahora ya puedes importar modelos de Django.
# django -> own
from apps.book.models import Author

vocals = ('a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U')
consonants = (
    'b', 'B', 'c', 'C', 'd', 'D', 'f', 'F', 'g', 'G', 'h', 'H',
    'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'p', 'P', 'q', 'Q',
    'r', 'R', 's', 'S', 't', 'T', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z'
)

def generate_string(length):
    if (length <= 0):
        return False

    random_string = ''

    for i in range(length):
        # seleciona un character consonants aleatoriamente, si coincide que el ultimo character added es vocal.
        if (random_string[-1:].lower() in vocals):
            character = rd_choice(consonants)
        # seleciona un character vocals aleatoriamente, si coincide que el ultimo character added es consonant.
        elif (random_string[-1:].lower() in consonants):
            character = rd_choice(vocals)
        # concatena las tuplas (vocals, consonants) y seleciona un character aleatoriamente entre vocals and consonants.
        else:
            character = rd_choice(vocals+consonants)

        # concatena el character.
        random_string += character
    return random_string

def generate_number():
    # num aleatorio entre 1 y 10.
    return rd_randint(1, 10)

def generate_author(count):
    authors_list = [] # para return.
    for i in range(count):
        random_name = generate_string(generate_number())
        random_last_name = generate_string(generate_number())
        random_nationality = generate_string(generate_number())
        random_description = generate_string(generate_number())

        # Author.objects.create( # para poblar la db.
        #     name = random_name,
        #     lastname = random_last_name,
        #     nationality = random_nationality,
        #     description = random_description
        # )
        author = Author ( # para return.
            name = random_name,
            lastname = random_last_name,
            nationality = random_nationality,
            description = random_description
        )
        authors_list.append(author) # para return.
    return authors_list

def show_authors(authors_list):
    for author in authors_list:
        print(f'name: {author.name}, lastname: {author.lastname}, nationality: {author.nationality}, description: {author.description}.')

if (__name__ == "__main__"):
    num = int(input("Enter the number of authors you want to add: "))
    print("Loading....")
    start = time.strftime('%c') # para validar que db es mas eficiente, al momento de cargar data.
    print(f'Start date and time of authors creation: {start}')
    # generate_author(num) # para poblar la db.
    show_authors(generate_author(num)) # para el return.
    end = time.strftime('%c') # para validar que db es mas eficiente, al momento de cargar data.
    print(f'End date and time of authors creation: {end}')
    print("Loaded....")
    
    # gestores de bds -> recomendable hacer test en pvs dedicados para dbs.
    # sqlite -> para creation de project (dev, test), poca data.
    # mysql -> para creation de project (qas, prd), mas data.
    # postgresql -> para creation de project (qas, prd), mas data.