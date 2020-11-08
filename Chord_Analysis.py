from collections import Counter
from csv import reader
import numpy as np
import pandas as pd
from random import choices

# Opening the csv file with the scrapped chord progression data
with open('the_beatles_chordprogressiondata.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    data = list(csv_reader)

# Create lists of lists with the data for each chord progression
chord_data_maj = []
chord_data_min = []
for row in data:
    if 'maj' in row[1] and row[2] !='':
        chord_data_maj.append([i for i in row[2:] if i] )
    elif 'min' in row[1] and row[2] !='':
        chord_data_min.append([i for i in row[2:] if i] )
    else:
        pass

# Grabbing the different major and minor keys used
major_keys = [el[1] for el in data if 'maj' in el[1]]
minor_keys = [el[1] for el in data if 'min' in el[1]]

# Grabbing the first chord in every major and minor key song
first_maj = [item[0] for item in chord_data_maj]
first_min = [item[0] for item in chord_data_min]
 

# Grabbing sorted list of chords used in each key
unique_maj = sorted(list(set(x for l in chord_data_maj for x in l)))
unique_min = sorted(list(set(x for l in chord_data_min for x in l)))

# Creating an empty matrix with the chords in each mode
tsm_maj_temp = pd.DataFrame(0, index=unique_maj, columns=unique_maj)
tsm_min_temp = pd.DataFrame(0, index=unique_min, columns=unique_min)


# Function to compute transition state matrix given empty tsm, chord progression data, and unique chords in a mode
def get_tsm(tsm,data,unique):
    lst = list(range(0,len(unique)))
    m = dict(zip(unique,lst))
    for row in data:
        for i in range(len(row)-1):
            tsm.iloc[m[row[i+1]],m[row[i]]] += 1
    return tsm.divide(tsm.sum(axis=1))

# Creating transition state matrix for major and minor keys
tsm_maj = get_tsm(tsm_maj_temp, chord_data_maj,unique_maj)
tsm_min = get_tsm(tsm_min_temp, chord_data_min,unique_min)


# Function to calculate the probability from a single song characteristic,
#       such as its key or first chord

def single_col_prob(lst):
    counts = dict(Counter(lst))
    return {k: v / sum(counts.values()) for k, v in counts.items()}


# Computing probability vectors for the first chord in both major and minor keys, as well as
#       the root note for a key (e.x. C major, D major)
first_prob_maj = single_col_prob(first_maj)
first_prob_min = single_col_prob(first_min)
key_prob_maj = single_col_prob(major_keys)
key_prob_min = single_col_prob(minor_keys)


# Function to randomly choose a key
def key_chooser(mode):
    if mode == 'major':
        return choices(list(key_prob_maj.keys()),list(key_prob_maj.values()))
    else:
        return choices(list(key_prob_min.keys()),list(key_prob_min.values()))

# Function that uses probability data to generate chord progressions
def chord_progression_generator(mode,length=4, total=1):
    full = []
    # Creating n total amount of chord progressions 
    for i in range(0,total):
        chord_lst = []
        # Setting the key and starting chord via probability vectors
        if mode == 'major':
            tsm = tsm_maj
            chord_lst.append(key_chooser(mode)[0])
            unique = unique_maj
            c = choices(list(first_prob_maj.keys()),list(first_prob_maj.values()))
            chord_lst.append(c[0])
        else:
            tsm = tsm_min
            chord_lst.append(key_chooser(mode)[0])
            unique = unique_min
            c = choices(list(first_prob_min.keys()),list(first_prob_min.values()))
            chord_lst.append(c[0])

        # Generate full chord progression
        for i in range(0,length-1):
            c = choices(unique,tsm[c].to_numpy())
            chord_lst.append(c[0])
        full.append(chord_lst)
    return(full)

# Running the function on the major key transition state matrix
gen_chords = chord_progression_generator('major',4,10)#, 'major',10, key = True)
print("Chord Progression(s) generate in the style of The Beatles (major key):")
for g in gen_chords:
    print(g)

# Running the function on the minor key transition state matrix
gen_chords = chord_progression_generator('minor',4,10)
print('')
print("Chord Progression(s) generate in the style of The Beatles (minor key):")
for g in gen_chords:
    print(g)

