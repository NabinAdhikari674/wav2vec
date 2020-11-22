import subprocess
import os
import shutil

def git_clone_repo():
    print("\t## Cloning Required Repositories ...")
    git_fairseq = 'https://github.com/pytorch/fairseq.git'
    git_cython = 'https://github.com/cython/cython.git'

    for git_link in [git_fairseq,git_cython]:
        print(" > Cloning from : ",git_link)
        cmd = 'git clone {}'.format(git_link)
        subprocess.run(cmd,shell=True)

def install_editable():
    print("\n\t## Installing Fairseq and Cython as Editable ... ")
    base = os.getcwd()
    cmd = 'pip install --editable .'
    shutil.copytree(os.path.join(base,'cython'),os.path.join(base,'fairseq','cython'))
    os.chdir(os.path.join(base,'fairseq','cython'))
    subprocess.run(cmd,shell=True)
    os.chdir(os.path.join(base,'fairseq'))
    subprocess.run(cmd,shell=True)
    os.chdir(base)

def install_requirements():
    print("\n\t## Installing dependencies from \'requirements.txt\'  ... ")
    cmd = 'pip install -r requirements.txt'
    subprocess.run(cmd,shell=True)

if __name__ == '__main__':
    print("\n\t\t## Setup For wav2vec v0.1 by NabinAdhikari674 \n")
    git_clone_repo()
    install_editable()
    install_requirements()
