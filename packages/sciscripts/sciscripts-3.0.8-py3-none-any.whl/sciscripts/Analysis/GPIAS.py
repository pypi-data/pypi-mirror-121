#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170612
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[Analysis.GPIAS] Loading dependencies...')
import numpy as np
from scipy import signal

from sciscripts.Analysis import Analysis as sAnalysis
from sciscripts.IO import IO
print('[Analysis.GPIAS] Done.')


## Level 0
def CheckGPIASRecs(Data, SizeLimits, Plot=False):
    ToCheck = [Rec for Rec in Data.keys()
                   if len(Data[Rec])<min(SizeLimits)
                   or len(Data[Rec])>max(SizeLimits)]

    if ToCheck:
        if Plot:
            Params = {'backend': 'TkAgg'}
            from matplotlib import rcParams; rcParams.update(Params)
            import matplotlib.pyplot as plt

            for Rec in ToCheck:
                print('Showing Rec', Rec+', size', Data[Rec].shape[0])
                plt.plot(Data[Rec])
                plt.show()

        return(ToCheck)
    else:
        print('All recs within expected size.')
        return(None)


def ConvertIndexesToArray(Indexes):
    Array = {'Exps': [], 'Animals': [], 'Freqs': [], 'Index':[]}
    for E, Exp in Indexes.items():
        for A, Animal in Exp.items():
            for Freq, Index in Animal.items():
                Array['Exps'].append(E)
                Array['Animals'].append(A)
                Array['Freqs'].append(Freq)
                Array['Index'].append(Index)

    for K in Array.keys(): Array[K] = np.array(Array[K])
    return(Array)


def ConvertTracesToArray(Traces):
    Array = {'Exps': [], 'Animals': [], 'Freqs': [], 'Traces':[], 'ColOrder':[]}
    ColOrder = ['NoGap', 'Gap']
    for E, Exp in Traces.items():
        for A, Animal in Exp.items():
            for Freq, Trace in Animal.items():
                Array['Exps'].append(E)
                Array['Animals'].append(A)
                Array['Freqs'].append(Freq)
                Array['ColOrder'].append(ColOrder)

                ATrace = np.zeros((Trace['Gap'].shape[0],2), Trace['Gap'].dtype)
                for i in range(2):
                    Trace[ColOrder[i]] = Trace[ColOrder[i]].reshape(Trace[ColOrder[i]].shape[0])
                    ATrace[:,i] = Trace[ColOrder[i]]

                Array['Traces'].append(ATrace)

    for K in [_ for _ in Array.keys() if _ != 'Traces']: Array[K] = np.array(Array[K])
    return(Array)


def GetExpsIndexesDict(Exps, Verbose=False):
    """
    Get index per freq per animal per exp.
    Necessary for retest overriding (the last tested is always the correct one).
    """
    Indexes_IFAE, Traces_IFAE = {}, {}
    for E, Exp in Exps.items():
        if E not in Indexes_IFAE: Indexes_IFAE[E], Traces_IFAE[E] = {}, {}

        for File in sorted(Exp):
            GPIASRec = IO.Bin.Read(File, Verbose=Verbose)[0]
            if 'XValues' in GPIASRec:
                # Backward compatibility
                GPIASRec['X'] = GPIASRec.pop('XValues')

            GPIASRec, X = GPIASRec['GPIAS'], GPIASRec['X']
            Animal = File.split('/')[-1].split('-')[1]
            if Animal not in Indexes_IFAE[E]:
                Indexes_IFAE[E][Animal], Traces_IFAE[E][Animal] = {}, {}

            Indexes_IFAE[E][Animal] = {**Indexes_IFAE[E][Animal],
                                             **{K: sAnalysis.GetNegEquiv(V['GPIASIndex'])
                                                for K, V in GPIASRec['Index'].items()}}
            Traces_IFAE[E][Animal] = {**Traces_IFAE[E][Animal], **GPIASRec['Trace']}

    Indexes_IFAE = ConvertIndexesToArray(Indexes_IFAE)
    Traces_IFAE = ConvertTracesToArray(Traces_IFAE)

    return(Indexes_IFAE, Traces_IFAE, X)


