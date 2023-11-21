import numpy as np
import sounddevice as sd
from scipy.io import wavfile
import os

class WaveAnalyzer:
    def __init__(self, degree):
        #This degree is the 'real' angle that the measurements were taken from
        self.degree = degree
        #This will set self.x,self.y and self.w (3 channel measurements for the current degree)
        self.get_channels(degree=degree)

    #Converts a wave file (given its path) to a numpy array
    def wav_to_numpy_array(self, wav_file_path):
        try:
            sample_rate, data = wavfile.read(wav_file_path)
            return sample_rate, data
        except Exception as e:
            print(f"Error reading {wav_file_path}: {e}")
            return None, None

    #Plays a sound given data and sample_rate (can be acquired by wav_to_numpy_array)
    def play(self, data, sample_rate):
        sd.play(data, sample_rate)
        sd.wait()

    #Normalizes an array so that its maximum value is 1 
    def normalize(self, array):
        max_value = np.max(array)
        if max_value != 0:
            return array / max_value
        else:
            return array

    #Given a degree value, this sets the current wave analyzer x,y, and w channel
    #With their respective measurements (normalized)
    def get_channels(self, degree, folder='Measurements/'):
        valid_channels = ['x', 'y', 'w']
        file_directory = os.path.join(folder, f"{degree}deg")

        for file in os.listdir(file_directory):
            file_path = os.path.join(file_directory, file)
            file_name = os.path.splitext(file)[0]
            channel = file_name[-1]

            if channel not in valid_channels:
                raise ValueError(f"Invalid channel measurement: {channel}")

            sample_rate, data = self.wav_to_numpy_array(file_path)
            if data is not None:
                normalized_data = self.normalize(data)
                if channel == 'x':
                    self.x = normalized_data
                elif channel == 'y':
                    self.y = normalized_data
                elif channel == 'w':
                    self.w = normalized_data
    
    #TODO equalize if necessary, not sure how to implement this yet, but we have access
    # to self.x, self.y, and self.w to work it out
    def equalize(self):
        pass
    
    
    #Function that predicts the incident angle of the measurement given relative weights to channel
    #x and y of the current measurements.
    def predict_angle(self, threshold=0.01):
        # Initialize variables
        max_theta = 0
        max_value = -np.inf
        current_max = -np.inf

        # Iterate over a range of angles (in radians)
        for theta in np.linspace(0, 2*np.pi, num=360):
            wx = np.cos(theta)
            wy = np.sin(theta)

            # Perform dot product
            dot_product = np.dot(self.x, wx) + np.dot(self.y, wy)

            # Find maximum value
            current_max = np.max(dot_product)

            # Update max_theta and max_value if a new maximum is found
            if current_max > max_value:
                max_theta = theta
                max_value = current_max

            # Check if the difference is less than the threshold
            if np.abs(current_max - max_value) < threshold:
                break

        # Set the current "maximum" and its corresponding theta
        self.maximum = max_value
        self.max_theta = max_theta

        return max_theta, max_value
    
    
    
   
    
    
    

# Example usage
analyzer = WaveAnalyzer(degree=0)
# To play, use: analyzer.play(analyzer.x, sample_rate) # assuming sample_rate is defined

analyzer.predict_angle()

