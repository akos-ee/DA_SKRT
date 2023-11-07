# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from Utilities.incident_angle import WaveAnalyzer
import os
def get3chanarr(folder):
    list = os.listdir(folder)
    i=0
    j=0
    arrs = [None, None, None]
    while i< len(list):
        if 'Audio Track' in list[i]:
            arrs[j] = ((WaveAnalyzer((folder + "/" + list[i]))).wav_to_numpy_array())[i]
            j = j+1

        i = i+1
if __name__ == '__main__':
    wav_path = '/Users/akosborbath/Documents/Soundskrit/DA/DA_SKRT/Utilities/led ring 1kHz 0deg.wav'  # Replace with your WAV file path
    analyzer = WaveAnalyzer(wav_path)
    x = analyzer.wav_to_numpy_array()
    sig = x[1]
    print(sig)






