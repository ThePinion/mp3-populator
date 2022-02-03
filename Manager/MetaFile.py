import eyed3
from functools import partial
from Manager.NameReplacer import NameReplacer
from Manager.Parser import name_parse

class MetaFile:
    def __init__(self, file_name:str, defaults: dict= None) -> None:
        self.file: eyed3.core.AudioFile = eyed3.load(file_name)
        assert self.file
        self.file_name = file_name
        self.name, self.parameters = name_parse(file_name)
        self.defaults = defaults

    def setters_and_getters(self) -> dict:
        """Returns the corresponding lambda function used to:
            a) Set the field's value to the first (and only) argument
            b) Get the field's value if the first argument is None
        """
        gs = self.field_get_set
        return {
            'a': partial(gs, 'artist'),
            't': partial(gs, 'title'),
            'c': partial(gs, 'composer'),
            'g': partial(gs, 'genre'),
            'b': partial(gs, 'album'),
            'd': partial(gs, 'release_date'),
            'A': partial(gs, 'album_artist'),
            'i': partial(self.save_cover, 3),
            'ia': partial(self.save_cover, 8),
        }

    def getters(self) -> dict:
        """Returns the corresponding lambda function used to:
            Get the field's value
        """
        setters_and_getters = self.setters_and_getters()
        ga = NameReplacer.generate_abreviation
        tag = self.file.tag
        temp = {
            'ln': partial(self.get_less_name),
            'aa': partial(ga, str(tag.artist), NameReplacer.abreviated),
            'ca': partial(ga, str(tag.composer), NameReplacer.abreviated),
            'as': partial(ga, str(tag.artist), NameReplacer.surname),
            'cs': partial(ga, str(tag.composer), NameReplacer.surname),
            'app_author': partial(ga, 'Szymon Wojtulewicz', NameReplacer.full_name),
        }
        setters_and_getters.update(temp)
        return setters_and_getters

    def get_defaults(self): # -> dict
        """Returns the lambdas for the default values of the fields based on other fields or the name"""
        out = {
            'c': ['$a'],
            'a': ['unknown'],
            't': ['$ca $ln by $aa'],
            'g': ['Classical'],
            'b': ['$cs by $as'],
            'A': ['$a'],
            'i': ['$b', '$aa', '$as', '$ca', '$cs', '$g'],
            'ia': ['$aa', '$as'],
        }
        if self.defaults:
            out.update(self.defaults)
        return {
            key: [partial(self.setters_and_getters()[key], self.process_value(str(value))) for value in list] 
            for key, list in out.items()
        }


    def field_get_set(self, field_name: str, value = None):
        if value != None:
            setattr(self.file.tag, field_name, value.strip())
            self.save()
            return None
        else: 
            return str(getattr(self.file.tag, field_name))

    def save_cover(self, mode: int, picture_name: str = None):
        # self.save()
        if picture_name == None:
            return ''
        picture_name = picture_name.strip()
        if picture_name.find('.jpg') < 0:
            picture_name += '.jpg'
        picture_name = 'Covers/' + picture_name
        #print(picture_name)
        img = open(picture_name, 'rb').read()
        self.file.tag.images.set(type_=mode, img_data=img, mime_type='image/jpg', description='thumbnail')
        # audio = MP3(self.file_name, ID3=ID3)
        # try:
        #     audio.add_tags()
        # except error:
        #     pass
        # audio.tags.add(APIC(encoding=3, mime='image/jpeg',type=mode,desc=u'Cover (front)',data=open(picture_name,'rb').read()))
        # audio.save() 
        # self.load()
        return None

    def get_less_name(self):
        """Returns the name excluding the words which were used to generate fields"""
        out: str = ''
        for i, word in enumerate(self.name.split()):
            if self.parameters.find(f'${i+1} ') < 0:
                out += word.strip() + " "
        return out.strip()

    def process_value(self, val: str, replace_name: bool = False) -> str:
        val += '  '
        for key, value in self.getters().items():
            val = val.replace(f'${key} ', value()+' ')
        splitted = self.name.split()
        for i in range(len(splitted))[::-1]:
            val = val.replace(f'${i+1}', splitted[i])
        if replace_name:
            val = NameReplacer.replace(val)
        return val

    def change_metadata(self, parameters:str) -> None:
        """Updates the metadata with desired values.
            ex. {-a N.Lugansky} sets the artists name. 
            {-t $a $g} sets the title to "'ARTIST' 'GENRE'".
        """
        
        self.parameters = parameters
        #Get the commands
        commands = {o[:1].strip(): o[1:].strip() for o in parameters.split('-')[1:]}
        # For each command
        for com, val in commands.items():
            # Process its value
            # And if such field exists replace it
            if com in self.setters_and_getters():
                change_name = False
                if com == 'a' or com == 'c':
                    change_name = True
                val = self.process_value(val, change_name)
                try:
                    self.setters_and_getters()[com](val)
                except FileNotFoundError as e:
                    print(e)
                    pass
            
               
        # If the command wasn't there set the value to default
        for com, list in self.get_defaults().items(): 
            if com not in commands:
                list = self.get_defaults()[com]
                for dflt in list:
                    try:
                        dflt()
                        break
                    except FileNotFoundError as e:
                        # print(e)
                        pass
        
    def save(self) -> None:
        """Saves the file to a disk"""
        self.file.tag.save()

    def load(self) -> None:
        self.file = eyed3.load(self.file_name)

    def clear(self) -> None:
        try:
            self.file.tag.clear()
        except AttributeError:
            pass
            