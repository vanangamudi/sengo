from arichuvadi import get_letters_coding as _ta
import arichuvadi as ari

################## ithuva_aa athuva_aa vagai  ####################
def yezhutha_aa(paangu):
    return ari.yezhutha_aa(paangu[0])

def maatraa_aa(paangu):
    return paangu[0] == '(' and paangu[-1] == ')'

################ pirippavai ######################################

# (த|அ)மிழ் ---> [தஅ]
def maatru_piri(paangu):
    assert maatraa_aa(paangu)
    paangu = ''.join(paangu[1:-1]) # 0 -> (; -1 ->)    #pack into string
    urupadigal = [ _ta(i) for i in paangu.split('|')]  #unpack into tamilstr
    return urupadigal

def paangu_piri(paangu):
    muthal, meethi = None, None

    if paangu[0] == '(':
        i  = paangu.index(')') + 1
    else:
        i = 1

    muthal = paangu[:i]
    meethi = paangu[i:]

    return muthal, meethi
        

def yezhuthu_poruvutha_aa(paangu, saram):
    return paangu[0] == saram[0]

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

    muthal, meethi = paangu_piri(paangu)
    
    if maatraa_aa(muthal):
        return maatru_poru(paangu, saram, neelam)
    elif yezhutha_aa(muthal):
        if yezhuthu_poruvutha_aa(paangu, saram):
            return paangu_poru(paangu[1:], saram[1:], neelam + 1)
    
    return False, None

def poru(paangu, saram):
    i = 0
    poruva_aa = False
    
    while not poruva_aa:
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

            print('{}, {} == {}'.format(
                paangu,
                saram,
                poruva_aa,
                ''.join( _ta(saram) [thalai:thalai+neelam] )
            ))
