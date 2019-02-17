#!/usr/bin/env python


import pyaudio
import struct
import math
import time,sys
import threading


INITIAL_TAP_THRESHOLD = 0.010
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 16000  
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME                    
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME # if we get this many quiet blocks in a row, decrease the threshold
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME # if the noise was longer than this many blocks, it's not a 'tap'



def get_rms(block):

    # L’amplitude d’un son est la caractéristique la plus simple que l’on puisse imaginer.
    #  Elle caractérise directement l’intensité du son  c’est à dire son volume, ou encore la force avec laquelle elle excite l’oreille de l’auditeur. S

    # Le son qui engendre une vibration d’un corps physique, 
    # crée des variations de pression qui exercent une force sur les autres corps physiques en contact avec l’air (l’air étant un milieu dit « élastique »). 
    # Cette force n’étant pas constante (si elle l’est, il n’y a pas de son) le corps en question ne bouge pas mais vibre (si tant est qu’il ne soit pas trop rigide).

    # L’amplitude d’un signal est sa valeur maximale. 
    # Ici l’amplitude du signal qui varie entre la valeur +max et -max est +max. 
    # En somme, le maximum réel de la fonction sur un intervalle de temps donné. 
    # Dans le cas d’un signal sinusoïdal (tel que celui ci-dessus) on peut exprimer simplement la valeur efficace du signal par la formule suivante :

    # En fait, la valeur efficace, qui est très utilisée (parce que renvoyée par les instruments de mesures : 
    # un voltmètre par exemple) est la valeur quadratique moyenne. 
    # Par exemple si la valeur du signal en fonction du temps est donnée par la fonction Y(t) 
    # on a la formule générale suivante qui donne la valeur efficace du signal sur un intervalle de temps donné :

    # Valeur max et valeur efficace sont à mettre en relation avec ce que l’on appelle
    #  les puissances max et les puissances efficaces.
    #   Par exemple un amplificateur de puissance 100 W efficace (ou RMS) fournit une puissance crête (max) de 200W voire 400W sur des impulsions très brèves (s’il ne grille pas avant). 
    #   Cette puissance impulsionnelle qui ne veut pas dire grand chose est parfois indiquée comme étant la puissance Musicale de l’amplificateur.



    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
    # sample is a signed short in +/- 32768. 
    # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

pa = pyaudio.PyAudio()                                 #]
                                                       #|
stream = pa.open(format = FORMAT,                      #|
         channels = CHANNELS,                          #|---- You always use this in pyaudio...
         rate = RATE,                                  #|
         input = True,                                 #|
         frames_per_buffer = INPUT_FRAMES_PER_BLOCK)   #]

tap_threshold = INITIAL_TAP_THRESHOLD                  #]
noisycount = MAX_TAP_BLOCKS+1                          #|---- Variables for noise detector...
quietcount = 0                                         #|
errorcount = 0                                         #]         

for i in range(1000):
    try:                                                    #]
        block = stream.read(INPUT_FRAMES_PER_BLOCK)         #|
    except (IOError,e):                                      #|---- just in case there is an error!
        errorcount += 1                                     #|
        print( "(%d) Error recording: %s"%(errorcount,e) )  #|
        noisycount = 1                                      #]

    amplitude = get_rms(block) # Root mean Square va permettre de calculer l'amplitude d'un son en streaming
    print(amplitude)

    if amplitude > tap_threshold: # if its to loud... bruyant
        quietcount = 0
        noisycount += 1
        if noisycount > OVERSENSITIVE:
            tap_threshold *= 1.1 # turn down the sensitivity

    else: # if its to quiet...

        if 1 <= noisycount <= MAX_TAP_BLOCKS:
            print('tap!')
        noisycount = 0
        quietcount += 1
        if quietcount > UNDERSENSITIVE:
            tap_threshold *= 0.9 # turn up the sensitivity