def GetExpsIndexesDict_InDev(Exps, Verbose=False):
    """
    Get index per freq per animal per exp.
    Necessary for retest overriding (the best tested is always the correct one).
    """
    Indexes_IFAE, Traces_IFAE = {}, {}
    for E, Exp in Exps.items():
        if E not in Indexes_IFAE: Indexes_IFAE[E], Traces_IFAE[E] = {}, {}

        for File in sorted(Exp):
            GPIASRec = IO.Bin.Read(File, Verbose=Verbose)[0]
            if 'XValues' in GPIASRec:
                # Backward compatibility
                GPIASRec['X'] = GPIASRec.pop('XValues')

            GPIASRec, X = GPIASRec['GPIAS'], GPIASRec['X']
            Animal = File.split('/')[-1].split('-')[1]
            if Animal not in Indexes_IFAE[E]:
                Indexes_IFAE[E][Animal], Traces_IFAE[E][Animal] = {}, {}

            Dict = {K: sAnalysis.GetNegEquiv(V['GPIASIndex']) for K, V in GPIASRec['Index'].items()}
            for K in Dict:
                if K in Indexes_IFAE[E][Animal]:
                    if Dict[K] < Indexes_IFAE[E][Animal][K]:
                        print(Indexes_IFAE[E][Animal][K], Dict[K])
                        Indexes_IFAE[E][Animal][K] = Dict[K]
                else:
                    Indexes_IFAE[E][Animal][K] = Dict[K]

            # Indexes_IFAE[E][Animal] = {**Indexes_IFAE[E][Animal], **Dict}

            Traces_IFAE[E][Animal] = {**Traces_IFAE[E][Animal], **GPIASRec['Trace']}

    Indexes_IFAE = ConvertIndexesToArray(Indexes_IFAE)
    Traces_IFAE = ConvertTracesToArray(Traces_IFAE)

    return(Indexes_IFAE, Traces_IFAE, X)


def GetMAF(Indexes_IFAE, Animals, ExpOrder):
    MAF = []
    for Animal in Animals:
        ## Indexes_IFAE as array
        ThisAnimal = Indexes_IFAE['Animals'] == Animal

        Freqs = [
            Indexes_IFAE['Freqs'][ThisAnimal*(Indexes_IFAE['Exps'] == Exp)]
            for Exp in ExpOrder[:2]
        ]

        FreqsI = np.array([
            abs(Indexes_IFAE['Index'][
                ThisAnimal*(Indexes_IFAE['Exps'] == ExpOrder[0])
                *(Indexes_IFAE['Freqs'] == Freq)
            ])
            for Freq in Freqs[0]
        ]).ravel()

        Freqs[0] = np.array(Freqs[0])[FreqsI > 30].tolist()
        Freqs = sorted(
            np.intersect1d(Freqs[0], Freqs[1]),
            key=lambda x: int(x.split('-')[-1])
        )

        ExpFIDiff = [
            abs(Indexes_IFAE['Index'][
                ThisAnimal*(Indexes_IFAE['Exps'] == ExpOrder[1])
                *(Indexes_IFAE['Freqs'] == Freq)
            ])
            - abs(Indexes_IFAE['Index'][
                ThisAnimal*(Indexes_IFAE['Exps'] == ExpOrder[0])
                *(Indexes_IFAE['Freqs'] == Freq)
            ])
            for Freq in Freqs
        ]


        if not ExpFIDiff: MAF.append(None)
        else: MAF.append(Freqs[ExpFIDiff.index(min(ExpFIDiff))])

    return(MAF)


def GetMAFIndexes(Indexes_IFAE, MAF, Animals, ExpOrder):
    Indexes = [
        np.array(
            [Indexes_IFAE['Index'][
                (Indexes_IFAE['Exps'] == Exp) *
                (Indexes_IFAE['Animals'] == Animal) *
                (Indexes_IFAE['Freqs'] == MAF[A])
             ] for A, Animal in enumerate(Animals) if MAF[A]
            ]
        ).ravel() for E, Exp in enumerate(ExpOrder)
    ]

    return(Indexes)


