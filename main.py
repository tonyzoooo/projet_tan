#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Imports
# =============================================================================
import wave
import pylab as pl
import scipy as sc
import os

# =============================================================================
# Variables globales
# =============================================================================

S = 4
# =============================================================================
# Lecture 
# =============================================================================
def getData(filename="./resources/voyelles_non_nasalisées/a1.wav"):
    """
    Param:
        - filename: string
    Returns:
        - time: array[float]
        - signal: array[int32]
        - freq: array[float]
        - fourier: array[float]
    """
    with wave.open(filename, 'r') as data:
        frames = data.getnframes() #nombre d'échantillons
        rate = data.getframerate() #fréquence d'échantillonage
        duration = frames/rate #durée du signal
        time = pl.linspace(0, duration, S)        
        signal = data.readframes(-1) #lit les frames audio sous forme de bytes
        signal = pl.frombuffer(signal, "int32") #transforme les bytes en array
        window = pl.hamming(frames)
        res = signal*window
        freq = pl.fftfreq(S*frames, 1/rate)
        fourier = abs(sc.fft.fft(res, S*frames))
    return frames, rate, time, res, freq, fourier


def plotSignalT(time, signal):
    """
    Param:
        - time: array[float]
        - signal: array[int16]
    Returns:
        None
    """
    pl.figure("Temporel")
    pl.grid()
    pl.xlabel('Temps en secondes')
    pl.ylabel('Amplitude du signal')
    pl.title("Signal audio dans le domaine temporel")
    pl.plot(time, signal)
    pl.show()


def plotSignalF(frequency, signal):
    """
    Param:
        - time: array[float]
        - signal: array[int16]
    Returns:
        None
    """
    pl.figure("Fréquentiel")
    pl.grid()
    pl.xlabel('Fréquence en Hertz')
    pl.ylabel('Amplitude du signal')
    pl.title("Signal audio dans le domaine fréquentiel")
    pl.plot(frequency, signal)
    pl.show()


# =============================================================================
# Extraction
# =============================================================================
def extract(frequency, signal):
    """
    extrait signal de 200 à 4000 Hz
    """
    res = []
    f = []
    for i in range(len(frequency)) :
        if frequency[i] >= 0:
            res.append(signal[i])
            f.append(frequency[i])
        elif frequency[i] > 2600:
            break
    return res, f

def weightedSignal(signal):
    Q = 2*30
    l = len(signal)
    print(l)
    coef = 0
    newSignal = [0]*l
    temp = 0
    for i in range(0,l):
        for j in range(-Q//2,Q//2-1):
            if (i-j)<0 or (i-j)>=l<0:
                coef = 0
            else:
                coef = signal[i-j]
            temp+=ponderation(Q,j)*coef
        newSignal[i] = temp
        temp=0
    return newSignal
    
def ponderation(Q,k):
    res=0
    for i in range(-Q//2,Q//2-1):
        res+=hamming(i,Q)
    return hamming(k,Q)/res


def findMaxFrequency(frequency, signal):
    s,f = extract(frequency, signal)
    maxAmp = max(s)
    threshold = 0.5*maxAmp/100
    fmax = 0
    for i in range(0,len(f)):
        if s[i] > threshold :
            fmax = f[i]
    return fmax

def findMinFrequency(frequency, signal):
    s,f = extract(frequency, signal)
    maxAmp = max(s)
    threshold = 0.5*maxAmp/100
    fmin = 0
    for i in range(len(s)-1, 0, -1):
        if s[i] > threshold :
            fmin = f[i]
    
    return fmin

def getK(f, deltaF):
    return round(f/deltaF)

def extractRaw(signal,Kmin,Kmax):
    res = []
    for i in range(len(signal)) :
        if(i > Kmin and i < Kmax) :
            res.append(signal[i])
    return res


# =============================================================================
# Normalisation
# =============================================================================

def normalValues(H):
    res = []
    meansquare = 0
    for element in H:
        meansquare += element
    meansquare = pl.sqrt(meansquare)
    for element in H :
        res.append(element/meansquare)
    return res

def hamming(q,Q):
    return (1+pl.cos(2*pl.pi*q/Q)/2)
    
def normalDistance(H, Hm, Kmin, Kmax):
    sum = 0
    for k in range(int(Kmin), int(Kmax)):
        sum+= (H[k]-Hm[k])**2
    res = pl.sqrt(sum)
    return  res



# =============================================================================
# Estimation de la réponse fréquentielle
# =============================================================================

# =============================================================================
# Comparaison
# =============================================================================



# =============================================================================
# Classification
# =============================================================================



def H(name):
    N, fe, t, s, f, tf = getData(name)
    N_prime = S*N   
    fmax = findMaxFrequency(f, tf)
    fmin = findMinFrequency(f, tf)
    plotSignalF(f, tf)
    deltaF = fe/N_prime
    Kmax = getK(fmax, deltaF)
    Kmin = getK(fmin, deltaF)
    rawValues = extractRaw(s,Kmin,Kmax)
    normalRawValues = normalValues(rawValues)
    return normalRawValues
# =============================================================================
# Programme principal
# =============================================================================
if __name__ == '__main__':
    N, fe, t, s, f, tf = getData()
    tf_eq = weightedSignal(tf)
    plotSignalF(f,tf_eq)
"""
    audios = dict()
    for root, dirs, files in os.walk("./resources/Audio"):
        for name in files:
            print(name)
            audios[name] = H("./resources/Audio/"+name)

    N, fe, t, s, f, tf = getData()
    N_prime = S*N
    print(fe)
    #plotSignalT(t, s)
    plotSignalF(f, tf)
    
    fmax = findMaxFrequency(f, tf)
    fmin = findMinFrequency(f, tf)
    deltaF = fe/N_prime
    Kmax = getK(fmax, deltaF)
    Kmin = getK(fmin, deltaF)
    print("fmin :"+str(fmin))
    print("fmax :"+str(fmax))
    print("Kmin :"+str(Kmin))
    print("Kmax :"+str(Kmax))

    rawValues = extractRaw(s,Kmin,Kmax)
    normalRawValues = normalValues(rawValues)
    

"""