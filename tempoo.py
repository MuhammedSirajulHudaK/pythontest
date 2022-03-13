import datetime
import os
from PIL import Image
import glob
import subprocess as sp
import sys
import numpy
from pydub import AudioSegment
import math
from pydub.utils import mediainfo
import scipy
from scipy.io.wavfile import write
from scipy.io.wavfile import read
from scipy.io import wavfile
import numpy as np


def single_split(from_min, to_min, file,num):
    #AudioSegment.from_file(r"C:\Users\MSHK\Downloads\WhatsApp Ptt 2020-12-17 at 7.00.06 PM.ogg", format="ogg")
    #wav_audio.export("audio1111.mp3", format="mp3")
    t1 = from_min* 1000
    t2 = to_min * 1000
    if num != 1:
        bismi = "int.wav"
    else:
        bismi = "bismi.mp3"
    snd = AudioSegment.from_file(bismi)
    snd = snd.set_frame_rate(44100)
    snd.export("newint.wav", format="wav")
    AudioSegment.from_file(file)[t1:t2].set_frame_rate(44100).export("final.wav", format="wav")

    
    
    fs, a = wavfile.read('newint.wav')
    fs, b = wavfile.read('final.wav')
    #b =(b>>16).astype(np.int16)
    c = scipy.vstack((a,b))
    write("temp.wav", 44100, c.astype(np.int16))
    #audiolab.wavwrite(c, 'file3.wav', fs, enc)

    #split_audio = snd + AudioSegment.from_file(file)[t1:t2]
    #split_audio.export("temp.wav", format="wav")
    return a,b,c

def findFfmpeg():
    
    if sys.platform == "win32":
      return "ffmpeg.exe"
    else:
      try:
        with open(os.devnull, "w") as f:
          sp.check_call(['ffmpeg', '-version'], stdout=f, stderr=f)
        return "ffmpeg"
      except:
        return "avconv"
    FFMPEG_BIN = findFfmpeg()

    encoders = sp.check_output(self.core.FFMPEG_BIN + " -encoders -hide_banner", shell=True)
    if b'libfdk_aac' in encoders:
      acodec = 'libfdk_aac'
    else:
      acodec = 'ac3'

def readAudioFile(filename,FFMPEG_BIN):
    
    command = [FFMPEG_BIN,
          '-i', filename,
          '-f', 's16le',
          '-acodec', 'pcm_s16le',
          '-ar', '44100', # ouput will have 44100 Hz
          '-ac', '1', # mono (set to '2' for stereo)
          '-']
    in_pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.DEVNULL, bufsize=10**8)

    completeAudioArray = numpy.empty(0, dtype="int16")

    while True:
      # read 2 seconds of audio
      raw_audio = in_pipe.stdout.read(88200*4)
      if len(raw_audio) == 0:
        break
      audio_array = numpy.fromstring(raw_audio, dtype="int16")
      completeAudioArray = numpy.append(completeAudioArray, audio_array)
      # print(audio_array)

    in_pipe.kill()
    in_pipe.wait()

    # add 0s the end
    completeAudioArrayCopy = numpy.zeros(len(completeAudioArray) + 44100, dtype="int16")
    completeAudioArrayCopy[:len(completeAudioArray)] = completeAudioArray
    completeAudioArray = completeAudioArrayCopy

    return completeAudioArray



