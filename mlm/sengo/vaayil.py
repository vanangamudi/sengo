import argparse
from arichuvadi import get_letters_coding as _ta
from sengo import poru

def vaayil():
    parser = argparse.ArgumentParser('sengo')
    parser.add_argument('paangu',
                        help='paangu e.g: ^தனி.*',)

    parser.add_argument('koappu',
                        help='file containing text',
                        nargs="+")
                        
    
    args = parser.parse_args()

    #print(f'======= {args.paangu}  =======')

    for koappu in args.koappu:
        for i, saram in enumerate(open(koappu)):
            saram = saram.strip()
            #print(f'  ======= {saram}  =======')
            poruva_aa, thalai, neelam = poru(_ta(args.paangu),
                                             _ta(saram))

            if poruva_aa:
                print(f'{koappu}:{i} "{args.paangu}" "{saram}" =?= {poruva_aa} ,' \
                      + ''.join( _ta(saram) [thalai:thalai+neelam] ) if poruva_aa else ''
                    )
                
if __name__ == '__main__':
    vaayil()
