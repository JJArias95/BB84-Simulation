import random 
from dictionaries_modules import *
import numpy as np

######## Generation of the raw key ########
def raw_key(numbits):
    return [random.choice([0,1]) for i in range(numbits)]

######## Generation of the bases ########
def random_bases(numbases):
    return [random.choice(["Rec","Dia"]) for i in range(numbases)]

def encode(bits,bases):
    return [angles_polarization[bases[i]][bits[i]] for i in range(len(bits))]

def decode(angles,bases):
    bits=[]
    for i in range(len(angles)):
        if decode_angles[angles[i]][bases[i]]=="N/A":
            bits.append(random.choice([0,1]))
        else:
            bits.append(decode_angles[angles[i]][bases[i]])
    return bits


############################################
########## Error Diferentes a Eve ##########
############################################
##Errores por problema de Despolarización al rotar la polarización un angulo 45 grados en sentido contrario (Sen="-") o en sentido (Sen="+") 
##a las manecillas del reloj. b es la probabilidad de que surga el error de polarizacion 
def depolarization(PolState,ProbDesPol=0.1,sen="-"):
    DepolState=[]
    PolStatelon=len(PolState)
    for i in range(PolStatelon):
        if random.uniform(ProbDesPol-1,ProbDesPol)>0:
            if PolState[i]==0:
                DepolAuxMinus=45
                DepolAuxPlus=135
            elif PolState[i]==90:
                DepolAuxMinus=135
                DepolAuxPlus=45
            elif PolState[i]==45:
                DepolAuxMinus=90
                DepolAuxPlus=0
            else:
                DepolAuxMinus=0
                DepolAuxPlus=90

            if sen=="-":
                DepolState.append(DepolAuxMinus)
            else:
                DepolState.append(DepolAuxPlus)
        else:
            DepolState.append(PolState[i])
    return DepolState

############################################
################ Sifting ###################
############################################

# Recordar que el Qber solo se saca con los bits con bases que 
# concuerdan y el Ber se saca con el total de los bits de la Rawkey
# En realidad el Qber y el Ber se saca de forma muy parecido con la 
# diferencia de que el Qber es el Ber calculado con los bits de la base
# que coincide.

def ber(Abits,Bbits):
    BerAux=0
    bits=len(Abits)
    for i in range(bits):
        if Abits[i]!=Bbits[i]:
            BerAux+=1
    BER=float(BerAux/bits)
    return BER


def qber(Abits,Bbits,Abases,Bbases):
    QberAux=0
    base=0
    bits=len(Abits)
    for i in range(bits):
        if Abases[i]==Bbases[i]:
            base+=1
            if Abits[i]!=Bbits[i]:
                QberAux+=1
    QBER=float(QberAux/base)
    return QBER



#this select only the bits that its bases agree
def bit_agree(Bits,ABases,BBases):
    NumBits=len(Bits)
    BitsAgree=[]
    for i in range(NumBits):
        if ABases[i]==BBases[i]:
            BitsAgree.append(Bits[i])
    return BitsAgree


# El A es la key despues de haber separado los bits de las bases que 
# agree de la funcion bit agree y el b es el porcentaje de bits de 
# esa key que se quiere usar para hallar el Qber. Esta funcion toma 
# de forma aleatoria len(A)*b de los bits donde la bases concuerdan

def index_random(lensiftbits,fractionbits):
    NumIndex=int(np.ceil(lensiftbits*fractionbits))
    index=[]
    for i in range(NumIndex):
        r=random.randint(0,lensiftbits-1)
        while r in index:
            r=random.randint(0,lensiftbits-1)
        index.append(r)
    index.sort() 
    return index


def sel_bit_random(SiftingKey,Index):
    return [SiftingKey[l] for l in Index]

def remove_bit(siftingkey,index):
    siftingkeylen=len(siftingkey)
    key=[]
    for j in range(siftingkeylen):
        if not j in index:
            key.append(siftingkey[j])
    return key
    
def bits_qber_selector(Asiftingkey,Bsiftingkey,perc):
    lenA=len(Asiftingkey)
    LenUnCoveredbits=int(np.ceil(perc*lenA))
    index=[]
    AFinalKey=[]
    BFinalKey=[]
    QberAux=0
    for i in range(LenUnCoveredbits):
        r=random.randint(0,lenA-1)
        while r in index:
            r=random.randint(0,lenA-1)   
        index.append(r)
    index.sort() 
    for k in range(lenA):
        if k in index:
            if Asiftingkey[k]!=Bsiftingkey[k]:
                QberAux+=1

        if not k in index:
            AFinalKey.append(Asiftingkey[k])
            BFinalKey.append(Bsiftingkey[k])

    Qber=QberAux/len(index)
    return Qber,AFinalKey,BFinalKey

#######################################################
##################### Cascade #########################
#######################################################
def parity_disagree_maj(Abits,Bbits,kj):
    bits=len(Abits)
    ParDisagree=[]
    AbitsAux=[]
    BbitsAux=[]
    for i in range(bits):
        AbitsAux.append(Abits[i])
        BbitsAux.append(Bbits[i])
    N_Seg=int(bits/kj)
    print("N_Seg: "+str(N_Seg))
    for i in range(N_Seg):
        ParAuxA=AbitsAux[i*kj:(i+1)*kj]
        ParA=parity(ParAuxA)
        ParAuxB=BbitsAux[i*kj:(i+1)*kj]
        ParB=parity(ParAuxB)
        if ParA!=ParB:
            ParDisagree.append(i)
    return ParDisagree

