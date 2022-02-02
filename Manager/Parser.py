from typing import Tuple

def name_parse(file_name: str) -> Tuple[str, str]:
        start, end = (file_name.find("{"), file_name.find("}"))
        if start >= 0 and end >= start:
            name = file_name[:start] + file_name[end+1:]
            parameters = file_name[start+1: end]
        else:
            name = file_name
            parameters = ""

        #Strpi the strings
        parameters = parameters.strip() + ' '
        name = name.replace('.mp3', '').strip()
        counter: int = 0
        out = ' '

        #Parse the in-name parameters
        till_next: bool = False
        in_name_parameters = ' '
        for word in name.split():
            if len(word) == 0:
                continue
            #Check if it is a paramiter
            if word[0] == '$':
                word = word[1:]
                # We will be adding the words till the next parameter
                if word[-1] == '-':
                    word = word[:-1]
                    repeat = 0
                    till_next = True
                # Otherwise specify length
                else:
                    try:
                        first_digit = [x.isdigit() for x in word].index(True)
                        repeat = int(word[first_digit:])
                        word = word[:first_digit]
                    except ValueError:
                        repeat = 1
                    till_next = False

                # Add The parameter to the parameters
                if len(word) > 0:
                    in_name_parameters += '-' + word + ' '
                    for i in range(repeat):
                        in_name_parameters +=  f'${counter + 1 + i} '
            else:
                counter += 1
                out += word + ' '
                if till_next:
                    in_name_parameters += f'${counter} '

        #In-name parameters go in first so that they can be referrenced later by non-in-name params
        parameters = in_name_parameters + parameters

        #print(parameters)
        return (out, parameters)