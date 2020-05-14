#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Imports
# =============================================================================
import os
import wave
from util import *

# =============================================================================
# Variables globales
# =============================================================================
T = 0.1 # duree du signal extrait initial
S = 4 #suréchantillonnage
fmax = 2500
fmin = 300
fc = 5000# fréquence de coupure

# =============================================================================
# Lecture 
# =============================================================================
def getData(filename="./resources/voyelles_non_nasalisées/a1.wav"):
    """
    Param:
        - filename: string
    Returns:
        - frames: int
        - rate: int
        - time: array[float]
        - signal: array[int32]
        - freq: array[float]
        - fourier: array[float]
    """
    with wave.open(filename, 'r') as data:
        frames = data.getnframes() #nombre d'échantillons
        rate = data.getframerate() #fréquence d'échantillonage
        duration = frames/rate #durée du signal
        time = pl.linspace(0, duration, frames)        
        signal = data.readframes(-1) #lit les frames audio sous forme de bytes
        signal = pl.frombuffer(signal, "int32") #transforme les bytes en array
    return frames, rate, time, signal

# =============================================================================
# Extraction
# =============================================================================
def extract(time, signal, fe):
    """
    Param:
        - time: array[float]
        - signal: array[int32]
        - fe: int
    Returns:
        - t: array[float]
        - res: array[int32]
    """
    startindex = len(signal)//10
    N = 2**nextpow2(T*fe)
    t = time[startindex:startindex+N].copy()-time[startindex]
    res = signal[startindex:startindex+N].copy()
    return t, res

# =============================================================================
# Fenêtrage
# =============================================================================
def windowedSig(signal):
    """
    Param:
        - signal: array[int32]
    Returns:
        - res: array[float]
    """
    res = signal.copy()
    N = len(signal)
    n = -N//2
    for i in range(N):
        res[i] *= hamming(n, N)
        n += 1
    return res

# =============================================================================
# Spectre
# =============================================================================
def spectrum(time, signal, fe):
    """
    Param:
        - time: array[float]
        - signal: array[int32]
        - fe: int
    Returns:
        - f: array[float]
        - res: array[int32]
    """
    N = len(signal)
    temp = pl.zeros(N*S)
    temp[:N] = signal
    f = pl.fftfreq(N*S, 1/fe)
    res = abs(pl.fft(temp))
    return f, res


def usefulSpectrum(Kmin, Kmax, frequency, signal):
    """
    Param:
        - Kmin: int
        - Kmax: int
        - frequency: array[float]
        - signal: array[float]
    Returns:
        - f: array[float]
        - res: array[float]
    """
    f = frequency[0:Kmax].copy()
    res = signal[0:Kmax].copy()
    res[:Kmin] =0
    return f, res

# =============================================================================
# Accentuation
# =============================================================================
def straighten(signal, fe):
    """
    Param:
        - signal: array[float]
    Returns:
        - res: array[float]
    """
    N = len(signal)
    res = pl.zeros(N)
    for k in range(N):
        kc = N*fc/fe
        res[k] = butterworth(k, kc)*signal[k]
    return res


