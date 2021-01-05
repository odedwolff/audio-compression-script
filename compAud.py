from pydub import AudioSegment
from pydub.utils import mediainfo
import os
import time 
import datetime

#outputFolder = "./output";
#outBitRate = "12k"


supported_files = ["wav", "wma", "ogg", "flac", "m4a"]


K = 1024 
M = K**2

#files that are either smaller or have already low bitrate are copied to the detination folder as is (are), with no compression

min_size_MB = 0.2
#kiilo bit per second (bit, not byte!) 
min_BitRate = 20 * K



#unspported files statistics by extention 
usFiilesByExt = {}
#stat of files copied unprocessed becaue they were bellow a threshold
statUnderThrsh = {
	'size':0,
	'bitRate':0
}
filesListsUThrsh = {
	'size':[],
	'bitRate':[]
}


#true for copying unspported files to target as is, false skip 
cfg_copyUnspported = True




#    script makes a compressed MP3 version of current folder tree. the output will be placed under a local output folder. if the source has subfolder (on any 
#    depth) the folders sub tree will copied, rooted udner the traget folder. each folder in the target tree will contain output files for files 
#	 in coresponding input foldeer 
#



#at entering this function, both input and out put folder are assumed to exist, thus, if there are sub directories at the input tree, we first create the corresponding 
#output folder and only then call in recursion 
def compDir(inputRoot, outputRoot, relPath, targetBitRate):
	print("entering compDir(inputRoot=%s, outputRoot=%s, relPath=%s, targetBitRate=%s)" % (inputRoot, outputRoot, relPath, targetBitRate))
	currentInputFolder = inputRoot + relPath
	currentOutputFolder = outputRoot + relPath
	fullCurrentPath = inputRoot + relPath;
	for entry in os.scandir(currentInputFolder):
		if entry.is_file():
			convertFile(entry.path, outputRoot + relPath, targetBitRate)
		else:
			if entry.is_dir():
				#newRelPath = entry.path[len(fullCurrentPath):]
				newRelPath = entry.path[len(inputRoot) + 0:]
				newOutputFull = outputRoot + newRelPath
				os.makedirs(newOutputFull)
				compDir(inputRoot, outputRoot, newRelPath, targetBitRate)



def convertTreeToMp3(inputFolderRoot, outputFolder, targetBitRate):
	
	print("entering convertTreeToMp3()")
	print(("args=(%s, %s, %s)" % (inputFolderRoot, outputFolder, targetBitRate)))
	outBitRate = str(targetBitRate) + "k"
	startTime = time.time()
	t = time.localtime()
	current_time = time.strftime("start script %H:%M:%S", t)
	print(current_time)
	
	if not os.path.exists(outputFolder):
			#os.makedirs(outputFolder)
			print(("output folder %s doe not exist, ABORTING" % (outputFolder)))
			return 
	#compDir(inputFolder, outputFolder, "./")
	compDir(inputFolderRoot, outputFolder,"",targetBitRate)

	runTimeSec =  time.time() - startTime
	printStats(runTimeSec)


def printStats(runTimeSec):	
	print('--------COMPLETE, run time %s -----------------' % (datetime.timedelta(seconds=runTimeSec)))
	print('unsupported files stat:')
	print(usFiilesByExt)
	print('stats of files bellow thresholds:')
	print(statUnderThrsh)
	print('>>>>>>>>>files bellow size threshold (copied unprocessed):  <<<<<<<<')
	for file in filesListsUThrsh['size']:
		print (file)
	print('<<<<<<<<files bellow bitRate threshold (copied unprocessed):   >>>>>>>>>')
	for file in filesListsUThrsh['bitRate']:
		print (file)
		

def convertFile(srcFilePath, targetFolder, targetBitRate):
	isSupported = True
	dotRIndex = srcFilePath.rfind(".")
	fileExt=srcFilePath[dotRIndex + 1:]
	print("\n handling file " + srcFilePath )
	if not fileExt in supported_files:
		addExtToUnsupStat(fileExt)
		print("file format " + fileExt + " not supported")
		if cfg_copyUnspported:
			isSupported=False
			print("fopying file to target unprocessed")
		else:
			print("dropping file")
			return None
	prefix=srcFilePath.replace(" ", "_")[0:dotRIndex]
	
	
	#if size or bit Rate are not in file meta deta, mark corresponding values in -1
	if 'size' in mediainfo(srcFilePath):
		fSize = mediainfo(srcFilePath)['size']
	else:
		fSize = -1
	if 'bit_rate' in mediainfo(srcFilePath):
		fBRrate = mediainfo(srcFilePath)['bit_rate']
	else:
		fBRrate = -1
		
	print('---> prefix:%s, fileExt:%s, bit rate:%s, size:%s' % (prefix,fileExt,fBRrate,fSize))
	sysCommand = None
	
	
	print('file size MB:%1.2f M TH SIZE %1.2f M -- -file bRate:%1.2f TH BRATE:%1.2f' % ((float(fSize))/M , min_size_MB, (float(fBRrate))/K, min_BitRate/K))
	#file not supported or bellow Thresholds -> copy as is to target
	underBRate = float(fBRrate) < min_BitRate and float(fBRrate) > 0 
	underSize =  (float(fSize))/M < min_size_MB and float(fSize) > 0
	if (not isSupported ) or underBRate or  underSize:
		print('file is not supported or size or bit rate is bellow threshold, copying to destination folder as is')
		sysCommand = ('copy \"%s\" \"%s\" ' % (reverseSlashDirection(srcFilePath), reverseSlashDirection(targetFolder)))
		if isSupported:
			if underBRate:
				statUnderThrsh['bitRate'] += 1
				filesListsUThrsh['bitRate'].append(srcFilePath)
			if underSize:
				statUnderThrsh['size'] += 1
				filesListsUThrsh['size'].append(srcFilePath)
	#compress 	
	else:
		#ffmpeg -i wma_src.wma -b 12k  output.mp3
		#trim the file name from tha path
		fileName = srcFilePath[srcFilePath.rfind("\\"):]
		print("claculated file name %s" % (fileName))
		sysCommand = ('ffmpeg -i "%s" -loglevel %s  -b:a %sk "%s"' %
		(reverseSlashDirection(srcFilePath), "warning", targetBitRate, reverseSlashDirection(targetFolder + fileName + ".mp3")))
	print ("sysCommand=" + sysCommand)
	os.system(sysCommand )

def pathFromRunDir(srcFilePath, outputFolderRoot):
	print(("enterint pathFromRunDir(srcFilePath=%s, outputFolderRoot=%s)" % (srcFilePath, outputFolderRoot)))
	return "dummy\\path"


def pathFromRunDir2(path):
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

def addExtToUnsupStat(fileExt):
	print('entering addExtToUnsupStat(fileExt=%s)' % (fileExt))
	if fileExt in usFiilesByExt.keys():
		usFiilesByExt[fileExt] += 1
	else:
		usFiilesByExt[fileExt] = 1
		
def reverseSlashDirection(path):
	 return path.replace("/", '\\')


	
#convertTreeToMp3()
