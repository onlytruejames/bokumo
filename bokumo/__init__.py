import soundfile as sf
import numpy as np
import copy

class Audio:
    def __init__(self, noChannels=1, samplerate=44100):
        self.channels = [Channel(samplerate=samplerate) for i in range(noChannels)]
        self.samplerate = samplerate
    
    def read(self, fname, overwriteSampleRate=True):
        data, samplerate = sf.read(fname)
        if overwriteSampleRate:
            self.samplerate = samplerate
        if type(data[0]) != np.array:
            data = np.array([data])
        else:
            data = np.swapaxes(data, 0, 1)
        self.channels = []
        for channel in data:
            self.channels.append(Channel(channel, samplerate=self.samplerate))

    def write(self, fname):
        data = np.array([channel.data for channel in self.channels])
        data = np.swapaxes(data, 0, 1)
        sf.write(fname, data, self.samplerate)

    def append(self, audio):
        if not len(audio.channels) == self.nChannels:
            raise Exception("Could not append audios: number of channels does not match")
        for c in range(self.nChannels):
            self.channels[c].append(audio.channels[c])
    
    def reverse(self):
        for c in range(self.nChannels):
            self.channels[c].reverse()

    def copy(self):
        return copy.deepcopy(self)
    
    def section(self, start, stop):
        newAudio = self.copy()
        for c in range(newAudio.nChannels):
            newAudio.channels[c].data = newAudio.channels[c].data[start:stop]
        return newAudio
    
    def addChannel(self, newChannel):
        try:
            assert newChannel.length == self.length
        except:
            raise Exception("Could not add channel: lengths do not match")

    class __Iterator:
        def __init__(self, audio, blockSize, addRemainder=True):
            self.current = 0
            self.audio = audio
            self.blockSize = blockSize
            self.addRemainder = addRemainder
            self.remainder = False
            self.segments = self.audio.length // self.blockSize

        def __iter__(self):
            return self

        def __next__(self):
            if self.remainder:
                raise StopIteration
            if self.current + 1 == self.segments:
                self.remainder = True
                return self.audio.section(self.current * self.blockSize, self.audio.length)
            seg = self.audio.section(self.current * self.blockSize, (self.current + 1) * self.blockSize)
            self.current += 1
            return seg

    def iterate(self, blocksize, addRemainder=True):
        return self.__Iterator(self, blocksize, addRemainder)

    @property
    def nChannels(self):
        return len(self.channels)
    
    @property
    def length(self):
        return self.channels[0].length
    
    def matches(self, other):
        try:
            assert other.length == self.length
        except:
            raise Exception("Could not perform operation: lengths do not match")
        try:
            assert other.nChannels == self.nChannels
        except:
            raise Exception("Could not perform operation: number of channels does not match")

    def __iadd__(self, other):
        if type(other) == type(self):
            self.matches(other)
            for c in range(self.nChannels):
                self.channels[c] += other.channels[c]
        elif type(other) == int or type(other) == float:
            for c in range(self.nChannels):
                self.channels[c] += other
        return self
        
    def __isub__(self, other):
        if type(other) == type(self):
            self.matches(other)
            for c in range(self.nChannels):
                self.channels[c] -= other.channels[c]
        elif type(other) == int or type(other) == float:
            for c in range(self.nChannels):
                self.channels[c] -= other
        return self
    
    def __imul__(self, other):
        if type(other) == type(self):
            self.matches(other)
            for c in range(self.nChannels):
                self.channels[c] *= other.channels[c]
        elif type(other) == int or type(other) == float:
            for c in range(self.nChannels):
                self.channels[c] *= other
        return self

    def __itruediv__(self, other):
        if type(other) == type(self):
            self.matches(other)
            for c in range(self.nChannels):
                self.channels[c] /= other.channels[c]
        elif type(other) == int or type(other) == float:
            for c in range(self.nChannels):
                self.channels[c] /= other
        return self
    
    def __add__(self, other):
        first = self.copy()
        first += other
        return first
    
    def __sub__(self, other):
        first = self.copy()
        first -= other
        return first
    
    def __mul__(self, other):
        first = self.copy()
        first *= other
        return first
    
    def __truediv__(self, other):
        first = self.copy()
        first /= other
        return first

class Channel:
    def __init__(self, data=None, samplerate=44100):
        if type(data) == type(None):
            data = np.array([])
        self.data = data
    
    def append(self, channel):
        self.data = np.append(self.data, channel.data)
    
    def reverse(self):
        self.data = self.data[::-1]
    
    @property
    def length(self):
        return len(self.data)
    
    def __iadd__(self, other):
        if type(other) == type(self):
            self.data += other.data
        elif type(other) == int or type(other) == float:
            self.data += other
        return self
    
    def __isub__(self, other):
        if type(other) == type(self):
            self.data -= other.data
        elif type(other) == int or type(other) == float:
            self.data -= other
        return self

    def __imul__(self, other):
        if type(other) == type(self):
            self.data *= other.data
        elif type(other) == int or type(other) == float:
            self.data *= other
        return self
    
    def __itruediv__(self, other):
        if type(other) == type(self):
            self.data /= other.data
        elif type(other) == int or type(other) == float:
            self.data /= other
        return self