# =============================================================================
# Lissage
# =============================================================================
def smoothing(signal, Kmin, Kmax):
    """
    Param:
        - signal: array[float]
        - Kmin: int
        - Kmax: int
    Returns:
        - res: array[float]
    """
    Q = 300
    N = len(signal)
    Sw = sum(hamming(q, Q) for q in range(-Q//2, Q//2))
    res = pl.zeros(N)
    for k in range(N):
        temp = 0
        for q in range(-Q//2, Q//2):
            if Kmax > k-q >= Kmin: 
                temp += hamming(q, Q)*signal[k-q]/Sw
        res[k] = temp        
    return res

# =============================================================================
# Récupération des données utiles
# =============================================================================
def extractRaw(signal, Kmin, Kmax):
    """
    Param:
        - signal: array[float]
        - Kmin: int
        - Kmax: int
    Returns: 
        - res: array[float]
    """
    res = pl.zeros(Kmax-Kmin)
    k = Kmin
    while k != Kmax:
        res[k-Kmin] = signal[k]
        k+=1
    return res

# =============================================================================
# Normalisation
# =============================================================================
def distance(H, Hm):
    """
    Param:
        - H: array[float]
        - Hm: array[float]
    Returns:
        - res: float
    """
    res = pl.sqrt(sum( (H[k]/meansquare(H) - Hm[k]/meansquare(Hm))**2 for k in range(len(H))))
    return res



# =============================================================================
# Classification
# =============================================================================
def nearestNeighbour(H, Hms):
    temp = dict()
    for key, value in Hms.items():
       temp.update({key : distance(H, value)})
    res = {k: v for k, v in sorted(temp.items(), key=lambda item: item[1])}
    return next(iter(res))

# =============================================================================
# Génération des exemples de comparaison
# =============================================================================
def H(filepath):
    N, fe, t, s = getData(filepath) #récupère les données
    new_t, new_s = extract(t, s, fe) #récupère une portion stable de données
    win_s = windowedSig(new_s) #multiplication par hamming
    f, dft = spectrum(new_t, win_s, fe)#fft
    new_N = len(dft)
    N_p = new_N
    delta_fp = fe/(N_p)
    Kmax = int(fmax/delta_fp)
    Kmin = int(fmin/delta_fp)
    new_f, new_dft = usefulSpectrum(Kmin, Kmax, f, dft)#récup données utiles
    last_dft = straighten(new_dft, fe) #accentuation
    latest_dft = smoothing(last_dft, Kmin, Kmax) #lissage
    rawValues = extractRaw(latest_dft, Kmin, Kmax) #récupère H non normalisé
    return rawValues
        
    
def examples():
    res = dict()
    for root, dirs, files in os.walk("./resources/Audio"):
        for name in files :
            if name.endswith(".wav"):
                filename = os.path.join(root, name)
                sound = name.split(".")[0]
                res.update({sound : H(filename)})
    return res
    

# =============================================================================
# Démonstration
# =============================================================================
def demo():
    N, fe, t, s = getData() #récupère les données
    new_t, new_s = extract(t, s, fe) #récupère une portion stable de données
    win_s = windowedSig(new_s) #multiplication par hamming
    f, dft = spectrum(new_t, win_s, fe)#fft
    new_N = len(dft)
    N_p = new_N
    delta_fp = fe/(N_p)
    Kmax = int(fmax/delta_fp)
    Kmin = int(fmin/delta_fp)
    new_f, new_dft = usefulSpectrum(Kmin, Kmax, f, dft)#récup données utiles
    last_dft = straighten(new_dft, fe) #accentuation
    latest_dft = smoothing(last_dft, Kmin, Kmax) #lissage
    rawValues = extractRaw(latest_dft, Kmin, Kmax) #récupère H non normalisé
    #### affichage
    pl.figure()
    plotSignalT(t, s, "Signal original")
    pl.figure()
    plotSignalT(new_t, new_s, "Signal extrait")
    pl.figure()
    plotSignalT(new_t, win_s, "Signal fenêtré")
    pl.figure()
    plotSignalF(f, dft, "Spectre du sig fenêtré")
    pl.figure()
    plotSignalF(new_f, new_dft, "Spectre extrait")
    pl.figure()
    plotSignalF(new_f, last_dft, "Spectre accentué")
    pl.figure()
    plotSignalF(new_f, latest_dft, "Spectre lissé")


# =============================================================================
# Programme principal
# =============================================================================
if __name__ == '__main__':
    
    filename = input("Chemin du fichier phonème à analyser : ")
    print("Génération des phonèmes types...")
    bank = examples()
    print("Calcul en cours...")
    rawValues = H(filename)
    print("Le phonème prononcé est : " + nearestNeighbour(rawValues, bank))
    