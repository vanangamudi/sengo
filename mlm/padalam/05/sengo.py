from arichuvadi import get_letters_coding as _ta
import arichuvadi as ari
import pdb

################## ithuva_aa athuva_aa vagai  ####################
def yezhutha_aa(yezhuthu):
    return ari.yezhutha_aa(yezhuthu[0])

# vaguppa_aa
def vaguppu_thalaiya_aa(yezhuthu): return yezhuthu == '['
def vaguppu_kaala_aa(yezhuthu):    return yezhuthu == ']'
def vaguppa_aa(paangu):
    return vaguppu_thalaiya_aa(paangu[0]) and vaguppu_kaala_aa(paangu[-1])

# pulli(.) kuri
def pulliya_aa(yezhuthu): return yezhuthu == '.'

def urupadiya_aa(paangu):
    return (
        vaguppa_aa(paangu)
        or yezhutha_aa(paangu[0])
        or pulliya_aa(paangu[0])
    )

# maatra_aa
def maatru_thalaiya_aa(yezhuthu): return yezhuthu == '('
def maatru_kaala_aa(yezhuthu):    return yezhuthu == ')'
def maatraa_aa(paangu):
    return maatru_thalaiya_aa(paangu[0]) and maatru_kaala_aa(paangu[-1])

# kurigal


################ pirippavai ######################################

# [தமிழ்] -> த,மி,ழ்
def vaguppu_piri(paangu, vazhu=False):
    assert vaguppa_aa(paangu)
    urupadigal = list(paangu[1:-1])
    return urupadigal

# (த|அ)மிழ் ---> [தஅ]
def maatru_piri(paangu):
    assert maatraa_aa(paangu)
    paangu = ''.join(paangu[1:-1]) # 0 -> (; -1 ->)    #pack into string
    urupadigal = [ _ta(i) for i in paangu.split('|')]  #unpack into tamilstr
    return urupadigal

def paangu_piri(paangu):
    muthal, meethi = None, None

    if maatru_thalaiya_aa(paangu[0]):
        i  = paangu.index(')') + 1
    elif vaguppu_thalaiya_aa(paangu[0]):
        i  = paangu.index(']') + 1
    else:
        i = 1

    muthal = paangu[:i]
    meethi = paangu[i:]

    return muthal, meethi
        
################### poruthubavai ########################
def yezhuthu_poruvutha_aa(paangu, saram):
    return paangu[0] == saram[0]

def urupadi_poruvutha_aa(paangu, saram):
    muthal, meethi = paangu_piri(paangu)
    
    if vaguppa_aa(muthal):
        urupadigal = vaguppu_piri(muthal)
        print(urupadigal, saram)
        return saram[0] in urupadigal

    elif yezhutha_aa(muthal):
        return yezhuthu_poruvutha_aa(paangu, saram)

    elif pulliya_aa(muthal[0]):
        return True

def maatru_poru(paangu, saram, neelam):
    muthal, meethi = paangu_piri(paangu)
    maatrugal = maatru_piri(muthal)

    for maatru in maatrugal:
         poruvu, puthu_neelam = paangu_poru(
             maatru + meethi, saram, neelam,
         )

         if poruvu:
             return poruvu, puthu_neelam
         
    return False, None

def paangu_poru(paangu, saram, neelam=0):
    print(neelam, ':', ''.join(paangu), '=?=', ''.join(saram))

    if len(paangu) == 0:
        return True, neelam
    if len(paangu) and not len(saram):
        return False, None

    muthal, meethi = paangu_piri(paangu)
    print(f' muthal meethi: {muthal}, {meethi}')
    if maatraa_aa(muthal):
        return maatru_poru(paangu, saram, neelam)
    elif urupadiya_aa(muthal):
        if urupadi_poruvutha_aa(muthal, saram):
            return paangu_poru(meethi, saram[1:], neelam + 1)
    
    return False, None

def poru(paangu, saram):
    i = 0
    poruva_aa = False
    
    while not poruva_aa and i < len(saram):
        poruva_aa, neelam = paangu_poru(paangu, saram[i:])
        if poruva_aa:
            return poruva_aa, i, neelam

        i += 1

    return False, None, None

if __name__ == '__main__':

    paangugal = open('sothanai-paangugal.txt').read().split('\n')
    varigal   = open('sothanai-varigal.txt').read().split('\n')

    paangugal = [i for i in paangugal if i.strip()]
    varigal   = [i for i in varigal if i.strip()]
    
    for paangu in paangugal:
        print(f'======= {paangu}  =======')
        for saram in varigal:
            print(f'  ======= {saram}  =======')
            poruva_aa, thalai, neelam = poru(_ta(paangu),
                                             _ta(saram))

            print('>>> {}, {} =?= {}'.format(
                paangu,
                saram,
                poruva_aa,
                ''.join( _ta(saram) [thalai:thalai+neelam] ) if poruva_aa else ''
            ))
