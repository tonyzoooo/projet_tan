#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Imports
# =============================================================================
import wave
import pylab as pl

# =============================================================================
# Lecture 
# =============================================================================
def getData(filename="./resources/Ensoniq-ZR-76-Ocarina-C5.wav"):
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
        time = pl.linspace(0, duration, frames)        
        signal = data.readframes(-1) #lit les frames audio sous forme de bytes
        signal = pl.frombuffer(signal, "int32") #transforme les bytes en array
        freq = pl.fftfreq(frames, 1/rate)
        freq = pl.fftshift(freq)
        fourier = pl.fft(signal)
    return time, signal, freq, fourier


def plotSignalT(time, signal):
    """
    Param:
        - time: array[float]
        - signal: array[int32]
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
        - time (array(float)) : frequency
        - signal (array(int32)) : signal
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
# Estimation de la réponse fréquentielle
# =============================================================================



# =============================================================================
# Comparaison
# =============================================================================



# =============================================================================
# Classification
# =============================================================================



# =============================================================================
# Programme principal
# =============================================================================
if __name__ == '__main__':
    t, s, f, tf = getData()
    plotSignalT(t, s)
    plotSignalF(f, tf)