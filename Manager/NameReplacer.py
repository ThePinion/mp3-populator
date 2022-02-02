import difflib

SIMILARITY_THRESHOLD = 0.7
known_artists = [
    'Nikolay Lugansky', 'Gregory Sokolov', 'Kamil Pacholec', 
    'Bruce Xiao Liu', 'Ray Chen', 'Emil Gilels'
]
known_composers = [
    'Dmitri Shostakovich', 'Fryderyk Chopin', 'Felix Mendelssohn',
    'Sergei Rachmaninoff', 'Antonín Dvořák', 'Johann Sebastian Bach',
    'Ludwig Beethoven', 'Itzhak Perlman'
]
known_people = known_artists + known_composers + [
     
]

class NameReplacer:
    artists_surnames = []
    initials = 1
    surname = 2
    full_name = 3
    abreviated = 4


    def similar(seq1: str, seq2: str) -> float:
        return difflib.SequenceMatcher(a=seq1.lower(), b=seq2.lower()).ratio()
        

    def generate_abreviation(person: str, mode: int) -> str:
        """Generates the abreviation using initials.
            mode: abreviated
            ex. Johann Sebastian Bach -> J.S.Bach
        """
        out_name = ''
        if mode == NameReplacer.initials:
            for word in person.split():
                if len(word) > 0:
                    out_name += word[0] + '.'
            out_name = out_name[:-1]

        elif mode == NameReplacer.surname:
            out_name = person.split()[-1]
            #print(out_name)

        elif mode == NameReplacer.full_name:
            out_name = person

        elif mode == NameReplacer.abreviated:
            for word in person.split()[:-1]: 
                if len(word) > 0:
                    out_name += word[0] + '.'
            out_name += person.split()[-1]

        return out_name


    def replace(in_name: str, mode: int = None) -> str:
        """Genrates the name in a standarized form. Given the given string is similar enough.
            ex. Rachmaninov -> S.Rachmaninoff
        """
        if not mode:
            mode = NameReplacer.full_name
        max_value = -1
        out_name = in_name
        for person in known_people:
            mutations = [person, person.split()[-1], person[0]+'.'+person.split()[-1]]
            for mutation in mutations:
                temp = NameReplacer.similar(mutation, in_name)
                if temp > SIMILARITY_THRESHOLD and temp > max_value:
                    out_name = person
                    max_value = temp
        return out_name