import numpy as np
import sounddevice as sd
from scipy.io import wavfile
import os
import matplotlib.pyplot as plt




class WaveAnalyzer:
    def __init__(self, degree, time_step = 0.25):
        #This degree is the 'real' angle that the measurements were taken from
        self.degree = degree
        #This will set self.x,self.y and self.w (3 channel measurements for the current degree)
        self.get_channels(degree=degree)
        
        #Time step between slices
        self.time_step = time_step
        

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
    def normalize(self):
        
        max_value = max(np.max(self.x),np.max(self.y),np.max(self.w))
        
        if max_value != 0:
            self.x /= max_value
            self.y /= max_value
            self.w /= max_value
            
        else:
            print('normalizing error')


    #Given a degree value, this sets the current wave analyzer x,y, and w channel
    #With their respective measurements (normalized)
    def get_channels(self, degree, folder='Measurements/'):
        valid_channels = ['X', 'Y', 'W']
        file_directory = os.path.join(folder, f"{degree}deg")

        for file in os.listdir(file_directory):
            file_path = os.path.join(file_directory, file)
            file_name = os.path.splitext(file)[0]
            channel = file_name[-1]

            if channel not in valid_channels:
                raise ValueError(f"Invalid channel measurement: {channel}")

            sample_rate, data = self.wav_to_numpy_array(file_path)
            if data is not None:
                if channel == 'X':
                    self.x = data.astype(np.float64)
                elif channel == 'Y':
                    self.y = data.astype(np.float64)
                elif channel == 'W':
                    self.w = data.astype(np.float64)
                    
                
        min_data_length = min(len(self.x),len(self.y),len(self.w))
        
        #Crop so all samples have same length (smallest available)
        self.x = self.x[:min_data_length]
        self.y = self.y[:min_data_length]
        self.w = self.w[:min_data_length]
        #To be used later
        self.sample_rate = sample_rate
            
                    
        self.normalize()
        
    
    #TODO equalize if necessary, not sure how to implement this yet, but we have access
    # to self.x, self.y, and self.w to work it out
    def equalize(self):
        pass
    
    
    #Function that predicts the incident angle of the measurement given relative weights to channel
    #x and y of the current measurements.
    def predict_angle(self, x, y, w):
       # x, y, and w are expected to be 2D arrays of shape (num_slices, slice_size)
              
       num_slices = x.shape[0] 
       theta_range = np.linspace(0, 2*np.pi, num=360)

       # Initialize arrays to store max_theta and max_value for each slice
       max_thetas = np.zeros(num_slices)
       max_values = -np.inf * np.ones(num_slices)
 

       for i, theta in enumerate(theta_range):
           wx = np.cos(theta)
           wy = np.sin(theta)

           # Perform dot product for all slices
           dot_products = wx * x + wy * y  # This will be a 2D array

           # Use mean as metric for "max" values
           #current_maxs = np.mean((dot_products), axis=1)
           
           current_maxs = np.max((dot_products), axis=1)

           # Update max_theta and max_value if a new maximum is found
           update_mask = current_maxs > max_values
           max_thetas[update_mask] = theta
           max_values[update_mask] = current_maxs[update_mask]

       # Adjust angles based on w
       max_measurements = np.cos(max_thetas[:, np.newaxis]) * x + np.sin(max_thetas[:, np.newaxis]) * y
       add_w = np.abs(max_measurements + w)
       sub_w = np.abs(max_measurements - w)

       complement = np.mean(add_w, axis=1) <= np.mean(sub_w, axis=1)
       max_thetas[complement] = (max_thetas[complement] + np.pi) % (2 * np.pi)

       # Convert radians to degrees
       max_thetas_degrees = np.rad2deg(max_thetas)
       

       # Return maximum theta for each slice
       return max_thetas_degrees
    
    
    def theta_time(self):
        slice_size = int(self.sample_rate * self.time_step)
        
        # Calculate the number of complete slices for each array
        min_length = min(len(self.x), len(self.y), len(self.w))
        num_slices = min_length // slice_size

        # Truncate arrays to make them divisible by slice_size
        x_truncated = self.x[:num_slices * slice_size]
        y_truncated = self.y[:num_slices * slice_size]
        w_truncated = self.w[:num_slices * slice_size]

        # Reshape arrays into (num_slices, slice_size)
        x_reshaped = x_truncated.reshape(num_slices, slice_size)
        y_reshaped = y_truncated.reshape(num_slices, slice_size)
        w_reshaped = w_truncated.reshape(num_slices, slice_size)

        # Vectorized operation to predict angles for all slices
        predicted_thetas = self.predict_angle(x_reshaped, y_reshaped, w_reshaped)

        self.predicted_thetas = predicted_thetas

        return predicted_thetas
        
        
        
    def plot_theta(self):
        num_slices = len(self.x) // int(self.sample_rate * self.time_step)
        
        predicted_thetas = self.theta_time()

        times = np.arange(len(self.predicted_thetas)).astype(np.float64)
        
        times *= self.time_step
        
        
        print(len(self.predicted_thetas) , len(times))

        # Ensure predicted_thetas has the same number of elements as times
        if len(self.predicted_thetas) != len(times):
            
        
            print("Error: Mismatch in the length of predicted_thetas and times.")
            return

        # Plotting
        plt.plot(times, self.predicted_thetas)
        plt.xlabel('Time (s)')
        plt.ylabel('Theta (degrees)')
        plt.title(f'Theta vs Time {self.degree}')
        plt.grid(True)
        plt.show()

         
        
        
   
    
   
analyzer = WaveAnalyzer(900)
    
thetas = analyzer.theta_time()


analyzer.plot_theta()
    
    