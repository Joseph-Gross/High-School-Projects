#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 23:17:29 2020

@author: josephgross
"""

import matplotlib.pyplot as plt

import numpy as np

import scipy
import scipy.io.wavfile
    
# ==============================================================================  
    
# Graphing helper function
def setup_graph(title='', x_label='', y_label='', fig_size=None):
    """
    Helper function for graphing

    Parameters
    ----------
    title : 'str', optional
       Title of the graph. The default is ''.
    x_label :  'str', optional
        X axis label. The default is ''.
    y_label : 'str', optional
        Y axis label. The default is ''.
    fig_size : tuple, optional
        Size of the figure. The default is None.

    Returns
    -------
    None.

    """
    fig = plt.figure()
    if fig_size != None:
        fig.set_size_inches(fig_size[0], fig_size[1])
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

def read_and_display_wav_file(filename, seconds_to_display, title='', xlabel='', ylabel='', fig_size=(14,7)):
    """
    Function to read in a wav file and display the sounds

    Parameters
    ----------
    filename : 'str'
        File path of a .wav file to read in
    seconds_to_display : 'float'
        The number of seconds to display of the signal
    title : 'str', optional
       Title of the graph. The default is ''.
    x_label :  'str', optional
        X axis label. The default is ''.
    y_label : 'str', optional
        Y axis label. The default is ''.
    fig_size : tuple, optional
        Size of the figure. The default is (14,7).

    Returns
    -------
    None.

    """
    
    (sample_rate, input_signal) = scipy.io.wavfile.read(filename)
    time_array = np.arange(0, len(input_signal)/sample_rate, 1/sample_rate)
    
    setup_graph(title=title, x_label=xlabel, y_label=ylabel, fig_size=fig_size)
    
    samples_to_take = round(seconds_to_display * sample_rate)
    plt.plot(time_array[0:samples_to_take], input_signal[0:samples_to_take])
    
    
# ============================================================================== 

    
def get_fft_wav_file(filename, sample_size=5000):
    """
    

    Parameters
    ----------
    filename : 'str'
        File path of a .wav file to read in
    sample_size : int, optional
        The amount of samples to return. The default is 5000.

    Returns
    -------
    'np.array'
        The frequencies of the discrete fourier transform (x-axis)
    'np.array'
        The magnitudes of the discrete fourier transform (y-axis)

    """
    
    (sample_rate, input_signal) = scipy.io.wavfile.read(filename)
    
    fft_out = np.fft.rfft(input_signal)
    fft_mag = [np.sqrt(i.real**2 + i.imag**2)/len(fft_out) for i in fft_out]
    num_samples = len(input_signal)
    rfreqs = [(i*1.0/num_samples)*sample_rate for i in range(num_samples//2+1)]
    
    
    return rfreqs[0:sample_size], fft_mag[0:sample_size]
    
    
def display_fft_wav_file(filename, sample_size=5000, title='', xlabel='', ylabel='', fig_size=(14,7)):
    """
    

    Parameters
    ----------
    filename : 'str'
        File path of a .wav file to read in and display the DFT
    sample_size : TYPE, optional
        DESCRIPTION. The default is 5000.
    title : 'str', optional
       Title of the graph. The default is ''.
    x_label :  'str', optional
        X axis label. The default is ''.
    y_label : 'str', optional
        Y axis label. The default is ''.
    fig_size : tuple, optional
        Size of the figure. The default is (14,7).

    Returns
    -------
    None.

    """
    
    (rfreqs, fft_mag) = get_fft_wav_file(filename, sample_size)
    
    setup_graph(title=title, x_label=xlabel, y_label=ylabel, fig_size=fig_size)
    plt.plot(rfreqs, fft_mag)


# ============================================================================== 


def stft(input_data, sample_rate, window_size, hop_size):
    """
    Short Time Fourier Transform. Breaks the input data into windows and applies the
    Fourier Transform on each window

    Parameters
    ----------
    input_data : 'np.array'
        A signal (complex wave)
    sample_rate : 'int'
        The number of samples taken per second for the input data
    window_size : 'int'
        The size of each window (number of samples)
    hop_size : 'int'
        The number up samples in between the start of each window

    Returns
    -------
    output : 'list'
        List of Fourier Transforms (one for each window)

    """
    window = np.hamming(window_size)
    #print(len([len(input_data[i:i+window_size]) for i in range(0, len(input_data)-window_size, hop_size)]))
    #print(len([window for i in range(0, len(input_data)-window_size, hop_size)]))
    #print([len(window*input_data[i:i+window_size]) for i in range(0, len(input_data)-window_size, hop_size)])
    output = ([np.fft.fft(window*input_data[i:i+window_size]) 
                          for i in range(0, len(input_data)-window_size, hop_size)])
    return output

def istft(input_data, sample_rate, window_size, hop_size, total_time):
    """
    Inverse Short Time Fourier Transform. Breaks the input data into windows and applies the
    Inverse Fourier Transform on each window

    Parameters
    ----------
    input_data : 'np.array'
        A signal (complex wave)
    sample_rate : 'int'
        The number of samples taken per second for the input data
    window_size : 'int'
        The size of each window (number of samples)
    hop_size : 'int'
        The number up samples in between the start of each window
    total_time : 'int'
        The total duration of a signal

    Returns
    -------
    output : 'list'
        List of Inverse Fourier Transforms (one for each window)

    """
    total_samples = round(total_time*sample_rate)
    output = np.zeros(total_samples) # Zeros array used for synthesizing the original ai
    for n,i in enumerate(range(0, len(output)-window_size, hop_size)):
        output[i:i+window_size] += np.real(np.fft.ifft(input_data[n]))
    return output


# ============================================================================== 


def low_pass_filter(max_freq, window_size, sample_rate):
    """
    A low-pass filter (LPF) is a filter that passes signals with a frequency lower than a 
    selected maximum frequency

    Parameters
    ----------
    max_freq : 'float'
        The cutoff frequency
    window_size : 'int'
        he size of each window (number of samples)
    sample_rate : 'int'
        The number of samples taken per second for the input data

    Returns
    -------
    filter_block : 'np.array'
        A filtered array of ones (all samples with a frequency greater than the cutoff are
        0 and the rest are one). This will multiplied with the input signal to filter the audio

    """
    
    max_freq_bin = round(max_freq * window_size / sample_rate)
    filter_block = np.ones(window_size)
    filter_block[max_freq_bin:(window_size-max_freq_bin)] = 0
    return filter_block

def high_pass_filter(min_freq, window_size, sample_rate):
    """
    A high-pass filter (HPF) is a filter that passes signals with a frequency higher than a 
    selected minimum frequency

    Parameters
    ----------
    min_freq : 'float'
        The cutoff frequency
    window_size : 'int'
        The size of each window (number of samples)
    sample_rate : 'int'
        The number of samples taken per second for the input data

    Returns
    -------
    filter_block : 'np.array'
        A filtered array of ones (all samples with a frequency less than the cutoff are
        0 and the rest are one). This will multiplied with the input signal to filter the audio

    """
    
    return np.ones(window_size) - low_pass_filter(min_freq, window_size, sample_rate)

def write_audio_file(outfile, data, sample_rate):
    """
    Writes the audio to a .wav file

    Parameters
    ----------
    outfile : "Str"
        The filepath the filtered audio file will be written to
    data : 'np.array'
        The ignal that will be saved as a .wav file
    sample_rate : 'int'
        The number of samples taken per second for the input data

    Returns
    -------
    None.

    """
    scipy.io.wavfile.write(outfile, sample_rate, data)
    
    
def filter_audio(input_signal, sample_rate, filter_window, window_size=256):
    """
    The Audio is actually filtered here

    Parameters
    ----------
    input_signal : 'np.array'
        The audio to be filtered
    sample_rate : 'int'
        The number of samples taken per second for the input data
    filter_window : 'np.array'
         Array of ones and zeros that will be multiplied by the input signal
         to filter the audio
    window_size : 'int', optional
        The size of each window (number of samples). The default is 256.

    Returns
    -------
    resynth : TYPE
        DESCRIPTION.

    """
    # Setting parameters
    hop_size = window_size // 2
    total_time = len(input_signal) / sample_rate
    
    # Do actual filtering and synthesize the wave
    stft_output = stft(input_signal, sample_rate, window_size, hop_size)
    filtered_result = [original * filter_window for original in stft_output]
    resynth = istft(filtered_result, sample_rate, window_size, hop_size, total_time)
    
    return resynth


# ============================================================================== 
    
#def signal_high_pass_and_low_pass_filter(infile, outfile_low, outfile_high)
    
    
if __name__ == "__main__":
    
    infile = "/Users/josephgross/Desktop/FFT/Audio_Files/A220_A233.wav"
    outfile1 = "/Users/josephgross/Desktop/FFT/Audio_Files/filtered_audio_low.wav"
    outfile2 = "/Users/josephgross/Desktop/FFT/Audio_Files/filtered_audio_high.wav"
    
    #infile = "/Users/josephgross/Desktop/FFT/Audio_Files/A220_C139.wav" 
    #outfile1 = "/Users/josephgross/Desktop/FFT/Audio_Files/filtered_audio_low2.wav"
    #outfile2 = "/Users/josephgross/Desktop/FFT/Audio_Files/filtered_audio_high2.wav"
   
    window_size = round(256)
    frequency_to_filter = 100
    delta = 0
    low_frequency = frequency_to_filter - delta
    high_frequency = frequency_to_filter + delta

    # Reading the original input file
    (sample_rate, audio) = scipy.io.wavfile.read(infile)
    input_signal = np.mean(audio, axis=1)
    
    
    # Create low pass filter window and filter the audio
    filter_window = low_pass_filter(low_frequency, window_size, sample_rate)
    resynth = filter_audio(input_signal, sample_rate, filter_window, window_size)
    write_audio_file(outfile1, resynth, sample_rate)
    
    # Create high pass filter window and filter the audio
    filter_window = high_pass_filter(high_frequency, window_size, sample_rate)
    resynth = filter_audio(input_signal, sample_rate, filter_window, window_size)
    write_audio_file(outfile2, resynth, sample_rate)
    
    
    # Read thefiltered audio files and display them
    seconds_to_display = 0.08
    sample_size = 1000
    
    filename1 = infile
    read_and_display_wav_file(filename1, seconds_to_display, 
                              title='A220 + C#139 Sound', 
                              xlabel='Time (Hz)', ylabel='Amplitude')
    display_fft_wav_file(filename1, sample_size=sample_size,
                              title='DFT of A220 + C#139 Sound (first %s Samples)' % sample_size, 
                              xlabel='Frequency (Hz)', ylabel='Amplitude')
    
    filename2 = outfile1
    read_and_display_wav_file(filename2, seconds_to_display, 
                              title='Low Pass Filter < %s Hz Sound' % low_frequency, 
                              xlabel='Time (s)', ylabel='Amplitude')
    display_fft_wav_file(filename2, sample_size=sample_size,
                              title='FFT of Low Pass Filter (first %s Samples)' % sample_size, 
                              xlabel='Frequency (Hz)', ylabel='Amplitude')
    
    filename3 = outfile2
    read_and_display_wav_file(filename3, seconds_to_display,
                              title='High Pass Filter > %s Hz Sound' % high_frequency,
                              xlabel='Time (s)', ylabel='Amplitude')
    display_fft_wav_file(filename3, sample_size=sample_size,
                              title='FFT of High Pass Filter (first %s Samples)' % sample_size, 
                              xlabel='Frequency (Hz)', ylabel='Amplitude')
    



    # Add the low pass filtered signal and the high pass filtered window and compare them
    (sample_rate, a) = scipy.io.wavfile.read(infile)
    a = np.mean(audio, axis=1)
    
    (sample_rate, b) = scipy.io.wavfile.read(outfile1)
    (sample_rate, c) = scipy.io.wavfile.read(outfile2)
    print(a.shape, b.shape, c.shape)
    
    input_signal = b + c
    time_array = np.arange(0, len(input_signal)/sample_rate, 1/sample_rate)
    
    setup_graph(title="Low Pass Filter + High Pass Filter", x_label="Time (s)", 
                y_label="Amplitude", fig_size=(14,7))
    
    samples_to_take = round(seconds_to_display * sample_rate)
    plt.plot(time_array[0:samples_to_take], input_signal[0:samples_to_take], label = "Low + High")
    plt.plot(time_array[0:samples_to_take], a[0:samples_to_take], label = "Original")
    
    plt.legend()





# ============================================================================== 
# Not part of main program
# Everything below was used for testing and for playing with different
# concepts such as hamming and windows




def flatten(lst):
    return [item for sublist in lst for item in sublist]


def hamming_example():
    sample_rate = 100
    total_time = 10   # in seconds
    t = np.linspace(0, total_time, total_time * sample_rate)
    original = [5 for i in t]
    
    setup_graph(title='f(x) = 5 function', x_label='time (in seconds)', y_label='amplitude')
    plt.plot(t, original)
    
    
    window_size = 100 # 100 points (which is 1 second in this case)
    hop_size = window_size // 2
    
    window = np.hamming(window_size) # Creates a raised cosine with non-zero endpoints, optimized to minimize the nearest side lobe.
    
    
    window_times = [t[i:i+window_size] for i in range(0, len(original)-window_size, hop_size)] # Creates windows of time of a given length
    window_graphs = [[wtime, window] for wtime in window_times] # Creates pairs: times to plot and amplitude
    flattened_window_graphs = flatten(window_graphs) # Flattens each pair so that there are 2*len(window_times) items in the list

    setup_graph(title='Hamming windows', x_label='time (in seconds)', y_label='amplitude', fig_size=(14,5))
    plt.plot(*flattened_window_graphs) # Allows you to graph a list. Example: *[1,2,3,4] is plotted as [(1,2), (3,4)]

    # Each window is a cosine wave multiplied by the original wave (same window size and length) with different start and end times
    # Amplitude is scaled from 1 to the ampliude of the original wave
    windowed = [window * original[i:i+window_size] for i in range(0, len(original)-window_size, hop_size)] 
    setup_graph(title='Scaled Amplitude Windows (first 5)', x_label='time (in seconds)', y_label='amplitude', fig_size=(14,5))
    plt.plot(t[0:window_size], window * original[0:window_size])
    plt.plot(t[window_size:2*window_size], window * original[window_size:2*window_size])
    plt.plot(t[2*window_size:3*window_size], window * original[2*window_size:3*window_size])
    plt.plot(t[3*window_size:4*window_size], window * original[3*window_size:4*window_size])
    plt.plot(t[4*window_size:5*window_size], window * original[4*window_size:5*window_size])
    
    # Join the scaled waves into one array so that the original wave can be syntheiszed/replicated
    convoluted = np.zeros(total_time * sample_rate) # zeroes the length of the total samples
    for n,i in enumerate(range(0, len(original)-window_size, hop_size)):
        convoluted[i:i+window_size] += windowed[n] # Add each windw to an array of zeros to "concatenate" them
        
    setup_graph(title='Resynthesized windowed parts (vs original)', x_label='time (in seconds)', y_label='amplitude', fig_size=(14,5))
    plt.plot(t, original, t, convoluted)
    
    
    
    
def test():
    
    sample_rate = 10 # samples per sec
    total_sampling_time = 3
    num_samples = sample_rate * total_sampling_time

    t = np.linspace(0, total_sampling_time, num_samples)

    # between x = 0 and x = 1, a complete revolution (2 pi) has been made, so this is
    # a 1 Hz signal with an amplitude of 5
    frequency_in_hz = 1
    wave_amplitude = 5
    f = lambda x: wave_amplitude * np.sin(frequency_in_hz * 2*np.pi*x)
    
    
    sampled_f = [f(i) for i in t]
    setup_graph(title='time domain', x_label='time (in seconds)', y_label='amplitude', fig_size=(12,6))
    plt.plot(t, sampled_f)
    

    rfft_output = np.fft.rfft(sampled_f)
    setup_graph(title='rFFT output', x_label='frequency (in Hz)', y_label='amplitude', fig_size=(12,6))
    plt.plot(rfft_output)
    
    # Getting frequencies on x-axis right
    rfreqs = [(i*1.0/num_samples)*sample_rate for i in range(num_samples//2+1)]
    rfft_mag = [np.sqrt(i.real**2 + i.imag**2)/len(rfft_output) for i in rfft_output]
    setup_graph(title='Corrected rFFT Output', x_label='frequency (in Hz)', y_label='magnitude', fig_size=(12,6))
    plt.plot(rfreqs, rfft_mag)