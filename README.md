

Assuming :
 cython source code directory is /path/to/cythondirectory
 fairseq source code directory is /path/to/fairseqdirectory

Run the following commands step by step : 

* mv /path/to/Cythondirectory /path/to/fairseqdirectory
* cd /path/to/fairseqdirectory/Cython
* pip install --editable .
* cd /path/to/fairseqdirectory
* pip install --editable .