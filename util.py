#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Imports
# =============================================================================
import pylab as pl


# =============================================================================
# Visualisation
# =============================================================================
def plotSignalT(time, signal, title):
    """
    Param:
        - time: array[float]
        - signal: array[int16]
        - title: string
    Returns:
        None
    """
    pl.grid()
    pl.xlabel('Temps en secondes')
    pl.ylabel('Amplitude du signal')
    pl.title(title)
    pl.plot(time, signal)
    pl.show()


def plotSignalF(frequency, signal, title):
    """
    Param:
        - time: array[float]
        - signal: array[int16]
    Returns:
        None
    """
    pl.grid()
    pl.xlabel('Fréquence en Hertz')
    pl.ylabel('Amplitude du signal')
    pl.title(title)
    pl.plot(frequency, signal)
    pl.show()

# =============================================================================
# Calcul
# =============================================================================
def nextpow2(x):
    """
    Param:
        - x: float
    Returns:
        - res : int
    """
    res = int(pl.ceil(pl.log2(x)))
    return res

def door(x, T):
    """
    Param:
        - x: float
        - T: float
    Returns:
        - res:int
    """
    res = 0
    if T/2 > x >= -T/2 :
        res = 1
    return res
    
def hamming(t, T):
    """
    Param:
        None
    Returns:
        - res: float
    """
    res = door(t, T)*(1+pl.cos(2*pl.pi*t/T))/2
    return res

def butterworth(f, fc):
    """
    Param:
        - f: float
        - fc: float
    Returns:
        - res: float
    """
    res = pl.sqrt(1+(f/fc)**4)
    return res

def meansquare(values):
    """
    Param:
        - values: array[float]
    Returns:
        - res: float
    """
    res = pl.sqrt(sum(value**2 for value in values)/len(values))
    return res
