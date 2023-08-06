from . import sign, verify, token
import argh

parser = argh.ArghParser()
parser.add_commands([sign, verify, token])

def cli(parser=parser):
    #argh.dispatch(parser)
    parser.dispatch()

if __name__ == '__main__':
    cli(parser)