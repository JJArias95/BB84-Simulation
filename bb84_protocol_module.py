import random 
from dictionaries_modules import *
import numpy as np

######## Generation of the raw key ########
def raw_key(numbits):
    return [random.choice([0,1]) for i in range(numbits)]

######## Generation of the bases ########
def random_bases(numbases):
    return [random.choice(["Rec","Dia"]) for i in range(numbases)]

######## Encoding the bits using the bases into Qbits ########
def encode(bits,bases):
    return [angles_polarization[bases[i]][bits[i]] for i in range(len(bits))]

######## Decoding the Qbits using the basis ########
def decode(angles,bases):
    bits=[]
    for i in range(len(angles)):
        if decode_angles[angles[i]][bases[i]]=="N/A":
            bits.append(random.choice([0,1]))
        else:
            bits.append(decode_angles[angles[i]][bases[i]])
    return bits

######## Bit error rate of two bits list. ########
def ber(Abits,Bbits):
    return sum(a != b for a, b in zip(Abits, Bbits))/ len(Abits)

######## Quantum bit error rate of two Qbits list. ########
def qber(Abits,Bbits,Abases,Bbases):
    QberAux = 0 
    matching_bases = 0 
    bits = len(Abits)
    for i in range(bits):
        if Abases[i] == Bbases[i]:
            matching_bases += 1
            if Abits[i] != Bbits[i]:
                QberAux += 1
    QBER = float(QberAux/matching_bases) if matching_bases > 0 else 0
    return QBER






    