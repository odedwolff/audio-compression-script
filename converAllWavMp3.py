from pydub import AudioSegment
import os

outputFolder = "output";

def convertAllWavToMp3s():
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)
	for entry in os.scandir('./'):
		if entry.path.endswith(".wav") and entry.is_file():
			print('converting ' + entry.path)
			AudioSegment.from_wav(entry.path).export(outputFolder + entry.path[:-4] + ".mp3", format="mp3")
			
			
		
convertAllWavToMp3s();