import logging
logging.getLogger().setLevel(logging.ERROR)

import os
from pydub import AudioSegment
from threading import Thread
from multiprocessing import Process

from Manager.MetaFile import MetaFile

    
def single_file(file_name: str):
    if file_name.find('.mp3') < 0:
        return
       
    file = MetaFile(file_name)
    # file.clear()
    file.change_metadata(file.parameters)
    file.save()
    print(file.file.tag.title)


def main(): 
    # for each file in the directory
    print()
    for file_name in os.listdir():
        Thread(target=single_file, args=[file_name]).start()
        #single_file(file_name)
        # print(file_name)
        # print(file.parameters)
        # print()
        # for var in file.file.tag.__dict__:
        #     print(var)
        
        # # If the file is to be trimmed
        # splited = file_name.split("!trim")
        # if len(splited)>1:
        #     # Load the frames
        #     sound = AudioSegment.from_mp3(file_name)
        #     # Remove the old file 
        #     os.remove(file_name)
        #     # Remove the trimming command
        #     file_name = splited[1].strip()
        #     # Trim the sound
        #     duration = int(float(splited[0])*1000)
        #     sound = sound[duration:]
        #     # Export the trimmed audio
        #     sound.export(file_name, format='mp3')
        # # Change the metadata based on the filename
       
        # change_metadata(file_name)
        
        
        
if __name__ == '__main__':
    main()