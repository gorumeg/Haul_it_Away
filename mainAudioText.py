from pickle import TRUE
import speech_recognition as sr
import os 
from xmlrpc.client import DateTime
import pyaudio
import wave
from datetime import datetime
import os
import time
from scipy.io import wavfile
import threading
from SocialDistancingAnalyzer.main import video
from Vrecorder import recordVideo
import geocoder
def distress(data):
    flag1 = keyword(data)
    return flag1

    # put frequency and amplitude here
def freq(path):
    log = []
    while (start < 4500):
        start =0
        end = start + 10
        sr, data = wavfile.read(path)
        sp = int(sr * start / 1000)
        ep = int(sr * end / 1000)
        l = 10 / 1000
        c = 0
        for i in range(sp, ep):
            if data[i] < 0 and data[i + 1] > 0:
                c += 1
        log.append( int(c / l))
        start+= 100
def keyword(data):
    proxy=["Help","help","bachao","Bachao","Stop"]
    for i in data:
        if(i in proxy):
            return True
    return False

   
def spreadsheet(data):

    from sheetfu import SpreadsheetApp

    

    sa = SpreadsheetApp('newkey.json')
    spreadsheet = sa.open_by_id('1t60CvJSHba-j9ZGHFIIWmA5i4n25Fn82E7Xhox6L3oU')
    sheet = spreadsheet.get_sheet_by_name('Sheet1')
    range = sheet.get_data_range() 
    print(range.coordinates.number_of_rows)
    s = ','.join(data)
    from datetime import datetime

# datetime object containing current date and time
    now = datetime.now()
    
   

    # dd/mm/YY H:M:S
    t = now.strftime("%d/%m/%Y %H:%M:%S")

    g =list( geocoder.ip('me'))
    data = [[t,s,g]]

    data_range = sheet.get_range(row=range.coordinates.number_of_rows+1,column=1,number_of_row=len(data), number_of_column=len(data[0]))
    try:
        data_range.set_values(data) 
    except:
        print("ERROR")

def makeWordsFromLogs(logs):
    listOfWords = []
    for phrase in logs:
        for words in phrase.split():
            listOfWords.append(words.capitalize())
    return listOfWords

def recordAudio():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 5
    filename = str(datetime.now().date())+ '-'+ str(datetime.now().time()).replace(':', '-')+".wav"
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    print(f'Recording file {filename}')
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []  # Initialize array to store frames
    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    path = "C:\\Users\\samri\\OneDrive\\Desktop\\object\\RecordedMedia\\"+filename
    # Save the recorded data as a WAV file
    wf = wave.open(path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f'Finished recording {filename}')


def getTextFromAudio():
    r = sr.Recognizer()
    directory  = "C:\\Users\\samri\\OneDrive\\Desktop\\object\\RecordedMedia"
    log = []
    for filename in os.listdir(directory):
        print(f"getting text from {filename}")
        audioFile = os.path.join(directory, filename)
        with sr.AudioFile(audioFile) as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio)
            log.append(text)
            print(text)
        except Exception as e:
            print(f"couldnt find anything  in {filename}")
    return log
    


def deleteLastLogs(folderPath):
    for file in os.listdir(folderPath):
        os.remove(folderPath+'\\'+file)

def convertAudioToText(noOfTimes, clearPreviousLogs = True):
    for i in range(noOfTimes):
        recordAudio()
    print(makeWordsFromLogs(getTextFromAudio()))
    data = makeWordsFromLogs(getTextFromAudio())
    print(data)
    if(distress(data) ):

        s=recordVideo()
        print(s)
        if(video(r"C:\Users\samri\OneDrive\Desktop\object\RecordedVideo\1.avi")):
            spreadsheet(data)
    # if(clearPreviousLogs):
        # deleteLastLogs("C:\\Users\\samri\\OneDrive\\Desktop\\object\\RecordedMedia")

convertAudioToText(1)



        
