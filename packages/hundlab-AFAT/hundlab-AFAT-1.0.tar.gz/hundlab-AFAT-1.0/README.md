# Automated Fibrosis Analysis Toolkit (AFAT)

*This tool was documented in [our paper](http://doi.org/10.1016/j.mex.2019.11.028) on marcophage and fibrosis quantification*

*Hundlab Website: [hundlab.org](http://hundlab.org/)*

*PyPI: [pypi.org/project/hundlab-AFAT](https://pypi.org/project/hundlab-AFAT/)*


*Github: [github.com/hundlab/MAT](https://github.com/hundlab/AFAT)*


## Setup

### Windows

1. Python 3 will need to be installed prior to setting up AFAT, preferably any python
    greater than 3.7. Python 3 can be downloaded from the [python website](http://python.org).
    The x86-64 executable installer is reccommended, as the default install configuration 
    will set python to open .py files by double clicking. If it is installed correctly opening
    cmd or powershell window and typing `py --version` will print the installed python
    version.

2.  Install AFAT by opening a cmd or powershell window and running
    `py -m pip install hundlab-AFAT`, this should install AFAT and all of its dependancies.

3.  Once AFAT has been installed it can be run via cmd, powershell or the start menu. To run
     type `AutomatedFibrosisAnalysisToolkit.py`. To create a desktop shortcut type
     `AutomatedFibrosisAnalysisToolkit.py` into the start menu select `Copy full path`, then on the 
     Desktop `right-click` -> `new` -> `new shortcut` and paste the path when it askes for a
     path.

     If AFAT does not run above as described this means that the python scipts directory has
     not been added to the windows path. To find the install location of python type 
     `py -0p` this will give the location of the python executable. In the same directory
     as python.exe, is a Scripts directory and the `AutomatedFibrosisAnalysisToolkit.py` will
     be in there. Once the AFAT script has been found, a shortcut can be made to it directly
     and placed on the desktop.

*Note that it may take a few seconds for AFAT to start.*

### Mac/Linux

1. Python 3 will need to be installed prior to setting up AFAT. Python 3 can be 
    installed via your package manager in linux, or downloaded from python.org for mac.
    If it is installed correctly opening a terminal and typing `python --version` (in some 
    distributions such as Ubuntu the command is `python3`) should start a python prompt. It 
    may also be necessary to install Tkinter. On unbuntu the package is `python3-tk`.

2. Install AFAT using pip: `python -m pip install hundlab-AFAT`

3. To run AFAT use the command `AutomatedFibrosisAnalysisToolkit.py`

## Usage

TODO!! For now see the paper.

