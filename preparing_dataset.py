# -*- coding: utf-8 -*-
"""preparing_dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yJQXaeMDlhjFouTXydtxr6AjPZjZ5dfM

**Music genre classification**
"""

import os
import librosa
import math
import json

DATASET_PATH = "/content/drive/MyDrive/music_dataset"
JSON_PATH = "/content/drive/MyDrive/music_dataset.json"

SAMPLE_RATE = 22050
DURATION = 30 # measured in sec
SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION

def save_mfcc(dataset_path, json_path, n_mfcc = 13, n_fft = 2048, hop_length = 512, num_segments = 5):

    # dictionary to store data
    data = {
        
        "mappings": [],
        "mfccs" : [],
        "labels" : []
    }

    num_samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
    expected_num_mfcc_vectors_per_segment = math.ceil(num_samples_per_segment / hop_length) # ->1.2..for example
 
    # loop through the directories
    for i,(dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):

       # ensure that we're at the root level
       if dirpath is not dataset_path:
    
          # save the semantic labels
          dirpath_components = dirpath.split("/")
          semantic_label = dirpath_components[-1]
          data["mappings"].append(semantic_label)

          print("\nProcessing: {}".format(semantic_label))

          # process files for specific genre

          for f in filenames:

              # load audio files
              file_path = os.path.join(dirpath, f)
              signal ,sr = librosa.load(file_path, sr = SAMPLE_RATE)

              # process segments extractng mfccs and storing data
              for s in range(num_segments):
                  start_sample = num_samples_per_segment * s
                  finish_sample = start_sample + num_samples_per_segment

                  mfccs = librosa.feature.mfcc(signal[start_sample:finish_sample],
                                               sr = sr, n_fft = n_fft, n_mfcc = n_mfcc,
                                               hop_length = hop_length)
                  mfccs = mfccs.T

                  # store mfcc for segment if it has expected length

                  if len(mfccs) == expected_num_mfcc_vectors_per_segment:
                      data["mfccs"].append(mfccs.tolist())
                      data["labels"].append(i-1)

                     # print("{}, segments:{}".format(file_path,s))

    with open(json_path, "w") as fp:
      json.dump(data, fp, indent=4)

if __name__== "__main__":
   save_mfcc(DATASET_PATH, JSON_PATH, num_segments=10)