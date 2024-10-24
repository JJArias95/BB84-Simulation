# BB84 Simulation 

This repository is composed by two simulations of some parameters on the BB84 protocol.

## Simulation 1
It is a simulation of the a) distribution of bits in the raw key list, b) distribution of bases in the random bases list, c) distribution of matching and non-matching bases between Alice's and Bob's bases in the RanBases list, and d) distribution of Qbits in the Qbits list.

### a) Distribution of bits in the raw key list
A list of bits, referred to as the "RawKey", of length "NumBitsSim1" is generated for "NumSimSim1" simulations. In each simulation, the value of bit at each position of the "RawKey" list is checked to determine whether it is a one or a zero. This process results in a histogram of zeros and ones for each position in the "RawKey" list, obtained after performing all "NumSimSim1" simulations, 

### b) Distribution of bases in the random bases list
A list of random bases, referred to as the "AliceBases", of length "NumBitsSim1" is generated for "NumSimSim1" simulations. In each simulation, the basis at every position of the "AliceBases" list is checked to determine whether it is a rectilinear basis (Rec) or a diagonal basis (Dia). This process results in a histogram of Recs and Dias bases for each position in the "AliceBases" list, obtained after performing all "NumSimSim1" simulations.

### c) Distribution of matching and non-matching bases between Alice's and Bob's bases in the RanBases list
Two list of random bases, referred to as the "AliceBases" and "BobBases", of length "NumBitsSim1" are generated for "NumSimSim1" simulations. In each simulation, the matching of the basis in the both list are checked at every basis position to determine whether or not they match. This process results in a histogram of agree bases and disagree bases for each position in the "AliceBases" and "BobBases" lists, obtained after performing all "NumSimSim1" simulations.

### d) Distribution of Qbits in the Qbits list
Using a one-to-one relationship of each element, the "RawKey" list is encoded into Qbits using the "AliceBases" list. This generates a "Qbits" list of length "NumBitsSim1", which presents a distribution of 25% of each combination of Qbit. This process is realized for "NumSimSim1" simulations. In each simulation, the Qbit at each position of the "Qbits" list is checked. This process results in a histogram of Qbits for each position in the "Qbits" list, obtained after performing all "NumSimSim1" simulations.

## Simulation 2
It is a simulation of the Qber and Ber of a BB84 protocol with a $\lambda$ probability of a eavesdropper in the communication. The BB84 protocol is simulated "NumSimSim2" times. In each simulation, the raw key length is change from 90 to "NumBitsMax" in order to obatin the depedency of the Qber and Ber into the raw key length.

