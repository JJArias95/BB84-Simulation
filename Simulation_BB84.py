# -*- coding: utf-8 -*
import numpy as np
import random
from bb84_protocol_module import *


def Parity(Abits): 
    return "Even" if sum(Abits) % 2 == 0 else "Odd"

def ParityComparator(AbitsMaj,AbitsMin,BbitsMaj,BbitsMin,NumSegj,kj):
    ParityValuesStep=[[],[]]

    for i in range(NumSegj):
        ParityValuesStep[0].append(Parity(AbitsMaj[i*kj:(i+1)*kj]))
        ParityValuesStep[1].append(Parity(BbitsMaj[i*kj:(i+1)*kj]))

    ParityValuesStep[0].append(Parity(AbitsMin))
    ParityValuesStep[1].append(Parity(BbitsMin))
    
    IndexBlock=[]
    for i in range(NumSegj+1):
        if ParityValuesStep[0][i]!=ParityValuesStep[1][i]:
            IndexBlock.append(i)
    print("IndexBlock: "+str(IndexBlock))
    return IndexBlock

def Binary(IndexStep,AbitsMaj,AbitsMin,BbitsMaj,BbitsMin,NumSegj,kj):
    ConVar=1
    substep=0
    print("\n\n")
    print("Substep: "+str(substep))
    ParitySubBlocksA=[[],[]]
    ParitySubBlocksB=[[],[]]
    FinalKeyBobStepA=[]
    FinalKeyBobStepB=[]
    print("\n")
    for q in IndexStep:
        if q!=NumSegj+1:
            Rl=kj
            BitsBlockqA=AbitsMaj[q*Rl:(q+1)*Rl]
            BitsBlockqB=BbitsMaj[q*Rl:(q+1)*Rl]
        else:
            Rl=len(BbitsMin)
            BitsBlockqA=AbitsMin
            BitsBlockqB=BbitsMin
        print("Rl: "+str(Rl))
        print("q: "+str(q))
        print("BitsBlockqA: "+str(BitsBlockqA))
        print("BitsBlockqB: "+str(BitsBlockqB))
        print("2q: "+str(2*q))
        print("BitsBlockqA[0:int(Rl/2)]: "+str(BitsBlockqA[0:int(Rl/2)]))
        print("Parity:"+str(Parity(BitsBlockqA[0:int(Rl/2)])))
        print("BitsBlockqB[0:int(Rl/2)]: "+str(BitsBlockqB[0:int(Rl/2)]))
        print("Parity:"+str(Parity(BitsBlockqB[0:int(Rl/2)])))
        print("1+2q: "+str(1+2*q))
        print("BitsBlockqA[int(Rl/2):Rl]: "+str(BitsBlockqA[int(Rl/2):Rl]))
        print("Parity:"+str(Parity(BitsBlockqA[int(Rl/2):Rl])))
        print("BitsBlockqB[int(Rl/2):Rl]: "+str(BitsBlockqB[int(Rl/2):Rl]))
        print("Parity:"+str(Parity(BitsBlockqB[int(Rl/2):Rl])))
        print("\n")


        ParitySubBlocksA[0].append(2*q)
        ParitySubBlocksA[1].append(Parity(BitsBlockqA[0:int(Rl/2)]))
        ParitySubBlocksA[0].append(1+2*q)
        ParitySubBlocksA[1].append(Parity(BitsBlockqA[int(Rl/2):Rl]))

        ParitySubBlocksB[0].append(2*q)
        ParitySubBlocksB[1].append(Parity(BitsBlockqB[0:int(Rl/2)]))
        ParitySubBlocksB[0].append(1+2*q)
        ParitySubBlocksB[1].append(Parity(BitsBlockqB[int(Rl/2):Rl]))
    
    SubDisagreeParityBlocks=[]
    for i in range(len(ParitySubBlocksB[0])):
        if ParitySubBlocksB[1][i]!=ParitySubBlocksA[1][i]:
            print(ParitySubBlocksB[0][i])
            SubDisagreeParityBlocks.append(ParitySubBlocksB[0][i])
    print("SubDisagreeParityBlocks: "+str(SubDisagreeParityBlocks))
    AFinalKey=AbitsMaj+AbitsMin
    BFinalKey=BbitsMaj+BbitsMin

    if locals().get('Rl') is not None:
        while ConVar:
            print("\n\n")
            print("Substep: "+str(substep+1))
            ParitySubBlocksA=[[],[]]
            ParitySubBlocksB=[[],[]]
            Rl=int(Rl*0.5)
            for q in SubDisagreeParityBlocks:
                # if substep>1:
                #     if q%2!=0: 
                #         Rl=Rl-int(Rl*0.5)
                # else:
                #     Rl=int(Rl*0.5)
                BitsBlockqA=AFinalKey[q*Rl:(q+1)*Rl]
                BitsBlockqB=BFinalKey[q*Rl:(q+1)*Rl]

                ParitySubBlocksA[0].append(2*q)
                ParitySubBlocksA[1].append(Parity(BitsBlockqA[0:int(Rl/2)]))
                ParitySubBlocksA[0].append(1+2*q)
                ParitySubBlocksA[1].append(Parity(BitsBlockqA[int(Rl/2):Rl]))

                ParitySubBlocksB[0].append(2*q)
                ParitySubBlocksB[1].append(Parity(BFinalKey[0:int(Rl/2)]))
                ParitySubBlocksB[0].append(1+2*q)
                ParitySubBlocksB[1].append(Parity(BFinalKey[int(Rl/2):Rl]))
                print("Rl: "+str(Rl))
                print("q: "+str(q))
                print("BitsBlockqA: "+str(BitsBlockqA))
                print("BitsBlockqB: "+str(BitsBlockqB))
                print("2q: "+str(2*q))
                print("BitsBlockqA[0:int(Rl/2)]: "+str(BitsBlockqA[0:int(Rl/2)]))
                print("Parity:"+str(Parity(BitsBlockqA[0:int(Rl/2)])))
                print("BitsBlockqB[0:int(Rl/2)]: "+str(BitsBlockqB[0:int(Rl/2)]))
                print("Parity:"+str(Parity(BitsBlockqB[0:int(Rl/2)])))
                print("1+2q: "+str(1+2*q))
                print("BitsBlockqA[int(Rl/2):Rl]: "+str(BitsBlockqA[int(Rl/2):Rl]))
                print("Parity:"+str(Parity(BitsBlockqA[int(Rl/2):Rl])))
                print("BitsBlockqB[int(Rl/2):Rl]: "+str(BitsBlockqB[int(Rl/2):Rl]))
                print("Parity:"+str(Parity(BitsBlockqB[int(Rl/2):Rl])))
                print("\n")

            substep+=1
            SubDisagreeParityBlocks=[]
            for i in range(len(ParitySubBlocksB[0])):
                if ParitySubBlocksB[1][i]!=ParitySubBlocksA[1][i]:
                    print(ParitySubBlocksB[0][i])
                    SubDisagreeParityBlocks.append(ParitySubBlocksB[0][i])

            print("SubDisagreeParityBlocks: "+str(SubDisagreeParityBlocks))

            if len(BitsBlockqB[0:int(Rl/2)])==1 or len(BitsBlockqB[int(Rl/2):Rl])==1:
                for k in SubDisagreeParityBlocks:
                    if BFinalKey[k]==0:
                        BFinalKey[k]=1
                    else:
                        BFinalKey[k]=0
                
                for l in range(len(BFinalKey)):
                    FinalKeyBobStepA.append(AFinalKey[l])
                    FinalKeyBobStepB.append(BFinalKey[l])
                ConVar=0
            else:
                ConVar=1
    return FinalKeyBobStepA,FinalKeyBobStepB




