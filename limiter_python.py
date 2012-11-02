# A simple limiter

from pyaudio import PyAudio, paContinue, paFloat32
from time import sleep
from numpy import array, random, arange, float32, float64, zeros
import matplotlib.pyplot as plt

################################### Constants ##################################

fs            = 44100   # Hz
threshold     = 0.8     # absolute gain
delay         = 40      # samples
signal_length = 1       # second
release_coeff = 0.9999  # release time factor
attack_coeff  = 0.9     # attack time factor
dtype         = float32 # default data type
block_length  = 1024    # samples

#################### Generate quiet-loud-quiet noise signal ####################

signal = array(random.rand(fs*signal_length)*2-1, dtype=dtype)
signal[:signal_length*fs/3] *= 0.1
signal[signal_length*fs*2/3:] *= 0.1

############################# Implementation of Limiter ########################

class Limiter:
    def __init__(self, attack_coeff, release_coeff, delay, dtype=float32):
        self.delay_index = 0
        self.envelope = 0
        self.gain = 1
        self.delay = delay
        self.delay_line = zeros(delay, dtype=dtype)
        self.release_coeff = release_coeff
        self.attack_coeff = attack_coeff

    def limit(self, signal, threshold):
        for i in arange(len(signal)):
            self.delay_line[self.delay_index] = signal[i]
            self.delay_index = (self.delay_index + 1) % self.delay

            # calculate an envelope of the signal
            self.envelope *= self.release_coeff
            self.envelope  = max(abs(signal[i]), self.envelope)

            # have self.gain go towards a desired limiter gain
            if self.envelope > threshold:
                target_gain = (1+threshold-self.envelope)
            else:
                target_gain = 1.0
            self.gain = ( self.gain*self.attack_coeff +
                          target_gain*(1-self.attack_coeff) )

            # limit the delayed signal
            signal[i] = self.delay_line[self.delay_index] * self.gain

################################# Play the Audio ###############################

original_signal = array(signal, copy=True, dtype=dtype)

limiter = Limiter(attack_coeff, release_coeff, delay, dtype)

def callback(in_data, frame_count, time_info, flag):
    if flag:
        print("Playback Error: %i" % flag)
    played_frames = callback.counter
    callback.counter += frame_count
    limiter.limit(signal[played_frames:callback.counter], threshold)
    return signal[played_frames:callback.counter], paContinue

callback.counter = 0

pa = PyAudio()

stream = pa.open(format = paFloat32,
                 channels = 1,
                 rate = fs,
                 frames_per_buffer = block_length,
                 output = True,
                 stream_callback = callback)

while stream.is_active():
    sleep(0.1)

stream.close()
pa.terminate()

############################## Plot results ####################################

plt.figure()
plt.plot(original_signal, color='grey', label='original signal')
plt.plot(signal, color='black', label='limited signal')
plt.legend()
plt.show(block=True)
