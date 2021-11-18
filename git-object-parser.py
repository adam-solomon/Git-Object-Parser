import os
import zlib
import argparse
import glob
import shutil
import subprocess

def setArgs():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument("-r", "--repo", type=str, dest="repo", help="Path of repo, one level above .git directory.")
    parser.add_argument("-o", "--outputDir", type=str, dest="outputDir", help="Directory to save files. Default outputs to terminal.")
    parser.parse_args()
    args = parser.parse_args()
    return args

def setRepoDir():
    if args.repo:
        dir = args.repo
    else:
        print("Enter path to repo, one level above .git directory:")
        dir = input("> ")
    return dir

def validateDir(dir):
    isValid = os.path.isdir(dir) 
    return isValid

def checkPack(path):
    packStatus = glob.glob(path + '/.git/objects/pack/*.pack')
    return packStatus

def unpack(path):
    for data in glob.glob(path + '/.git/objects/pack/*.pack'):
        print("[+] Moving pack file to base directory.")
        shutil.move(data,path)
    for data in glob.glob(path + '/*.pack'):
        print("[+] Unpacking pack file.")
        packCmd = ("cat", data)
        p1 = subprocess.Popen(packCmd, cwd=path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p1_out = p1.communicate()[0]
        gitCmd = ("git", "unpack-objects")
        p2 = subprocess.Popen(gitCmd, cwd=path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p2.communicate(input=p1_out)[0]
    return True

def parse(path):
    skipFiles = [".ds_store"]
    objectDir = (path + "/.git/objects/")
    if args.outputDir and not validateDir(args.outputDir):
        print("[-] Output directory is invalid.")
        exit()
    files = os.listdir(objectDir)
    for root, directories, files in os.walk(objectDir):
        if "pack" in directories:
            directories.remove("pack")
        if "info" in directories:
            directories.remove("info")
        for name in files:
            if name.lower() not in skipFiles:
                last_chars = root[-2:]
                filename = (os.path.join(root, name))
                compressed_contents = open(filename, 'rb').read()
                decompressed_contents = zlib.decompress(compressed_contents)
                if args.outputDir:
                    objectName = (last_chars + name)
                    outputFile = (args.outputDir + "/" + objectName)
                    file = open(outputFile, "wb")
                    file.write(decompressed_contents)
                    file.flush()
                    file.close()
                else:
                    print("Object Name: ", last_chars, name, sep='')
                    print("\r\n-------- Start of File --------\r\n\r\n")
                    print(decompressed_contents)
                    print("\r\n\r\n-------- End of File ---------\r\n\r\n")
    return

if __name__ == "__main__":
    args = setArgs()
    baseObjectDir = setRepoDir()
    if validateDir(baseObjectDir):
        if checkPack(baseObjectDir):
            unpack(baseObjectDir)
        parse(baseObjectDir)
        print("[+] Object parsing complete.")
        if args.outputDir and validateDir(args.outputDir):
            print("[+] Output files written to:", args.outputDir)
    else:
        print("[-] Repo directory is invalid.")