def IndexCalc(Data, X, SliceSamples, Keys, BGNormalize=True):
    Index = {}
    for Key in Keys:
        PulseStart = np.where((X >= 0))[0][0]
        PulseEnd = PulseStart + SliceSamples

        if type(Data[Key[0]]) == list:
            if not Data[Key[0]]:
                print('Key', Key[0], 'is empty. Skipping...')
                continue

        ResRMSPulse = (np.mean(Data[Key[0]][PulseStart:PulseEnd]**2))**0.5
        RefRMSPulse = (np.mean(Data[Key[1]][PulseStart:PulseEnd]**2))**0.5

        if BGNormalize:
            BGStart = PulseStart-SliceSamples
            BGEnd = PulseStart
            ResRMSBG = (np.mean(Data[Key[0]][BGStart:BGEnd]**2))**0.5
            RefRMSBG = (np.mean(Data[Key[1]][BGStart:BGEnd]**2))**0.5

            ResRMS = abs(ResRMSPulse-ResRMSBG)
            RefRMS = abs(RefRMSPulse-RefRMSBG)

        else:
            RefRMS = RefRMSPulse
            ResRMS = ResRMSPulse

        Index[Key[2]] = ((ResRMS/RefRMS)-1)*100

    return(Index)


def PreallocateDict(Freqs):
    Dict = {
        Key: {'-'.join([str(Freq[0]), str(Freq[1])]): {} for Freq in Freqs}
        for Key in ['Trace', 'Index', 'IndexTrace']
    }

    for Freq in Dict['Trace'].keys():
        Dict['Trace'][Freq]['NoGap'] = []; Dict['Trace'][Freq]['Gap'] = []
        Dict['IndexTrace'][Freq]['NoGap'] = []; Dict['IndexTrace'][Freq]['Gap'] = []

    return(Dict)


def OrganizeRecs(
        Dict, Data, Rate, DataInfo, TimeWindow, FilterFreq=[70, 400],
        FilterOrder=4, FilterType='', Filter='butter', Verbose=False
    ):

    Recs = sorted(Data.keys(), key=lambda i: int(i))

    print('Slicing and filtering Recs...')
    for R, Rec in Data.items():
        Freq = DataInfo['ExpInfo']['FreqOrder'][Recs.index(R)][0];
        Trial = DataInfo['ExpInfo']['FreqOrder'][Recs.index(R)][1];

        SFreq = ''.join([str(DataInfo['Audio']['NoiseFrequency'][Freq][0]), '-',
                         str(DataInfo['Audio']['NoiseFrequency'][Freq][1])])

        if Trial == -1: STrial = 'Pre'
        elif Trial == -2: STrial = 'Post'
        elif Trial % 2 == 0: STrial = 'NoGap'
        else: STrial = 'Gap'

        if STrial in ['Pre', 'Post']:
            print('Pre- and Post- trials still to be implemented. Skipping...')
            continue

        TTLs = sAnalysis.QuantifyTTLs(
            Rec[:,DataInfo['DAqs']['TTLCh']-1], Verbose=Verbose
        )
        if len(TTLs) > 1:
            if Verbose: print('More than one TTL detected!!')
            # TTLs = [Rec[:,DataInfo['DAqs']['TTLCh']-1].argmax()]    # Get larger TTL
            TTLs = [TTLs[0]]                                          # Get first TTL
        # print(TTLs)

        if not TTLs: print('No TTL detected. Skipping trial...'); continue


        if not FilterType:
            if len(FilterFreq) == 1: FilterType = 'lowpass'
            else: FilterType = 'bandpass'

        if len(DataInfo['DAqs']['RecCh']) == 1:
            if Filter:
                GD = sAnalysis.FilterSignal(
                    Rec[:,DataInfo['DAqs']['RecCh'][0]-1],
                    Rate, FilterFreq, FilterOrder, Filter, FilterType
                )
            else:
                GD = Rec[:,DataInfo['DAqs']['RecCh'][0]-1]

        elif len(DataInfo['DAqs']['RecCh']) == 3:
            if Filter:
                GD = sAnalysis.FilterSignal(
                    Rec[:,np.array(DataInfo['DAqs']['RecCh'])-1],
                    Rate, FilterFreq, FilterOrder, Filter, FilterType
                )
            else:
                GD = Rec[:,np.array(DataInfo['DAqs']['RecCh'])-1]

            GD = sAnalysis.Normalize(GD, MeanSubtract=True, MaxDivide=False)
            GD = abs(GD).mean(axis=1)

            # X = sAnalysis.FilterSignal(Rec[:,DataInfo['DAqs']['RecCh'][0]-1],
                                          # Rate, FilterFreq, FilterOrder, Filter, FilterType)
            # Y = sAnalysis.FilterSignal(Rec[:,DataInfo['DAqs']['RecCh'][1]-1],
                                          # Rate, FilterFreq, FilterOrder, Filter, FilterType)
            # Z = sAnalysis.FilterSignal(Rec[:,DataInfo['DAqs']['RecCh'][2]-1],
                                          # Rate, FilterFreq, FilterOrder, Filter, FilterType)

            # GD = np.mean([
                # np.abs(X-X.mean()),
                # np.abs(Y-Y.mean()),
                # np.abs(Z-Z.mean())],
                # axis=0
            # )

        GD -= GD.mean()
        GD = sAnalysis.Slice(GD, TTLs, [int(TimeWindow[0]*Rate), int(TimeWindow[1]*Rate)])

        Dict['IndexTrace'][SFreq][STrial].append(GD)
        Dict['Trace'][SFreq][STrial].append(GD)

    return(Dict)


