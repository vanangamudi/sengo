from arichuvadi import get_letters_coding as _ta

def urupadi_poruvutha_aa(paangu, saram):
    return paangu[0] == saram[0]

def paangu_poru(paangu, saram, poruvu_neelam=0):
    print(poruvu_neelam, ''.join(paangu), ''.join(saram))
    
    if len(paangu) == 0:
        return True, poruvu_neelam

    if urupadi_poruvutha_aa(paangu, saram):
        return paangu_poru(paangu[1:], saram[1:], poruvu_neelam + 1)
    else:
        return False, None

def poru(paangu, saram):
    poruva_aa = False
    
    poruva_aa, neelam = paangu_poru(paangu, saram)
    if poruva_aa:
            return poruva_aa, neelam

    return False, 0

if __name__ == '__main__':

    paangu = 'தமிழ்'
    saram = 'தமிழ்'
    poruva_aa, neelam = poru(_ta(paangu),
                                       _ta(saram))

    print('{}, {} == {}'.format(
        paangu,
        saram,
        poruva_aa,
    ))
