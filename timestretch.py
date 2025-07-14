from bokumo import Audio

snare = Audio()
snare.read("snare05.wav")
stretchSnare = Audio(noChannels=2)
for segment in snare.iterate(4000):
    stretchSnare.append(segment)
    segment.reverse()
    stretchSnare.append(segment)

stretchSnare.write("stretchSnare.wav")