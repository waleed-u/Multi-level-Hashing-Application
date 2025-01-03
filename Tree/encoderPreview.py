import argparse

from Models.Encoder import Encoder

def previewEncoder()->None:
    parser = argparse.ArgumentParser(
        prog="Multi Level Encoder for Hashing",
        description="This program read a file and creates a Merkle Tree ready for Multi-Level Hashing",
        epilog="Created by \033[1mAbubakar Javed :)\033[0m"
    )
    parser.add_argument("-f","--file",action='store',help="stores path of the file you want to hash", type=str)
    parser.add_argument("-s","--string",action='store',help="sstring you want to hash", type=str)
    args = parser.parse_args()
    
    if args.file == None and args.string == None:
        print("Usage: -f, --file\tadd path of file to be hashed")
        print("Usage: -s, --string\tstring to be hashed")
        return
    
    if args.file != None:
        encoder = Encoder(args.file, isFile=True) 
    else:
        encoder = Encoder(args.string, isFile=False)
    
    print(f"\n\033[1m\033[32mFinal Hash Value: {encoder.getFinalHash()}\033[0m")
    
    
previewEncoder()
    
    
    
    
    
    