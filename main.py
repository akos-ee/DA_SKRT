# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import this

from Utilities.incident_angle import WaveAnalyzer
import os
import numpy

num = 0
def get3chanarr(folder):
    global num
    list = os.listdir(folder)
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
    arrs[0] = (arrs[0] /num)+1  # normalize arrays and shift
    arrs[1] = (arrs[1] / num)+1
    arrs[2] = (arrs[2] / num)+1
    return arrs
if __name__ == '__main__':
    # wav_path = '/Users/akosborbath/Documents/Soundskrit/DA/DA_SKRT/Utilities/led ring 1kHz 0deg.wav'  # Replace with your WAV file path
    # analyzer = WaveAnalyzer(wav_path)
    # x = analyzer.wav_to_numpy_array()
    # sig = x[1]

    sig = get3chanarr("/Users/akosborbath/Documents/Soundskrit/DA/DA_SKRT/Utilities")[2]
    print(sig)





