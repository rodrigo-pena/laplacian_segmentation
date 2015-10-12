# -*- coding: utf-8 -*-
# CREATED: 2015-10-12 10:26:00 by Rodrigo Pena <rodrigo.pena@epfl.ch>
"""Visualization of lab files

"""

# %% Import libraries
import librosa
import numpy as np
import matplotlib.pyplot as plt

# %% Read audio file and compute its spectrogram
audio_path = '/Users/rodrigopena/Music/dizquefuiporai.mp3'
y, sr = librosa.load(audio_path, sr=44100)

S = librosa.feature.melspectrogram(y, sr=sr)
log_S = librosa.logamplitude(S, ref_power=np.max)

# %% Read lab file and extract the fields
start, end, labels = [], [], []
with open('dizquefuiporai8.lab') as infile:
    print "Start / End / Label"
    for line in infile:
        print line
        fields = line.split()
        start.append(float(fields[0]))
        end.append(float(fields[1]))
        labels.append(int(fields[2]))

start = np.array(start)
end = np.array(end)
labels = np.array(labels)

# %% Convert the time stamps into frame indices
start_frames = librosa.time_to_frames(start, sr=sr)
end_frames = librosa.time_to_frames(end, sr=sr)

# %% Overlay the section markers with the mel-frequency spectrogram

plt.figure(figsize=(12, 6))
librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel',
                         n_xticks=20)

# Overlay with the detected beats
colors = ['r', 'c', 'orange', 'b', 'k', 'g', 'm', 'y']
for i in range(len(labels)):
    lines = np.arange(start_frames[i], end_frames[i])
    plt.vlines(lines, 0, log_S.shape[0],
               colors=colors[labels[i] % len(colors)],
               linestyles='-', linewidth=2, alpha=0.01)
plt.axis('tight')
title = audio_path
plt.title(title)
plt.show()

# %% Print Section transition times

print "Start\tEnd\tLabel"
for i in range(len(start)):
    print "%02d:%02d\t%02d:%02d\t%d" % \
        (start[i] / 60, start[i] % 60, end[i] / 60, end[i] % 60, labels[i])
