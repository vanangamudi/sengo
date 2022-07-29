from arichuvadi import get_letters_coding as _ta
import arichuvadi as ari
import pdb
import sys
import argparse

################## ithuva_aa athuva_aa vagai  ####################
# ?, *, + kurigal
def kelvi_kuriya_aa(yezhuthu):     return yezhuthu == '?'
def vinmeen_kuriya_aa(yezhuthu):   return yezhuthu == '*'
def koottal_kuriya_aa(yezhuthu):   return yezhuthu == '+'
def kuriya_aa(yezhuthu):
    return (kelvi_kuriya_aa(yezhuthu)
            or vinmeen_kuriya_aa(yezhuthu)
            or koottal_kuriya_aa(yezhuthu))

# yezhutha
def yezhutha_aa(yezhuthu):
    return ari.yezhutha_aa(yezhuthu[0])

# vaguppa_aa
def vaguppu_thalaiya_aa(yezhuthu): return yezhuthu == '['
def vaguppu_kaala_aa(yezhuthu):    return yezhuthu == ']'
def vaguppa_aa(paangu):
    return vaguppu_thalaiya_aa(paangu[0]) and vaguppu_kaala_aa(paangu[-1])

# pulli(.) kuri
def pulliya_aa(yezhuthu): return yezhuthu == '.'

# \எ - எண்கள், \செ - எழுத்துகள் போல
def sirappu_vaguppa_aa(yezhuthu):
    return yezhuthu == '\\'

def urupadiya_aa(paangu):
    return (
        vaguppa_aa(paangu)
        or yezhutha_aa(paangu[0])
        or pulliya_aa(paangu[0])
        or sirappu_vaguppa_aa(paangu[0])
    )

# maatra_aa
def maatru_thalaiya_aa(yezhuthu): return yezhuthu == '('
def maatru_kaala_aa(yezhuthu):    return yezhuthu == ')'
def maatraa_aa(paangu):
    return maatru_thalaiya_aa(paangu[0]) and maatru_kaala_aa(paangu[-1])

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
    muthal, kuri, meethi = None, None, None

    i = 0
    if maatru_thalaiya_aa(paangu[0]):
        i  = paangu.index(')') + 1
    elif vaguppu_thalaiya_aa(paangu[0]):
        i  = paangu.index(']') + 1
    elif sirappu_vaguppa_aa(paangu[0]): 
        i += 2
    else:
        i = 1

    muthal = paangu[:i]
    if i < len(paangu) and kuriya_aa(paangu[i]):
        kuri = paangu[i]
        i += 1
        
    meethi = paangu[i:]
        
    return muthal, kuri, meethi
        
################### poruthubavai ########################
def pala_poru(paangu, saram, neelam,
                 kurai_neelam, athi_neelam,
    ):
    
    muthal, kuri, meethi = paangu_piri(paangu)
    if not kurai_neelam:
        kurai_neelam = 0

    utporu_neelam = -1

    while not athi_neelam or utporu_neelam < athi_neelam:
        utporuvu, ut_neelam = paangu_poru(
            muthal * (utporu_neelam + 1), saram, neelam
        )
        if utporuvu:
            utporu_neelam += 1
        else:
            break

    while utporu_neelam >= kurai_neelam:
        poruvu, puthu_neelam = paangu_poru(
            muthal *  utporu_neelam + meethi, saram, neelam
        )
        if poruvu:
            return poruvu, puthu_neelam
        utporu_neelam -= 1

    return False, None


def yezhuthu_poruvutha_aa(paangu, saram):
    return paangu[0] == saram[0]

def urupadi_poruvutha_aa(paangu, saram):
    muthal, kuri, meethi  = paangu_piri(paangu)
    
    if vaguppa_aa(muthal):
        urupadigal = vaguppu_piri(muthal)
        return saram[0] in urupadigal

    elif yezhutha_aa(muthal):
        return yezhuthu_poruvutha_aa(paangu, saram)

    elif pulliya_aa(muthal[0]):
        return True
    
    elif sirappu_vaguppa_aa(muthal[0]):
        if ''.join(muthal) == '\எ':
            return ari.yenna_aa(saram[0])
        if ''.join(muthal) == '\சொ':
            return ari.yezhutha_aa(saram[0])
        

def maatru_poru(paangu, saram, neelam):
    muthal, kuri, meethi = paangu_piri(paangu)
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
    
    if paangu[0] == '$':
        if len(saram) > 0:
            return False, None
        else:
            return True, neelam
    
    muthal, kuri, meethi = paangu_piri(paangu)
    print(f' muthal kuri meethi: {"".join(muthal)}, {kuri}, {"".join(meethi)}')
    
    if kelvi_kuriya_aa(kuri):
        #paangu not muthal because pala_poruthu needs meethi for backtracking
        return pala_poru(paangu, saram, neelam, 0, 1) 
    elif koottal_kuriya_aa(kuri):
        return pala_poru(paangu, saram, neelam, 1, None)
    elif vinmeen_kuriya_aa(kuri):
        return pala_poru(paangu, saram, neelam, None, None)
    
    elif maatraa_aa(muthal):
        return maatru_poru(paangu, saram, neelam)
    elif urupadiya_aa(muthal):
        if urupadi_poruvutha_aa(muthal, saram):
            return paangu_poru(meethi, saram[1:], neelam + 1)
    
    return False, None

def poru(paangu, saram):
    i = 0
    poruva_aa = False

    if paangu[0] == '^':
        athi_neelam = 1
        paangu = paangu[1:]
    else:
        athi_neelam = len(saram)
        
    while not poruva_aa and i < athi_neelam:
        poruva_aa, neelam = paangu_poru(paangu, saram[i:])
        if poruva_aa:
            return poruva_aa, i, neelam

        i += 1

    return False, None, None

if __name__ == '__main__':

    parser = argparse.ArgumentParser('sengo')
    parser.add_argument('-p', '--paangu',
                        help='paangu e.g: ^தனி.*',
                        default=None)
    
    parser.add_argument('-s', '--saram',
                        help='saram to match e.g:தனிச்செம்மொழி தமிழ்',
                        default=None)
    
    args = parser.parse_args()

    paangugal, varigal = [], []
    
    if args.paangu: paangugal = [args.paangu]
    if args.saram: varigal = [args.saram]

    if not paangugal:
        paangugal = open('sothanai-paangugal.txt').read().split('\n')
        paangugal = [i for i in paangugal if i.strip()]
        
    if not varigal:
        varigal   = open('sothanai-varigal.txt').read().split('\n')
        varigal   = [i for i in varigal if i.strip()]

    
    for paangu in paangugal:
        print(f'======= {paangu}  =======')
        for saram in varigal:
            print(f'  ======= {saram}  =======')
            poruva_aa, thalai, neelam = poru(_ta(paangu),
                                             _ta(saram))

            print('>>> "{}" "{}" =?= {}, {}'.format(
                paangu,
                saram,
                poruva_aa,
                ''.join( _ta(saram) [thalai:thalai+neelam] ) if poruva_aa else ''
            ))
