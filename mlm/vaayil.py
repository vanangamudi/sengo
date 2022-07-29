import argparse
from arichuvadi import get_letters_coding as _ta
from sengo import poru
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