NumBits=2**(11)
ProbEve=0 
ProbDesPol=0.041
fracSiftingKey=0.37

#Alice
AliceRanBases=random_base(NumBits)
AliceBits=raw_key(NumBits)
AlicePolarStates=encode(AliceBits,AliceRanBases)

if random.uniform(-(1-ProbEve),ProbEve)>0:
    #Fibra optica
    DesPolAlicePolarStates=depolarization(AlicePolarStates,ProbDesPol,"-")
    #Eve
    EveRanBases=random_base(NumBits)
    EveBits=decode(DesPolAlicePolarStates,EveRanBases)
    EvePolarStates=encode(EveBits,EveRanBases)
    #Fibra optica        
    DesPolEvePolarStates=depolarization(EvePolarStates,ProbDesPol,"-")
else:
    DesPolEvePolarStates=depolarization(AlicePolarStates,ProbDesPol,"-")
    
#Bob
BobRanBases=random_base(NumBits)
BobBits=decode(DesPolEvePolarStates,BobRanBases)

BerAliceBob=ber(AliceBits,BobBits)
QberAliceBob=qber(AliceBits,BobBits,AliceRanBases,BobRanBases)

###################
##### Sifting #####
###################
AliceSiftingKey=bit_agree(AliceBits,AliceRanBases,BobRanBases)
BobSiftingKey=bit_agree(BobBits,AliceRanBases,BobRanBases)