## Level 1
def GetAllTrials(
        Data, Rate, DataInfo, TimeWindow=[-0.1, 0.15], FilterFreq=[70, 400],
        FilterOrder=3, FilterType='', Filter='butter', **Args
    ):

    if not DataInfo:
        # Override for old .mat recordings
        if not FilterType:
            if len(FilterFreq) == 1: FilterType = 'lowpass'
            else: FilterType = 'bandpass'

        GPIASData = Data.copy()
        for Key in ['IndexTrace', 'Trace']:
            for F,Freq in GPIASData[Key].items():
                for G,Gap in Freq.items():
                    for T,Trial in enumerate(Gap):
                        if Filter:
                            GD = sAnalysis.FilterSignal(Trial, Rate, FilterFreq, FilterOrder, Filter, FilterType)
                        else:
                            GD = Trial.copy()

                        GD -= GD.mean()
                        GD = sAnalysis.Slice(
                            GD, GPIASData['TTLs'],
                            [int(TimeWindow[0]*Rate), int(TimeWindow[1]*Rate)]
                        )

                        print(Key, F, G, T)
                        GPIASData[Key][F][G][T] = GD.copy()

        del(GD)

    else:
        GPIASData = PreallocateDict(DataInfo['Audio']['NoiseFrequency'])
        GPIASData = OrganizeRecs(GPIASData, Data, Rate, DataInfo,
                                       TimeWindow,
                                       FilterFreq, FilterOrder, FilterType, Filter)

    return(GPIASData)


## Level 2
def Analysis(
        Data, Rate, DataInfo,
        TimeWindow=[-0.15, 0.15], SliceSize=0.1,
        FilterFreq=[70, 400], FilterOrder=3, FilterType='', Filter='butter',
        BGNormalize=True, Save='', Return=True):

    X = sAnalysis.GetTime(TimeWindow, Rate)*1000

    GPIASData = GetAllTrials(
        Data, Rate, DataInfo, TimeWindow, FilterFreq,
        FilterOrder, FilterType, Filter,
    )

    for Freq in GPIASData['IndexTrace'].keys():
        for Key in GPIASData['IndexTrace'][Freq].keys():
            # Average trials for traces
            GPIASData['Trace'][Freq][Key] = np.mean(GPIASData['Trace'][Freq][Key], axis=0)
            if GPIASData['Trace'][Freq][Key].shape == ():
                print('Freq', Freq, 'trial', Key, 'is empty. Skipping...')
                continue

            for Tr in range(len(GPIASData['IndexTrace'][Freq][Key])):
                GPIASData['IndexTrace'][Freq][Key][Tr] = abs(
                        signal.hilbert(GPIASData['IndexTrace'][Freq][Key][Tr])
                )

            GPIASData['IndexTrace'][Freq][Key] = np.nanmean(GPIASData['IndexTrace'][Freq][Key], axis=0)

        # RMS
        Keys = [['Gap', 'NoGap', 'GPIASIndex']]

        GPIASData['Index'][Freq] = IndexCalc(
            GPIASData['IndexTrace'][Freq], X, int(SliceSize*Rate),
            Keys, BGNormalize
        )


    if len(Save):
        IO.Bin.Write({'GPIAS': GPIASData, 'X': X}, Save)

    if Return: return(GPIASData, X)
    else: return(None)

