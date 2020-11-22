## Install Instructions :
> run setup.py as : sudo python setup.py
 
## Instructions to Train a Model :

> Put all your audio dataset in a folder named 'audio' on the same directory as main.py
> run main.py
  >> main.py first checks if your audio files are in recommended sample rate and convert them if not.
  >> then it will check if your audio files are in recommended length to train a model (10-30sec) and split a audio file if not.
  >> then it will initiate to create a manifest required to train the model.
  >> at last, training shall begin and last best checkpoint of the model will be saved to 'model' foder.

### Windows Limitations :

The program may not run in windows due to a recent change in how pip installs its packages.
After the numpy version 1.19.4, due to a incompatibility, package fairseq which requires numpy during installation,
fails to build required the wheels to install itself. Even after rolling back to numpy 1.19.3 other problems may occur.
One may occur with following error message during the installation :
> 'ERROR: Could not build wheels for fairseq which use PEP 517 and cannot be installed directly'
This error directly reflects the incompatibility of fairseq installation method with the changed PEP installation methods.
In some this error can be mitigated with the installation of numpy 1.19.3 and not allowing pip to upgrade numpy during 
installation of fairseq. But this solution may not work for all.
Another solution may be `pip install fairseq --no-binary :all:`, but this may not work for all.
Another solution may be `pip install fairseq --no-use-pep517` during its installation. But this also doesnot work for all.
Likewise one can encounter many other problems while installing fairseq on Windows.
But installation on Linux may not have such problems at all.