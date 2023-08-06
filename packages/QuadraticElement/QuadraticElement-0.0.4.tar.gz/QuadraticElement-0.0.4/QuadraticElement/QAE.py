import sys
import getopt
import os

def run():
    print("QuadraticElement")
    print("\nPYmili ! PYDOME ! yes !")
    print("\n====================================")
    print("欢迎使用QuadraticElement>")
    from QuadraticElement import QE

def main():
    """
    python QAE.py -r
    """
    options, args = getopt.getopt(sys.argv[1:], 'r')
    
    for name, value in options:
        if name in ('-r'):
            run()
 
if __name__ == "__main__":
    main()
