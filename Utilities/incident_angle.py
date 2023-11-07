# -*- coding: utf-8 -*-
"""
Created on Tue Nov 7 11:45:21 2023

@author: yajiluck
"""

import numpy as np
import sounddevice as sd
from scipy.io import wavfile

class WaveAnalyzer:
    def __init__(self, wav_file_path):
        self.wav_file_path = wav_file_path
        self.sample_rate, self.data = self.wav_to_numpy_array()
        self.n_channels = self.data.shape[1] if self.data.ndim > 1 else 1
        self.sample_width = self.data.dtype.itemsize
        self.n_frames = self.data.shape[0]

    def wav_to_numpy_array(self):
        # Use scipy.io.wavfile to read the WAV file
        sample_rate, data = wavfile.read(self.wav_file_path)
        # No need to reshape data, scipy.io.wavfile already returns a numpy array
        return sample_rate, data

    def play(self):
        # Directly play numpy array
        sd.play(self.data, self.sample_rate)
        sd.wait()  # Wait until the audio has finished playing

# Example usage
# wav_path = 'test_sound.wav'  # Replace with your WAV file path
# analyzer = WaveAnalyzer(wav_path)
# analyzer.play()
