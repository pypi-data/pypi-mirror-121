#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170612
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import numpy as np
from itertools import combinations
from scipy import stats as sstats

try:
    from rpy2 import robjects as RObj
    from rpy2.robjects import packages as RPkg
except ModuleNotFoundError as e:
    print(f'[Analysis.Stats] {e}: Module `rpy2` not available. Some functions will not work.')


## Level 0
def PearsonRP(A,B):
    r = sstats.pearsonr(A, B)
    r = list(r)
    r[0] = round(r[0], 3)
    if r[1] < 0.05:
        r[1] = '%.1e' % r[1] + ' *'
    else:
        r[1] = str(round(r[1], 3))

    return(r)


def PToStars(p, Max=3):
    No = 0
    while p < 0.05 and No <= Max:
        p *=10
        No +=1

    return(No)


def RAdjustNaNs(Array):
    try: NaN = RObj.NA_Real
    except NameError as e:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    for I, A in enumerate(Array):
        if A != A: Array[I] = NaN

    return(Array)


def RCheckPackage(Packages):
    try:
        RPacksToInstall = [Pack for Pack in Packages if not RPkg.isinstalled(Pack)]
    except NameError as e:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    if len(RPacksToInstall) > 0:
        print(str(RPacksToInstall), 'not installed. Install now?')
        Ans = input('[y/N]: ')

        if Ans.lower() in ['y', 'yes']:
            from rpy2.robjects.vectors import StrVector as RStrVector

            RUtils = RPkg.importr('utils')
            RUtils.chooseCRANmirror(ind=1)

            RUtils.install_packages(RStrVector(RPacksToInstall))

        else: print('Aborted.')

    return(None)


def RModelToDict(Model):
    Dict = {
        C: np.array(Col.levels)
        if 'Factor' in C and np.array(Col).dtype == np.int32
        else np.array(Col)
        for C,Col in Model.items()
    }

    return(Dict)


## Level 1
def RPCA(Matrix):
    try:
        RCheckPackage(['stats']); Rstats = RPkg.importr('stats')
    except NameError as e:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    RMatrix = RObj.Matrix(Matrix)
    PCA = Rstats.princomp(RMatrix)
    return(PCA)


def RAnOVa(Data, Factors, Paired, Id=[]):
    try:
        RCheckPackage(['rstatix']); RPkg.importr('rstatix')
    except NameError as e:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    Values = RObj.FloatVector(Data)
    FactorsV = [RObj.FactorVector(_) for _ in Factors]
    Frame = {f'Factor{f+1}': F for f,F in enumerate(FactorsV)}
    Frame['Values'] = Values

    if len(Id):
        Idv = RObj.IntVector(Id)
        RObj.globalenv['Id'] = Idv
        Frame['Id'] = Idv

    Frame = RObj.DataFrame(Frame)

    RObj.globalenv['Frame'] = Frame
    RObj.globalenv['Values'] = Values
    for F,Factor in enumerate(FactorsV): RObj.globalenv[f'Factor{F+1}'] = Factor

    FactorsW = ','.join([f'Factor{_+1}' for _ in range(len(Factors)) if Paired[_]])
    FactorsB = ','.join([f'Factor{_+1}' for _ in range(len(Factors)) if not Paired[_]])
    Model = RObj.r(f'''anova_test(Frame, dv=Values, wid=Id, between=c({FactorsB}), within=c({FactorsW}))''')

    return(Model)


def RAnOVaPwr(GroupNo=RObj.NULL, SampleSize=RObj.NULL, Power=RObj.NULL,
           SigLevel=RObj.NULL, EffectSize=RObj.NULL):
    try:
        RCheckPackage(['pwr']); Rpwr = RPkg.importr('pwr')
    except NameError as e:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    Results = Rpwr.pwr_anova_test(k=GroupNo, power=Power, sig_level=SigLevel,
                                  f=EffectSize, n=SampleSize)

    print('Running', Results.rx('method')[0][0] + '... ', end='')
    AnOVaResults = {}
    for Key, Value in {'k': 'GroupNo', 'n': 'SampleSize', 'f': 'EffectSize',
                       'power':'Power', 'sig.level': 'SigLevel'}.items():
        AnOVaResults[Value] = Results.rx(Key)[0][0]

    print('Done.')
    return(AnOVaResults)