def drawBars(image,image1,bgI,results1,frame):
    if frame == 1:
        
        width, height = image1.size

        
        depth = width*9/16
        
        im = Image.new("RGB", (width-width%2, int(depth)-int(depth)%2), "black")
        
        #width = width-width%2
        #depth = int(depth)-int(depth)%2
        #left = 0
        #top = max(results1[0][1],min(results1[-1][1]-int(depth),(bgI-int(depth)/2)))  #max((bgI-int(depth)/2),0)
        #right = width
        
        #bottom = min(results1[-1][1],max((results1[0][1]+int(depth)),int(depth)/2+bgI))
        #if bottom > height:
         #   top = height- int(depth)#bgI
          #  bottom = height
        #if >(bgI-int(depth)/2):
         #   top = 0
          #  bottom = int(depth)
        # Cropped image of above dimension
        # (It will not change orginal image)
        #print((left, top, right, bottom))
        #image = image.crop((left, top, right, bottom))
        #im1.show()
        image = image.resize((width-width%2, int(depth)-int(depth)%2))
        im.paste(image, (0, 0))


    else:        
        width, height = image1.size
       
        
        depth = width*9/16
        
        im = Image.new("RGB", (width-width%2, int(depth)-int(depth)%2), "black")

        
        width = width-width%2
        depth = int(depth)-int(depth)%2
        left = 0
        top = max(results1[0][1],min(results1[-1][1]-int(depth),(bgI-int(depth)/2)))  #max((bgI-int(depth)/2),0)
        right = width
        
        bottom = min(results1[-1][1],max((results1[0][1]+int(depth)),int(depth)/2+bgI))


        
        #print(top, bottom)
      
        #if bottom > height:
         #   top = height- int(depth)#bgI
          #  bottom = height
        #if >(bgI-int(depth)/2):
         #   top = 0
          #  bottom = int(depth)
        # Cropped image of above dimension
        # (It will not change orginal image)
        #print((left, top, right, bottom))
        image = image.crop((left, top, right, bottom))
        #im1.show()
        im.paste(image, (0, 0))

    
    return im

