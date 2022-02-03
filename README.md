## Mp3 metadata populator app 

### Introduction 
This app does what you think it does. Mark important parts of the audio's file name and the metadata will be generated for you.
It is a quick side project so it has its bugs 

### Technologies
* Python 3.8
* [eyed3 0.9.6](https://pypi.org/project/eyed3/)

### Setup
To run this project, place it in your music folder, and run ```$python3 manager.py```. For some music apps, generated '.jpg' covers might not work. You would then have to update them with another application (simple load and save with [Mp3tag](https://www.mp3tag.de/en/) might work).

### Quick tutorial
Almost everything you do, you do by changing the file name.
The first way to do it, is to place the metadata inside the curly brackets {}.
You define the field, and the corresponding metadata will be generated.<br />
For example:
```
{-a Nikolay $1 -c Chopin -d 2015 -i lugansky_chopin -b $c by $a} Lugansky Chopin Piano Concerto No. 1 in E minor.mp3
```
will output the .mp3 file with the following metadata fields.
* Artist: Nikolai Lugansky
* Composer: Chopin
* Release date: 2015
* Front cover: Covers/lugansky_chopin.jpg
* Album: Chopin by Nikolai Lugansky<br />

$1 stands for the first word in the file name.<br />
Note that the order of the fields matters for some are generated using others.<br />
Additionally there are the default values for each field, so that they are generated despite you not providing their values. They are defined in the Manager/MetaFile class and can be changed easily.<br />
The second way to populate the fields is to place the $[] marks just before the corresponding words.<br />
For example:
```
$b2 $a Lugansky $c Chopin $t- Piano Concerto No. 1 $ in E minor $i lugansky_chopin.mp3
```
will output:
* Artist: Lugansky
* Composer: Chopin
* Album: Lugansky Chopin
* Title: Piano Concerto No. 1
* Front cover: Covers/lugansky_chopin.jpg  <br />
The $b2 says that the next 2 words are for the album. $c is an equivalent for $c1. $t- means that the title is the words until the next $ character.<br />
Additionally there is the name replacing functionality that maps the provided name-values to known artists or composers defined in the Manager/NameReplacer.py file. For example Bach would be changed to Johann Sebastian Bach.

### TODO
The planned functionalities are:
* Expanding the command line arguments from 0 to more than 0. (ex. giving different default values)
* Trimming the videos