def RKruskalWallis(Data, Factor):
    try:
        RCheckPackage(['rstatix']); RPkg.importr('rstatix')
    except NameError as e:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    Values = RObj.FloatVector(Data)
    FactorV = RObj.FactorVector(Factor)
    Frame = RObj.DataFrame({f'Factor': FactorV, 'Values': Values})

    RObj.globalenv['Frame'] = Frame
    RObj.globalenv['Values'] = Values
    RObj.globalenv['Factor'] = FactorV

    Model = RObj.r(f'''kruskal_test(Frame, Values~Factor)''')

    return(Model)


def RTTest(DataA, DataB, Paired=True, EqualVar=False, Alt='two.sided', Confidence=0.95):
    try:
        RCheckPackage(['rstatix']); RPkg.importr('rstatix')
    except NameError as e:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    Rttest = RObj.r['t.test']
    RCohensD = RObj.r['cohens_d']

    DataA = RAdjustNaNs(DataA); DataB = RAdjustNaNs(DataB)

    Results = Rttest(RObj.FloatVector(DataA), RObj.FloatVector(DataB),
                     paired=Paired, var_equal=EqualVar, alternative=Alt,
                     conf_level=RObj.FloatVector([Confidence]),
                     na_action=RObj.r['na.omit'])

    TTestResults = {}; Names = list(Results.names)
    for Name in Names:
        TTestResults[Name] = Results.rx(Name)[0][0]

    Values = RObj.FloatVector(np.concatenate((DataA, DataB)))
    Factor = RObj.FactorVector(['A']*len(DataA)+['B']*len(DataB))

    Frame = RObj.DataFrame({
        'Values': Values,
        'Factor': Factor,
    })

    RObj.globalenv["Confidence"] = Confidence
    RObj.globalenv["EqualVar"] = EqualVar
    RObj.globalenv["Factor"] = Factor
    RObj.globalenv["Frame"] = Frame
    RObj.globalenv["Paired"] = Paired
    RObj.globalenv["Values"] = Values
    Model = RObj.r('''cohens_d(Frame, Values ~ Factor, conf.level=Confidence, var.equal=EqualVar, paired=Paired)''')
    TTestResults['CohensD'] = RModelToDict(Model)

    return(TTestResults)


def RWilcoxon(DataA, DataB, Paired=False, Pairwise=True, PAdj='bonferroni'):
    try:
        RCheckPackage(['rstatix']); RPkg.importr('rstatix')
    except NameError as e:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    Values = RObj.FloatVector(np.concatenate((DataA, DataB)))
    FactorV = RObj.FactorVector(
        np.concatenate((
            np.tile(['0'],len(DataA)), np.tile(['1'],len(DataB))
        ))
    )
    Frame = RObj.DataFrame({f'Factor': FactorV, 'Values': Values})

    RObj.globalenv['Frame'] = Frame
    RObj.globalenv['Values'] = Values
    RObj.globalenv['Factor'] = FactorV

    PW = 'pairwise_' if Pairwise else ''
    PairedV = 'TRUE' if Paired else 'FALSE'
    Model = RObj.r(f'''{PW}wilcox_test(Frame, Values~Factor, paired={PairedV}, p.adjust.method='{PAdj}')''')

    return(Model)


def Shapiro(Data, Factors):
    try:
        RCheckPackage(['rstatix']); RPkg.importr('rstatix')
    except NameError as e:
        raise e(f'[Analysis.Stats] {e}: Module `rpy2` not available.')

    Values = RObj.FloatVector(Data)
    FactorsV = [RObj.FactorVector(_) for _ in Factors]
    Frame = {f'Factor{f+1}': F for f,F in enumerate(FactorsV)}
    Frame['Values'] = Values
    Frame = RObj.DataFrame(Frame)

    RObj.globalenv['Frame'] = Frame
    RObj.globalenv['Values'] = Values
    for F,Factor in enumerate(FactorsV): RObj.globalenv[f'Factor{F+1}'] = Factor

    # Result = {
        # Fac: RObj.r(f'''Frame %>% group_by({Fac}) %>% shapiro_test(Values)''')
        # for Fac in [f'Factor{_+1}' for _ in range(len(Factors))]
    # }
#
    # Result = {K: RModelToDict(V) for K,V in Result.items()}

    SModel = RObj.r(f'''Frame %>% group_by({', '.join(['Factor'+str(_+1) for _ in range(len(Factors))])}) %>% shapiro_test(Values)''')

    Result = RModelToDict(SModel)

    return(Result)


