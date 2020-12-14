from pydub import AudioSegment
import os

outputFolder = "./output";


supported_files = ["wav"]

#    script makes a compressed MP3 version of current folder tree. the output will be placed under a local output folder. if the source has subfolder (on any 
#    depth) the folders sub tree will copied, rooted udner the traget folder. each folder in the target tree will contain output files for files 
#	 in coresponding input foldeer 
#

def compDir(outputRoot, pathFromInputRoot):
	
	for entry in os.scandir( pathFromInputRoot):
		if entry.is_file() and entry.path.endswith(".wav"):
			AudioSegment.from_wav(entry.path).export(outputFolder + pathFromInputRoot + entry.path[:-4] + ".mp3", format="mp3")
		else:
			if entry.is_dir() and entry.path != outputFolder:
				newFolderPath = outputRoot + entry.path
				os.makedirs(newFolderPath)
				compDir(outputRoot, entry.path)



def convertTreeToMp3():
	if not os.path.exists(outputFolder):
			os.makedirs(outputFolder)
	compDir(outputFolder, "./")
		
#convertAllWavToMp3s(.)

convertTreeToMp3()