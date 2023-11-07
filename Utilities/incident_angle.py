# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 11:45:21 2023

@author: yajiluck
"""

import wave
import numpy as np
import simpleaudio as sa

class WaveAnalyzer:
    def __init__(self, wav_file_path):
        self.wav_file_path = wav_file_path
        self.sample_rate, self.n_channels, self.sample_width, self.n_frames, self.data = self.wav_to_numpy_array()

    def wav_to_numpy_array(self):
        # Open the WAV file
        with wave.open(self.wav_file_path, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()
            n_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            n_frames = wav_file.getnframes()
            frames = wav_file.readframes(n_frames)
            
            dtype_map = {1: np.int8, 2: np.int16, 4: np.int32}
            if sample_width in dtype_map:
                dtype = dtype_map[sample_width]
            else:
                raise ValueError(f"Unsupported sample width: {sample_width}")
            data = np.frombuffer(frames, dtype=dtype)
            
            if n_channels > 1:
                data = data.reshape(-1, n_channels)
            return sample_rate, n_channels, sample_width, n_frames, data

    def play(self):
        # Convert numpy array to bytes
        audio_data = self.data.tobytes()
        # Play audio
        play_obj = sa.play_buffer(audio_data, self.n_channels, self.sample_width, self.sample_rate)
        play_obj.wait_done()

# Example usage
wav_path = 'test_sound.wav'  # Replace with your WAV file path
analyzer = WaveAnalyzer(wav_path)
analyzer.play()