def parity(Abits): 
    return "Even" if sum(Abits) % 2 == 0 else "Odd"

def busq_binary_may(Abits,Bbits,ParDisBlock,kj):
    for q in ParDisBlock:
        Rl=kj
        blockq=q
        AbitsBlock=Abits[blockq*Rl:(blockq+1)*Rl]
        BbitsBlock=Bbits[blockq*Rl:(blockq+1)*Rl]
        blocksq=[]
        RlValues=[]
        while len(AbitsBlock)!=1:
            blocksq.append(blockq)
            RlValues.append(int(Rl))

            DisParBlockBinary=busq_binary_may2(AbitsBlock,BbitsBlock,Rl,int(Rl*0.5))
            blockq=DisParBlockBinary       

            AbitsBlock=AbitsBlock[blockq*int(Rl*0.5):int((blockq+1)*Rl*0.5)]
            BbitsBlock=BbitsBlock[blockq*int(Rl*0.5):int((blockq+1)*Rl*0.5)]

            if blockq==1: 
                Rl=Rl-int(Rl*0.5)
            else:
                Rl=int(Rl*0.5)

            if len(AbitsBlock)==1:
                blocksq.append(blockq)
                RlValues.append(int(Rl))
            
        Index2=0
        for i in range(len(blocksq)):
            if i==0:
                Index2+=blocksq[i]*RlValues[i]
            else:
                Index2+=blocksq[i]*(RlValues[i-1]-RlValues[i])

        if Abits[Index2]!=Bbits[Index2]:
            Bbits[Index2]=Abits[Index2]
        else:
            print("There is a mistake")
    return Abits, Bbits

def busq_binary_may2(Abits,Bbits,Rl,halfRl):
    lenAbits=len(Abits)
    ParAbits=[]
    ParBbits=[]
    AbitsAux=[]
    BbitsAux=[]
    for i in range(lenAbits):
        AbitsAux.append(Abits[i])
        BbitsAux.append(Bbits[i])

    ParAbits.append(parity(AbitsAux[0:halfRl]))
    ParAbits.append(parity(AbitsAux[halfRl:Rl]))

    ParBbits.append(parity(BbitsAux[0:halfRl]))
    ParBbits.append(parity(BbitsAux[halfRl:Rl]))       

    if ParAbits[0]!=ParBbits[0]:
        DisPar=0
    elif ParAbits[1]!=ParBbits[1]:
        DisPar=1

    return DisPar

def busq_binary_min(Abits,Bbits,ParAbits,ParBbits):
    if ParAbits!=ParBbits:
        AbitsBlock=Abits
        BbitsBlock=Bbits
        blockq=0
        lenABits=len(Abits)
        blocksq=[]
        lenABitsValues=[]
        while len(AbitsBlock)!=1:
            blocksq.append(blockq)
            lenABitsValues.append(lenABits)
            DisParBlockBinary=busq_binary_may2(AbitsBlock,BbitsBlock,lenABits,int(lenABits*0.5))
            blockq=DisParBlockBinary      
            AbitsBlock=AbitsBlock[blockq*int(lenABits*0.5):int((blockq+1)*lenABits*0.5)]
            BbitsBlock=BbitsBlock[blockq*int(lenABits*0.5):int((blockq+1)*lenABits*0.5)]
            if blockq==1: 
                lenABits=lenABits-int(lenABits*0.5)
            else:
                lenABits=int(lenABits*0.5)
            if len(AbitsBlock)==1:
                blocksq.append(blockq)
                lenABitsValues.append(lenABits)
        Index22=0
        for i in range(len(blocksq)):
            if i==0:
                Index22+=blocksq[i]*lenABitsValues[i]
            else:
                Index22+=blocksq[i]*(lenABitsValues[i-1]-lenABitsValues[i])
        if Abits[Index22]!=Bbits[Index22]:
            Bbits[Index22]=Abits[Index22]
        else:
            print("Thre is a mistake")
    return Abits, Bbits

def ran_per(Abits,Bbits,NumPer):
    lenAbits=len(Abits)
    AbitsAux=[]
    BbitsAux=[]
    for i in range(lenAbits):
        AbitsAux.append(Abits[i])
        BbitsAux.append(Bbits[i])

    for i in range(NumPer):
        firstindex = int(np.ceil(random.uniform(0,lenAbits-1)))
        secondindex = int(np.ceil(random.uniform(0,lenAbits-1)))
        while secondindex==firstindex:
            secondindex = int(np.ceil(random.uniform(0,lenAbits-1)))

        AbitsAux1=AbitsAux[firstindex]
        AbitsAux2=AbitsAux[secondindex]
        AbitsAux[firstindex]=AbitsAux2
        AbitsAux[secondindex]=AbitsAux1

        BbitsAux1=BbitsAux[firstindex]
        BbitsAux2=BbitsAux[secondindex]
        BbitsAux[firstindex]=BbitsAux2
        BbitsAux[secondindex]=BbitsAux1

    return AbitsAux,BbitsAux

##########################################################################
##########################################################################
##########################################################################

    