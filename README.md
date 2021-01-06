A script for converting a folder tree with arbitrary structure containing audio files 
to a similarly structured tree in which corresponding files are compressed.
motivation behind this is achieving susbstential reduction in library size while compromising
quality

the script was developed and tested on a window platform. 

use like:

>convertTreeToMp3(path_source_root , path_target_root, bitRate) 

for isntance 

>convertTreeToMp3("C:/temp/recording ideas", "C:/temp/recording ideas out", 20) 

in this case i am using an output bit rate of 20, which to my experience roughly equals a value 
that is just recognizable enough to be useful, that is, size reduction prioritized 
just 