from pydub import AudioSegment
from pydub.utils import mediainfo
import os

outputFolder = "./output";
outBitRate = "12k"


supported_files = ["wav", "wma", "ogg", "flac"]

#files that are either smaller or have already low bitrate are copied to eh destination folder as they, with no compression
min_size_byte = 100000
min_BitRate = 20000




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
	print("converting file " + srcFilePath )
	prefix=srcFilePath.replace(" ", "_")[0:dotRIndex]
	print("prefix =" + prefix)
	print("fileExt =" + fileExt)
	print("bit rate=" + mediainfo(srcFilePath)['bit_rate'])
	print("size=" + mediainfo(srcFilePath)['size'])
	#ffmpeg -i wma_src.wma -b 12k  output.mp3
	sysCommand = "ffmpeg -i \"" +srcFilePath + "\" -b " + outBitRate + " " + outputFolder + prefix[1:] + ".mp3"
	print ("sysCommand=" + sysCommand)
	os.system(sysCommand )
	
	
def testConvertTםWma():
	#buf = AudioSegment.from_file("wma_src.wma", "wma")
	#buf = AudioSegment.from_file("wav_src.wav", "wav")
	#ffmpeg -i audio.ogg -acodec libmp3lame audio.mp3
	print(mediainfo("wav_src.wav")['size'])
	
convertTreeToMp3()
# testConvertTםWma()