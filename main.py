# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import this

import numpy as np

from Utilities.incident_angle import WaveAnalyzer
import os
import numpy
import math

num = 0
def findangle(arrs):
    x=arrs[2]
    y=arrs[0]
    w=arrs[1]
    count=0
    error=5 #degrees
    weightx=math.cos(math.radians(45))
    weighty=math.cos(math.radians(45))
    angle=45
    maxi=0
    while True:

        res=(weightx*x)+(weighty*y)
        anglep1= math.degrees(numpy.arccos(weightx))
        print(angle - anglep1)
        if max(res)>maxi and (abs(angle-anglep1)>error):
            maxi=max(res)
            if count%2==0:
                weightx=weightx+0.05
                if weightx>1:
                    weightx=1
                weighty=math.sqrt(1-(weightx*weightx))
            else:
                weightx=weightx-0.05
                if weightx<-1:
                    weightx=-1
                weighty=math.sqrt(1-(weightx*weightx))
        else:
            count=count+1
            if abs(angle-anglep1)<error:
                return math.degrees(numpy.arccos(weightx))




def get3chanarr(folder):
    global num
    list = os.listdir(folder)
    # print(list)
    i=0
    j=0
    arrs = [None, None, None]
    while i< len(list):
        if 'Audio Track' in list[i] and j < 3:
            arrs[j] = ((WaveAnalyzer((folder + "/" + list[i]))).wav_to_numpy_array())[1]
            if abs(max(arrs[j])) > num:
                num = abs(max(arrs[j]))

            j = j+1

        i = i+1


    arrs[0] = (arrs[0] / num)  # normalize arrays

    arrs[1] = (arrs[1] / num)

    arrs[2] = (arrs[2] / num)
    b= arrs[1]
    arrs[1]=6.144*arrs[2] #cheap eq to experiment
    arrs[2]=b


    return arrs

if __name__ == '__main__':
        # wav_path = '/Users/akosborbath/Documents/Soundskrit/DA/DA_SKRT/Utilities/led ring 1kHz 0deg.wav'  # Replace with your WAV file path
    # analyzer = WaveAnalyzer(wav_path)
    # x = analyzer.wav_to_numpy_array()
    # sig = x[1]

    # sigs = get3chanarr("/Users/akosborbath/Documents/Soundskrit/DA/DA_SKRT/Utilities")
    #
    # # print(math.degrees(numpy.arcsin(1)))
    # angle = findangle(sigs)
    # print(angle)

        analyzer = WaveAnalyzer(1270)

        thetas = analyzer.theta_time()
        # analyzer.predicted_thetas = analyzer.filter(analyzer.predicted_thetas)
        # print(analyzer.filter(analyzer.predicted_thetas))
        # print(analyzer.predicted_thetas)

        analyzer.plot_theta()