Qber,AliceFinalKey,BobFinalKey=bits_qber_selector(AliceSiftingKey,BobSiftingKey,fracSiftingKey)

Qber100=ber(AliceFinalKey,BobFinalKey)
print("Qber100:"+str(Qber100))

##################################
######## Cascade protocol ########
##################################

print("bits: "+str(len(AliceFinalKey)))
# if 0<Qber100<0.23:
#     ## Esto es para calcular el K1 ##
#     k1=int(np.ceil(0.73/Qber100))
#     ### Limit steps of Cascade protocol is given by ki<=LimitK
#     LimitK=len(BobFinalKey)/2
#     MaxStep=int(np.log2(LimitK*Qber100/0.73))+1
            
#     MaxStep=2
#     Qbers=[Qber100]
#     NumErrorBits=[Qber100*len(BobFinalKey)]
            
#     print("int(len(AliceFinalKey)/k1): "+str(len(AliceFinalKey)/k1))
#     print("k1: "+str(k1))
#     MaxStep=1 
    
    
#     for step in range(MaxStep):
#         kj=(2**step)*k1
#         NumSegj=int(len(AliceFinalKey)/kj)
#         for u in range(NumSegj+1):
#             if u<NumSegj:
#                 AliceKeyAuxMaj=AliceFinalKey[u*kj:(u+1)*kj]
#                 BobKeyAuxMaj=BobFinalKey[u*kj:(u+1)*kj]
#                 print("NumSegj: "+str(u))
#                 print("AliceKeyAuxMaj: "+str(AliceKeyAuxMaj))
#                 print("Parity: "+str(Parity(AliceKeyAuxMaj)))
#                 print("BobKeyAuxMaj: "+str(BobKeyAuxMaj))
#                 print("Parity: "+str(Parity(BobKeyAuxMaj)))
#                 print("\n")
#             else:
#                 AliceKeyAuxMin=AliceFinalKey[NumSegj*kj:]
#                 BobKeyAuxMin=BobFinalKey[NumSegj*kj:]
#                 print("NumSegj: "+str(u))
#                 print("AliceKeyAuxMin: "+str(AliceKeyAuxMin))
#                 print("Parity: "+str(Parity(AliceKeyAuxMin)))
#                 print("BobKeyAuxMin: "+str(BobKeyAuxMin))
#                 print("Parity: "+str(Parity(BobKeyAuxMin)))
#                 print("\n")


#         if step!=0:
#             AliceFinalKey,BobFinalKey=ran_per(AliceFinalKey,BobFinalKey,5*NumSegj)
        
#         AliceKeyMaj=AliceFinalKey[:NumSegj*kj]
#         AliceKeyMin=AliceFinalKey[NumSegj*kj:]

#         BobKeyMaj=BobFinalKey[:NumSegj*kj]
#         BobKeyMin=BobFinalKey[NumSegj*kj:]
        
