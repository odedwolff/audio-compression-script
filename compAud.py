from pydub import AudioSegment
from pydub.utils import mediainfo
import os
import time 
import datetime

outputFolder = "./output";
outBitRate = "12k"


supported_files = ["wav", "wma", "ogg", "flac"]

#files that are either smaller or have already low bitrate are copied to eh destination folder as they, with no compression
# min_size_byte = 100000
# min_BitRate = 20000

min_size_byte = 4
min_BitRate = 2






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
	startTime = time.time()
	t = time.localtime()
	current_time = time.strftime("start script %H:%M:%S", t)
	print(current_time)
	
	if not os.path.exists(outputFolder):
			os.makedirs(outputFolder)
	compDir(outputFolder, "./")
	
	runTimeSec =  time.time() - startTime
	print('COMPLETE, run time %s' % (datetime.timedelta(seconds=runTimeSec)))
		

def convertFile(srcFilePath, outputFolderRoot):
	dotRIndex = srcFilePath.rfind(".")
	fileExt=srcFilePath[dotRIndex + 1:]
	if not fileExt in supported_files:
		print("file format " + fileExt + " not supported")
		return None 
	print("handling file " + srcFilePath )
	prefix=srcFilePath.replace(" ", "_")[0:dotRIndex]
	fSize = mediainfo(srcFilePath)['size']
	fBRrate = mediainfo(srcFilePath)['bit_rate']
	print('---> prefix:%s, fileExt:%s, bit rate:%s, size:%s' % (prefix,fileExt,fBRrate,fSize))
	sysCommand = None
	
	if float(fSize) < min_size_byte or float(fBRrate) < min_BitRate:
		print('file size:%f TH SIZE %f file bRate%f TH BRATE%f' % (float(fSize), min_size_byte, float(fBRrate), min_BitRate))
		print('file is size or bit rate is bellow threshold, copying to destination folder as is')
		relPath = pathFromRunDir(srcFilePath)
		sysCommand = ('copy \"%s\" \"%s\" ' % (srcFilePath, outputFolder + relPath))
		
	else:
		#ffmpeg -i wma_src.wma -b 12k  output.mp3
		sysCommand = ('ffmpeg -i "%s" -loglevel %s -b:a %s %s' % (srcFilePath, "warning", outBitRate, outputFolder + prefix[1:] + ".mp3"))
	print ("sysCommand=" + sysCommand)
	os.system(sysCommand )

def pathFromRunDir(path):
 #strips from the path  ...\folder\sub_fdler\file.ext the file.ext partition
	if not path:
		print ('invalid path %s' % (path))
	idx = path.rfind("\\")
	if idx < 1 :
		return ""
	out = path[0:idx]
	print('stripped path: %s' % (out))
	return out
	
def testConvertTםWma():
	
	print(mediainfo("wav_src.wav")['size'])
	
convertTreeToMp3()
# testConvertTםWma()