## Level 2
# def ShapiroPerLevel(Data, Factors):
    # SPL = Shapiro(Data, Factors)
    # SPL = {
        # [v for k,v in fac.items() if 'Factor' in k][0][L]: p
        # for fac in SPL.values()
        # for L,p in enumerate(fac['p'])
    # }
#
    # return(SPL)


def KruskalWallis(Data, Factor):
    Model = RKruskalWallis(Data, Factor)
    Results = RModelToDict(Model)
    Results['Effect'] = RModelToDict(RObj.r(
        f'''kruskal_effsize(Frame, Values~Factor)'''
    ))

    return(Results)


def Wilcoxon(DataA, DataB, Paired=False, Pairwise=True, PAdj='bonferroni'):
    Model = RWilcoxon(DataA, DataB, Paired, Pairwise, PAdj)
    Results = RModelToDict(Model)
    PairedV = 'TRUE' if Paired else 'FALSE'
    Results['Effect'] = RModelToDict(RObj.r(
        f'''wilcox_effsize(Frame, Values~Factor, paired={PairedV})'''
    ))

    return(Results)


## Level 3
def AnOVa(Data, Factors, Id=[], Paired=[], Parametric='auto'):
    if not len(Paired): Paired = [False for _ in Factors]
    PairedV = ['TRUE' if _ else 'FALSE' for _ in Paired]

    # # Automatic checking of paired data
    # Combs = list(combinations(range(len(Factors)),len(Factors)-1))
    # for F,Factor in enumerate(Factors):
        # Others = [F not in _ for _ in Combs].index(True)
        # Others = Combs[Others]

        # OthersCond = []
        # for O in Others:
            # if not len(OthersCond): OthersCond =
        # Paired = [
            # O==ao for ao in np.unique(Others)]
            # for O in Others
        # ]

    # # This works
    # True in [a[((c==af1)*(d==af2)*(e==ai)).astype(bool)].shape[0]>1 for af1 in c for af2 in d for ai in e]
    # # for data a; factors b,c and d; and id e
    # # but how to dynamically iterate through different number of factors?

    Model = RAnOVa(Data, Factors, Paired, Id)

    if Model.rclass[1] == 'list':
        Results = {
            'ANOVA': RModelToDict(Model[0]),
            'MauchlySphericity': RModelToDict(Model[1]),
            'SphericityCorrection': RModelToDict(Model[2]),
        }
    else:
        Results = {
            'ANOVA': RModelToDict(Model),
        }

    IsNormal = Shapiro(Data, Factors) if Parametric == 'auto' else None

    if len(Factors) == 1:
        PWC, PWCEff = {}, {}

        if type(IsNormal) == dict:
            Results['ShapiroNormality'] = {**IsNormal}
            Parametric = True not in (IsNormal['p']<0.05)

        if Parametric:
            PWC['Factor1'] = [RObj.r(
                f'''Frame %>% pairwise_t_test(Values~Factor1, paired={PairedV[0]}) %>% adjust_pvalue(method="bonferroni")'''
            )]
            PWCEff['Factor1'] = [RObj.r(
                f'''Frame %>% cohens_d(Values~Factor1, paired={PairedV[0]})'''
            )]
        else:
            PWC['Factor1'] = [RObj.r(
                f'''Frame %>% pairwise_wilcox_test(Values~Factor1, paired={PairedV[0]}) %>% adjust_pvalue(method="bonferroni")'''
            )]
            PWCEff['Factor1'] = [RObj.r(
                f'''Frame %>% wilcox_effsize(Values~Factor1, paired={PairedV[0]})'''
            )]

        Results = {**Results, **{
            'PWCs': {F: [RModelToDict(_) for _ in Fac] for F,Fac in PWC.items()}
        }}

        for F,Fac in PWCEff.items():
            for f,fac in enumerate(Fac):
                Results['PWCs'][F][f]['Effect'] = RModelToDict(fac)

    else:
        FactorsW = [_ for _ in range(len(Factors)) if Paired[_]]
        FPairs = tuple(combinations(range(len(Factors)), 2))

        # Variables `Frame`, `Values`, `FactorX` and `Id` defined inside `RAnOVa()`.
        FXs = {f'Factor{FPair+1}': [] for FPair in range(len(Factors))}
        for FPair in FPairs:
            try:
                fw = [_ in FactorsW for _ in FPair]

                fs = f'within=Factor{FPair[0]+1}' if fw[0] else f'between=Factor{FPair[0]+1}'
                FXs[f'Factor{FPair[0]+1}'].append(RObj.r(
                    f'''Frame %>% group_by(Factor{FPair[1]+1}) %>% anova_test(dv=Values, wid=Id, {fs}) %>% get_anova_table() %>% adjust_pvalue(method="bonferroni")'''
                ))

                fs = f'within=Factor{FPair[1]+1}' if fw[1] else f'between=Factor{FPair[1]+1}'
                FXs[f'Factor{FPair[1]+1}'].append(RObj.r(
                    f'''Frame %>% group_by(Factor{FPair[0]+1}) %>% anova_test(dv=Values, wid=Id, {fs}) %>% get_anova_table() %>% adjust_pvalue(method="bonferroni")'''
                ))
            except Exception as e:
                print(f"{e}: Factors {FPair[0]+1} and {FPair[1]+1} are not enough to uniquely separate the data.")

        PWC = {f'Factor{FPair+1}': [] for FPair in range(len(Factors))}
        PWCEff = {f'Factor{FPair+1}': [] for FPair in range(len(Factors))}

        for FPair in FPairs:
            if type(IsNormal) == dict:
                Results['ShapiroNormality'] = {**IsNormal}
                Parametric = True not in (IsNormal['p']<0.05)

            if Parametric:
                PWC[f'Factor{FPair[0]+1}'].append(RObj.r(
                    f'''Frame %>% group_by(Factor{FPair[1]+1}) %>% pairwise_t_test(Values~Factor{FPair[0]+1}, paired={PairedV[FPair[0]]}) %>% adjust_pvalue(method="bonferroni")'''
                ))
                PWC[f'Factor{FPair[1]+1}'].append(RObj.r(
                    f'''Frame %>% group_by(Factor{FPair[0]+1}) %>% pairwise_t_test(Values~Factor{FPair[1]+1}, paired={PairedV[FPair[1]]}) %>% adjust_pvalue(method="bonferroni")'''
                ))
                PWCEff[f'Factor{FPair[0]+1}'].append(RObj.r(
                    f'''Frame %>% group_by(Factor{FPair[1]+1}) %>% cohens_d(Values~Factor{FPair[0]+1}, paired={PairedV[FPair[0]]})'''
                ))
                PWCEff[f'Factor{FPair[1]+1}'].append(RObj.r(
                    f'''Frame %>% group_by(Factor{FPair[0]+1}) %>% cohens_d(Values~Factor{FPair[1]+1}, paired={PairedV[FPair[1]]})'''
                ))
            else:
                PWC[f'Factor{FPair[0]+1}'].append(RObj.r(
                    f'''Frame %>% group_by(Factor{FPair[1]+1}) %>% pairwise_wilcox_test(Values~Factor{FPair[0]+1}, paired={PairedV[FPair[0]]}) %>% adjust_pvalue(method="bonferroni")'''
                ))
                PWC[f'Factor{FPair[1]+1}'].append(RObj.r(
                    f'''Frame %>% group_by(Factor{FPair[0]+1}) %>% pairwise_wilcox_test(Values~Factor{FPair[1]+1}, paired={PairedV[FPair[1]]}) %>% adjust_pvalue(method="bonferroni")'''
                ))
                PWCEff[f'Factor{FPair[0]+1}'].append(RObj.r(
                    f'''Frame %>% group_by(Factor{FPair[1]+1}) %>% wilcox_effsize(Values~Factor{FPair[0]+1}, paired={PairedV[FPair[0]]})'''
                ))
                PWCEff[f'Factor{FPair[1]+1}'].append(RObj.r(
                    f'''Frame %>% group_by(Factor{FPair[0]+1}) %>% wilcox_effsize(Values~Factor{FPair[1]+1}, paired={PairedV[FPair[1]]})'''
                ))

        Results = {**Results, **{
            'FXFactors': {F: [RModelToDict(_) for _ in Fac] for F,Fac in FXs.items()},
            'PWCs': {F: [RModelToDict(_) for _ in Fac] for F,Fac in PWC.items()}
        }}

        for F,Fac in PWCEff.items():
            for f,fac in enumerate(Fac):
                Results['PWCs'][F][f]['Effect'] = RModelToDict(fac)

    return(Results)


