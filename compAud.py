from pydub import AudioSegment
import os

outputFolder = "./output";


supported_files = ["wav", "wma", "m4a"]

#    script makes a compressed MP3 version of current folder tree. the output will be placed under a local output folder. if the source has subfolder (on any 
#    depth) the folders sub tree will copied, rooted udner the traget folder. each folder in the target tree will contain output files for files 
#	 in coresponding input foldeer 
#

def compDir(outputRoot, pathFromInputRoot):
	for entry in os.scandir( pathFromInputRoot):
		if entry.is_file():
			convertFile(entry.path, outputFolder)
					
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


def convertFile(srcFilePath, outputFolderRoot):
	"""
	fileExt=srcFilePath[-3:]
	if not fileExt in supported_files:
		print("file format " + fileExt + " not supported")
		return None 
	prefix=srcFilePath.replace(" ", "_")[0:-4]
	print("prefix =" + prefix)
	buf = AudioSegment.from_file(srcFilePath, fileExt)
	buf.export(outputFolder + prefix + ".mp3", format="mp3");
	
	"""
	dotRIndex = srcFilePath.rfind(".")
	fileExt=srcFilePath[dotRIndex + 1:]
	if not fileExt in supported_files:
		print("file format " + fileExt + " not supported")
		return None 
	prefix=srcFilePath.replace(" ", "_")[0:dotRIndex]
	print("prefix =" + prefix)
	buf = AudioSegment.from_file(srcFilePath, fileExt)
	buf.export(outputFolder + prefix + ".mp3", format="mp3");
	
	

convertTreeToMp3()