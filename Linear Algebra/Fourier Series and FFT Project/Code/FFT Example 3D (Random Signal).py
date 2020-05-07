#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 15:13:24 2020

@author: josephgross
"""

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

import numpy as np
import random
from scipy import fftpack
import scipy


colors = ["red", "green", "blue", "orange", "purple"]

def create_frequency_example(num_freq, sampling_rate):
    """
    Create a makeshift signal with a predefined number frequency 
    that will be randomly generated and summed. Also takes in the 
    sampling .

    Parameters
    ----------
    num_freq : 'int'
        The number of random frequencies that will be generated to create
        a random signal
    sampling_rate : 'float'
        Sampling rate, or number of measurements per second

    Returns
    -------
    "tuple"
        Tuple of the list of random frequencies used to create a signal x 
        and the np.array that hold the times that will be plotted (x-axis) 

    """
    
    # Create an array of times t to eventually plot 
    t = np.linspace(0, 2, 2*sampling_rate, endpoint=False)
    
    freq_list = sorted(random.sample(range(1, 7), num_freq))
    amp_list = [random.randint(1, 5) for i in range(num_freq)]
    
    random_freq_amp_list = [(freq_list[i], amp_list[i]) for i in range(num_freq)]
    
    x = 0
    for (freq, amp) in random_freq_amp_list:
        temp = amp * np.sin(freq * 2 * np.pi * t)
        x += temp
    
    return random_freq_amp_list, t, x

# ==============================================================================  
# Display the signal in 3d

def display_3D_signal(random_freq_amp_list, t, z):
    """
    Display the signal created in three dimensions.

    Parameters
    ----------
    random_frequencies_list : 'list'
        A list of integers (frequencies) that have been used to create the signal z
    t : 'np.array'
        Times from 0 to 2 that will be plotted
    z : 'np.array'
        A signal that is randomly generated from a list of random frequencies
        

    Returns
    -------
    None.

    """
    
    fig = plt.figure(figsize=(15,12))
    ax = plt.axes(projection='3d')
    
    n = len(random_freq_amp_list)
    
    ax.plot(t, np.zeros(t.size), z, "black")
    

    for i, (freq, amp) in enumerate(random_freq_amp_list):
        
        y_temp = np.zeros(t.size) + (n-i)
        z_temp = amp * np.sin(freq * 2 * np.pi * t)
        
        
        ax.plot(t, y_temp, z_temp, color=colors[i])
        
    ax.legend(loc='best')
        
    ax.set_xlabel("Time [s]", fontsize = 20)
    ax.set_ylabel("Frequency [Hz]", fontsize = 20)
    ax.set_zlabel("Amplitude",  fontsize = 20)

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    
    ax.set_title("Random Signal Creation", fontsize = 20)
    plt.show()

# ==============================================================================  
# Display the signal in 2D
    
def display_signal(random_freq_amp_list, t, x):
    """
    Displays the created frequency x as well as all the frequencies that 
    were added to create x

    Parameters
    ----------
    random_frequencies_list : 'list'
        A list of integers (frequencies) that have been used to create the signal x
    t : 'np.array'
        Times from 0 to 2 that will be plotted
    x : 'np.array'
        A signal that is randomly generated from a list of random frequencies

    Returns
    -------
    None.

    """
    n = len(random_freq_amp_list) + 1
    fig, axs = plt.subplots(n, sharex=True, sharey=True, figsize=(8,8))
    
    axs[n-1].plot(t,x, 'black')
    axs[n-1].set_xlabel('Time [s]')
    
    for i, ax in enumerate(axs):
        if i > n-2:
            continue
        
        freq = random_freq_amp_list[i][0]
        amp = random_freq_amp_list[i][1]
        x = amp*np.sin(freq * 2 * np.pi * t)
        ax.plot(t, x, color = colors[i])
        ax.legend(["%s Sin(2*Pi*t * %s), Freq = %s" % (amp,freq, freq)], loc='best')
        
        # Turn off tick labels
        ax.set_yticklabels([])
        
    axs[0].set_title("Random Signal Creation (Time [s] vs Amplitude)", fontsize = 20)
    
# ==============================================================================  
# Convert a frequency to the fourier transform

def discrete_fourier_transform(x, sampling_rate):
    """
    Compute the discrete fourier transform for a signal x

    Parameters
    ----------
    x : 'np.array'
        The input signal to compute the fourier transform of
    sampling_rate : 'int'
        Number of samples to be taken per second

    Returns
    -------
    X : 'np.array'
        The magnitudes of the discrete fourier transform  (y-axis)
    freqs : 'np.array'
        The frequencies of the fourier transform (x-axis).

    """
    
    X = fftpack.fft(x)
    freqs = fftpack.fftfreq(len(X)) * sampling_rate
    
    for i, freq in enumerate(freqs):
        if freq > 0 and np.abs(X[i]) > 10:
            print("Frequencies: %s" % str(round(freq)) + "Hz")
    
    return X, freqs


def display_fft(X, freqs, sampling_rate):
    """
    Display the fourier transform

    Parameters
    ----------
    X : 'np.array'
        The magnitudes of the discrete fourier transform  (y-axis)
    freqs : 'np.array'
        The frequencies of the fourier transform (x-axis).
    sampling_rate : 'int'
        Number of samples to be taken per second

    Returns
    -------
    None.

    """
    
    fig, ax = plt.subplots()
    
    ax.stem(freqs, np.abs(X), use_line_collection=True)
    ax.set_title("Discrete Fourier Transform Stem Plot (Frequency [Hz] vs Amplitude)", fontsize = 20)
    ax.set_xlabel('Frequency (Hz)', fontsize = 20)
    ax.set_ylabel('Amplitude', fontsize = 20)
    ax.set_xlim(0, 10)
    
    
# ==============================================================================
    
def read_audio_file(filename):
    """
    Read a .wav audio file

    Parameters
    ----------
    filename : 'str'
        File path of the .wav file to be read

    Returns
    -------
    sampling_rate : 'int'
        Number of samples to be taken per second
    audio : 'np.array'
        Array of magnitudes of a wav (y-axis)
    t : 'np.array'
        Array of times to be plotted (x-axis)

    """
   
    # Read the audio file. Rate is the sampling rate and audio is the actual audio
    sampling_rate, audio =  scipy.io.wavfile.read(filename)
    audio = np.mean(audio, axis=1)
    
    N = audio.shape[0]
    t = np.arange(N) / sampling_rate
    
    return sampling_rate, audio, t

    
    
if __name__ == "__main__":
    
    num_freq = 3 # Max is 5
    sampling_rate = 100
    
    random_frequencies_list, t, x = create_frequency_example(num_freq, sampling_rate)
    
    display_3D_signal(random_frequencies_list, t, x)
    
    display_signal(random_frequencies_list, t, x)
    
    X, freqs = discrete_fourier_transform(x, sampling_rate)
    display_fft(X, freqs, sampling_rate)
    