#         IndexStep=ParityComparator(AliceKeyMaj,AliceKeyMin,BobKeyMaj,BobKeyMin,NumSegj,kj)
#         AliceFinalKey,BobFinalKey=Binary(IndexStep,AliceKeyMaj,AliceKeyMin,BobKeyMaj,BobKeyMin,NumSegj,kj)

#         QberStep=ber(AliceFinalKey,BobFinalKey)

#         Qbers.append(QberStep)
#         NumErrorBits.append(QberStep*len(BobFinalKey))

#         print("Qbers: "+str(Qbers))
#         print("NumErrorBits: "+str(NumErrorBits))



if 0<Qber100<0.23:
    ## Esto es para calcular el K1 ##
    k1=int(np.ceil(0.73/Qber100))
    print("Valor de k1 antes:"+str(k1))
    
    Qberbefore=ber(AliceFinalKey,BobFinalKey)
    print("Qberbefore: "+str(Qberbefore))

    ### Esto es para sacar el numeros maximo de 
    ### pasos que se puede hacer el protocolo 
    ### cascada cumpliendo que ki<=lengthKey/2
    LimitK=len(AliceFinalKey)/2
    MaxStep=int(np.log2(LimitK*Qber100/0.73))
    ###

    print("MaxStep: "+str(MaxStep))
    Qbers=[Qberbefore]
    for step in range(MaxStep+1):
        print("step: "+str(step))
        kj=(2**step)*k1
        print("kj: "+str(kj))
        NumSegj=int(len(AliceFinalKey)/kj)
        if step==0:
            AliceKeyMaj=AliceFinalKey[:NumSegj*kj]
            AliceKeyMin=AliceFinalKey[NumSegj*kj:]

            BobKeyMaj=BobFinalKey[:NumSegj*kj]
            BobKeyMin=BobFinalKey[NumSegj*kj:]
        else:
            AliceKeyKj,BobKeyKj=ran_per(AliceKeyKj,BobKeyKj,5*NumSegj)

            AliceKeyMaj=AliceKeyKj[:NumSegj*kj]
            AliceKeyMin=AliceKeyKj[NumSegj*kj:]

            BobKeyMaj=BobKeyKj[:NumSegj*kj]
            BobKeyMin=BobKeyKj[NumSegj*kj:]

        ParDisMay=parity_disagree_maj(AliceKeyMaj,BobKeyMaj,kj)
        ParAliceKeyMin=parity(AliceKeyMin)
        ParBobKeyMin=parity(BobKeyMin)

        if step==0:
            print("len(ParDisMay): "+str(len(ParDisMay)))
        if Qbers[step]!=0:
            ## Solo se pone esto por que la funcion BusqBinaryMay modifica directamente a EE0 y EE1 solamente con llamarla #
            busq_binary_may(AliceKeyMaj,BobKeyMaj,ParDisMay,kj)
            #################################################################################################################
            ## Solo se pone esto por que la funcion BusqBinaryMin modifica directamente a EE2 y EE3 solamente con llamarla ##
            busq_binary_min(AliceKeyMin,BobKeyMin,ParAliceKeyMin,ParBobKeyMin)
            #################################################################################################################
        else:
            break
            
        AliceKeyKj=AliceKeyMaj+AliceKeyMin
        BobKeyKj=BobKeyMaj+BobKeyMin
        Qbers.append(ber(AliceKeyKj,BobKeyKj))

    AliceFinalKey=AliceKeyKj
    AliceFinalKey=BobKeyKj

    Qbers2=[]
    Qbers3=[]
    for i in range(0,len(Qbers)-1):
        Qbers2.append(100*(Qberbefore-Qbers[i])/Qberbefore)
        Qbers3.append(100*(Qbers[i]-Qbers[i+1])/Qbers[i])
        
    print("\n")
    print("QBER: "+str(Qbers))
    print("Qberafter: "+str(Qbers[-1]))
    print("len: "+str(len(AliceFinalKey)))
elif Qber==0.0:
    print("There is no error in the key.")
else:
    print("There is an eavesdropper. Abort the communication!")