if __name__ == "__main__":


    #####################################
    # inputs
    #####################################
    
   
    now = datetime.datetime.now().strftime("%d%m%Y%H%M")
    inputFile = "current.wav"
    outputFile = now+".mp4"

    #results = ['0:00', '0:34', '1:11', '1:51', '2:20', '3:02', '3:20', '3:46', '4:04', '4:28', '5:14', '5:46', '6:12', '6:46', '7:14', '7:55', '8:25', '8:44', '9:03', '10:24', '12:01', '13:48', '15:00', '16:46', '18:39', '19:31', '21:07', '22:17', '23:17', '24:43', '25:48', '26:18']
    #results1 = [[835, 540], [453, 956], [410, 1239], [413, 1522], [433, 1686], [430, 1970], [423, 2051], [397, 2246], [411, 2429], [414, 2609], [417, 2977], [381, 3160], [430, 3345], [395, 3613], [460, 3800], [406, 4076], [400, 4258], [405, 4427], [402, 4615], [458, 5344], [475, 5994], [411, 6741], [424, 7368], [431, 8009], [459, 8918], [435, 9280], [368, 9948], [363, 10470], [437, 10938], [491, 11390], [394, 11753], [547, 11986]]
    #results = ['0:39', '1:02', '1:31', '2:08', '2:45', '3:19', '3:40', '4:01', '4:14', '4:24', '4:37', '5:02', '5:19', '5:47', '6:05', '6:34', '6:59', '7:20', '7:34', '7:53', '8:16', '8:38', '8:57', '9:23', '9:48', '10:13', '10:50', '11:23', '12:01', '13:15']
    #results1 = [[826, 181], [432, 592], [428, 872], [401, 1247], [400, 1516], [426, 1873], [387, 1964], [419, 2240], [435, 2431], [395, 2520], [415, 2707], [442, 2975], [382, 3162], [377, 3438], [385, 3614], [377, 3984], [379, 4255], [406, 4441], [372, 4616], [400, 4811], [381, 5085], [404, 5354], [359, 5538], [396, 5901], [436, 6175], [415, 6449], [401, 6809], [430, 7092], [426, 7371], [406, 8049]]
    



    if True:
        num = int(input("Repeat No: "))
        results = input("Audio time: ")
        results1 = input("Slide time: ")
        audo = results
        slido = results1
        results = results.split(",")
        results3 = results1.split(" ")
        results1 = []
        for i in results3:
            results1.append([0,int(i)])
        
        
        print("Updated")
        print(results)
        print(results1)

    with open("tracklist.txt", "a", encoding="utf-8") as myfile:
        myfile.write("Audio time : "+audo)
        myfile.write("Slide time : "+slido)


    #results = ['0:19', '0:46', '1:27', '2:03', '2:27', '3:00', '3:49', '4:39', '5:40', '6:41', '7:34', '8:11', '8:35', '9:42']
    #results1 = [[0, 0], [0, 401], [0, 770], [0, 1051], [0, 1241], [0, 1509], [0, 1965], [0, 2430], [0, 2871], [0, 3424], [0, 3796], [0, 4154], [0, 4344], [0, 4939]]
    #results = ['0:00', '0:20', '0:49', '1:01', '1:22', '1:52', '2:13', '2:37', '2:58', '3:22', '3:53', '4:08', '4:21', '4:38', '4:45', '5:12', '5:34', '6:08', '6:25', '6:40', '6:50', '7:20', '7:49', '8:12', '8:31', '8:55', '9:15', '9:38', '9:59', '10:27']
    #results1= [[793, 3], [440, 413], [439, 675], [432, 778], [425, 956], [394, 1240], [433, 1427], [425, 1603], [431, 1786], [420, 1964], [410, 2236], [406, 2430], [448, 2612], [423, 2786], [430, 2886], [463, 3150], [417, 3425], [410, 3809], [393, 3981], [438, 4072], [403, 4165], [414, 4439], [404, 4707], [454, 4896], [404, 5075], [387, 5254], [424, 5439], [403, 5619], [398, 5808], [497, 6127]]
   

    #results =['0:00', '0:24', '0:58', '1:29', '1:57', '2:19', '3:02', '3:51', '5:02', '5:50', '6:30', '6:57']
    #results1 = [[815, 175], [431, 599], [411, 1046], [386, 1414], [409, 1691], [438, 1962], [404, 2427], [425, 2976], [414, 3704], [400, 4258], [437, 4798], [575, 5124]]



        
    for item in range(len(results)):
        if len(results[item])==4:
            results[item] = '0:0'+results[item]
        elif len(results[item])==5:
            results[item] = '0:'+results[item]
        else:
            results[item] = str(int(results[item][:3])//60)+":"+str(int(results[item][:3])%60)+':'+results[item][-2:]
            
    results2 = [(int(results[i][:1])*60*60*0.01+int(results[i][2:4])*60*0.01+int(results[i][-2:])*0.01) for i in range(len(results))]
    a,b,c = single_split(results2[0]*100, results2[-1]*100, inputFile,num)
    

    print(results2)
    
    inputFile = 'temp.wav'
    
    #results1 = [[1058, 463], [924, 687], [818, 1076]]
    #results2 = [0.12, 0.22, 0.32]
    results3= []
    for j in range(len(results2)-1):
        slides = int((results2[j+1]-results2[j])/0.001)
        #print(slides)
        results3.append((results1[j+1][1]-results1[j][1])/slides)
        #print((results1[j+1][1]-results1[j][1]))




    FFMPEG_BIN = findFfmpeg()

    #print(results2[0], results2[-1])
    #single_split(results2[0], results2[-1], inputFile)
    # test if user has libfdk_aac
    encoders = sp.check_output(FFMPEG_BIN + " -encoders -hide_banner", shell=True)
    if b'libfdk_aac' in encoders:
      acodec = 'libfdk_aac'
    else:
      acodec = 'ac3'
    image = Image.open("tempo.png")#+filelist[bgI])
    subimage = Image.open("logo1.png")
    width, height = image.size
    subwidth, subheight = subimage.size
    depth = width*9/16
    width = width-width%2
    depth = int(depth)-int(depth)%2
    subwidth = subwidth-subwidth%2
    subheight = int(subheight)-int(subheight)%2
    value = str(width-width%2)+"x"+str(int(depth))


########################################## for audio repeating
    fs, h = wavfile.read('temp.wav')
    #fs, b = wavfile.read('final.wav')
    w  = h


    for volv in range(num-1):
        w = scipy.vstack((h,w))
    write("jembo.wav", 44100, w.astype(np.int16))
    inputFile1 = "jembo.wav"
    
    ffmpegCommand = [FFMPEG_BIN,
       '-y', # (optional) means overwrite the output file if it already exists.
       '-f', 'rawvideo',
       '-vcodec', 'rawvideo',
       '-s', value, # size of one frame
       '-pix_fmt', 'rgb24',
       '-r', '20', #'30' default frames per second this can be 10 20 then sample size 4410 or 2105 etc like that
       '-i', '-', # The input comes from a pipe
       '-an',
       '-i', inputFile1,
       '-acodec', acodec, # output audio codec
       '-b:a', "192k",
       '-vcodec', "libx264",
       '-pix_fmt', "yuv420p",
       '-preset', "medium",
       '-f', "mp4"]

    if acodec == 'aac':
      ffmpegCommand.append('-strict')
      ffmpegCommand.append('-2')

    ffmpegCommand.append(outputFile)

    out_pipe = sp.Popen(ffmpegCommand,
        stdin=sp.PIPE,stdout=sys.stdout, stderr=sys.stdout)

    smoothConstantDown = 0.08
    smoothConstantUp = 0.8
    lastSpectrum = None
    sampleSize = 2205#4410#1470#2205#4410#2205#1470

    numpy.seterr(divide='ignore')
    completeAudioArray = c#readAudioFile(inputFile,FFMPEG_BIN)
    subcompleteAudioArray = a #readAudioFile("newint.wav",FFMPEG_BIN)
    #intrlen = float(mediainfo('bismi.mp3')['duration'])/100
    

    #filelist = os.listdir(r"C:\Users\MSHK\AppData\Local\Programs\Python\Python37\Clips") #glob.glob(r"C:\Users\MSHK\AppData\Local\Programs\Python\Python37\Clips\*.png")
    #print(filelist)
    #bgI = 0

    #print(completeAudioArray)



    for yy in range(num):




        bgI = 0
        tag = 0
        nextval = results2[tag+1]*1000-results2[0]*1000# + intrlen
        fast = results3[tag]
        subfast = subheight*sampleSize/len(subcompleteAudioArray)
        count = results1[tag][1]
        subcount = 0
        subresult = [[0,0],[0,subheight]]
        #results1[j+1][1]-results1[j][1]
        temp = 0
        frames = os.listdir("frame")
        cnt = 0



        if yy == num-1:
            
            #image = Image.open("tempo.png")#+filelist[bgI])
            #subimage = Image.open("logo1.png")


            #attaching at the end
            image = image.crop((0, 0, width, results1[-1][1]))
            subimage = subimage.crop((0, 0, width, subheight))
            #im1.show()
            dst = Image.new("RGB", (width,results1[-1][1]+subheight), "black")
            dst.paste(image, (0,0))
            dst.paste(subimage, (0,results1[-1][1]))
            image = dst
            results1[-1][1] = results1[-1][1]+subheight
        

        
        #frames = frames.sort(key=lambda f: int(filter(str.isdigit, f)))
        for i in range(0, len(completeAudioArray), sampleSize):
            if temp<len(subcompleteAudioArray)/sampleSize :
                #subimage = Image.open("frame/"+"frame"+str(cnt)+".jpg")
                cnt +=1
                #print(frames[temp])
                im = drawBars(image,image,count,results1,0)
                #im = drawBars(subimage,image,subcount,subresult,1)
                subcount = subcount + subfast/2
                temp += 1
                #print(temp)
                #maxo = bgI
                #nextval = results2[tag+1]*1000 + maxo
        
                try:
                    out_pipe.stdin.write(im.tobytes())
                except:
                    pass   
               
            elif bgI/2<nextval:
                
                im = drawBars(image,image,count,results1,0)
                count = count + fast/2
                bgI += 1
                try:
                    out_pipe.stdin.write(im.tobytes())
                    #outval = out_pipe.check_output()
                    #print(type(outval))
                except:
                    pass
                
                
            else:
                tag = tag + 1
                try:
                    nextval = results2[tag+1]*1000-results2[0]*1000 # + intrlen
                    fast = results3[tag]
                    count  = results1[tag][1]
                    im = drawBars(image,image,count,results1,0)
                    bgI += 1
                    try:
                        outval = out_pipe.stdin.write(im.tobytes())
                        #print(type(outval))
                        #print(outval)
                    except:
                        pass
                except:
                    break
            #print(count,"  ",fast,"  ")
               
                  
          # create video for output
          #lastSpectrum = self.core.transformData(
           # i,
            #completeAudioArray,
            #sampleSize,
            #smoothConstantDown,
            #smoothConstantUp,
            #lastSpectrum)
          #if imBackground != None:
           # print(imBackground,"this is i wnat")
            #im = self.core.drawBars(lastSpectrum, imBackground, visColor)
          #else:
          #results1,results
          

          

          #im = drawBars(filelist,bgI)#Image.open(filelist[0])
          #print(i)#self.core.drawBars(lastSpectrum, getBackgroundAtIndex(bgI), visColor)
          #if bgI < len(filelist)-1:


    numpy.seterr(all='print')

    out_pipe.stdin.close()
    if out_pipe.stderr is not None:
      #print(out_pipe.stderr.read())
      out_pipe.stderr.close()
    # out_pipe.terminate() # don't terminate ffmpeg too early
    out_pipe.wait()


