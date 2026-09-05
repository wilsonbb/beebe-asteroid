import argparse
from .seed import seed

def main():
    p=argparse.ArgumentParser(description='Beebe public-image pipeline')
    sub=p.add_subparsers(dest='command',required=True)
    s=sub.add_parser('seed');s.add_argument('--source')
    args=p.parse_args()
    if args.command=='seed':seed(args.source)
if __name__=='__main__':main()
