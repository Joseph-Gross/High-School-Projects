#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 15:02:10 2020

@author: josephgross
"""


import matplotlib.pyplot as plt

import numpy as np
from scipy import signal

from IPython.display import Audio
from scipy.io import wavfile
from pydub import AudioSegment
from skimage import util

    
    
# ==============================================================================  
# Read an mp3 file, convert to .wav file and display it
    
def convert_mp3_to_wav(filename_import, filename_export):
    """
    Convert an mp3 file to a .wav file

    Parameters
    ----------
    filename_import : 'str'
        File path of the file to import
    filename_export : 'str'
        File path of the file to import

    Returns
    -------
    None.

    """
    
    sound = AudioSegment.from_mp3(filename_import)
    sound.export(filename_export, format="wav")

    
def read_audio_file(filename):
    """
    Read the mp3 file

    Parameters
    ----------
    filename : 'str'
        File path of the file to import

    Returns
    -------
    rate : 'int'
        Number of samples taken per second.
    audio : 'np.array'
        Array of amplitudes of a signal

    """
    filename_import = "/Users/josephgross/Desktop/FFT/Audio_Files/%s" % filename
    filename_export = "/Users/josephgross/Desktop/FFT/Audio_Files/test.wav"
    convert_mp3_to_wav(filename_import, filename_export)
    
    wav_file = '/Users/josephgross/Desktop/FFT/Audio_Files/test.wav'
    
    # Read the audio file. Rate is the sampling rate and audio is the actual audio
    rate, audio = wavfile.read(wav_file)
    audio = np.mean(audio, axis=1)
    
    return rate, audio

def display_audio_file(filename):
    """
    Display the wav of an mp3 file

    Parameters
    ----------
    filename : 'str'
        File path of the file to import

    Returns
    -------
    None.

    """
    rate, audio = read_audio_file(filename)
    
    N = audio.shape[0]
    L = N / rate

    print(f'Audio Length: {L:.2f} seconds')    
    
    f, ax = plt.subplots()
    ax.plot(np.arange(N) / rate, audio)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude [unkown]')
    
# ==============================================================================  

def fft_audio_file(signal, window_size=1024):
    """
    Split the audio into windows and apply the fourier transform to each

    Parameters
    ----------
    audio : 'np.array'
        Array of amplitudes of a signal
    window_size : 'int',  optional
        The size of the windows (numbe of samples). Default is 1024

    Returns
    -------
    fourier_transform : np.array
        The fourier transform of a signal

    """
    
    slices = util.view_as_windows(signal, window_shape=(window_size,), step=100)
    print(f'Audio shape: %s, Sliced audio shape:  %s' % (signal.shape, slices.shape))
    
    win = np.hanning(window_size + 1)[:-1]
    slices = (slices * win).T
    print('Shape of `slices`:', slices.shape)
    
    fourier_transform = np.fft.fft(slices, axis=0)[:window_size // 2 + 1: -1]
    
    return  np.abs(fourier_transform)

    
def display_spectrogram(filename):
    """
    Displays the Spectrogram of a signal. Take in the file path of an .mp3

    Parameters
    ----------
     filename : 'str'
        File path of the file to import

    Returns
    -------
    None.

    """
    M = 1024
    rate, audio = read_audio_file(filename)
    
    
    freqs, times, Sx = signal.spectrogram(audio, fs=rate, window='hanning',
                                      nperseg=1024, noverlap=M - 100,
                                      detrend=False, scaling='spectrum')

    f, ax = plt.subplots(figsize=(4.8, 2.4))
    ax.pcolormesh(times, freqs / 1000, 10 * np.log10(Sx), cmap='viridis')
    ax.set_ylabel('Frequency [kHz]')
    ax.set_xlabel('Time [s]');

# ==============================================================================  

if __name__ == "__main__":
    
    filename = 'Example.mp3'
    display_audio_file(filename)
    display_spectrogram(filename)