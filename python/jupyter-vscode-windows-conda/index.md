# Jupyter Vscode Windows Conda


Before this procedure, I already have python 3.8.2 installed, not with Choco.
```powershell
PS C:\Users\vma> py -0p
Installed Pythons found by C:\WINDOWS\py.exe Launcher for Windows
 -3.8-64        C:\Users\vma\AppData\Local\Programs\Python\Python38\python.exe *

PS C:\Users\vma> Get-Command python

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Application     python.exe                                         3.8.215... C:\Users\vma\AppData\Local\Programs\Python\Pyth...

```
## Conda

> Conda 是 Miniconda 和 Anaconda 的核心组件.  Miniconda 是一个精简版的 Anaconda.

I didn't use choco install miniconda3, as it's not up to date and has complains.

1. Download Miniconda3-py310_23.3.1-0-Windows-x86_64.exe
1. from https://docs.conda.io/en/latest/miniconda.html#installing
1. and  Install for myself

Miniconda installers contain the conda package manager and Python. 

There are two variants of the installer: Miniconda is Python 2 based and Miniconda3 is Python 3 based. 

Note that the choice of which Miniconda is installed only affects the root environment. Regardless of which version of Miniconda you install, you can still install both Python 2.x and Python 3.x environments. ```$ conda create -n myenv python``` will be to install Python 2.7 with the Python 2 Miniconda and to install Python 3.10 with the Python 3 Miniconda.

```powershell
PS C:\Users\vma> py -0p
Installed Pythons found by C:\WINDOWS\py.exe Launcher for Windows
 -3.8-64        C:\Users\vma\AppData\Local\Programs\Python\Python38\python.exe *
 -3.10-64       C:\Users\vma\miniconda3\python.exe
```
### Manage conda environments

When you begin using conda, you already have a default environment named base. You don't want to put programs into your base environment, though. Create separate environments to keep your programs isolated from each other.

Create a new environment and install a package in it. For example, We will name the environment snowflakes and install the package BioPython. 
```powershell
conda create --name snowflakes biopython
#To use, or "activate" the new environment, type the following:
conda activate snowflakes
```
conda activate only works on conda 4.6 and later versions.

## vscode setup
Start vscode, open a command prompt terminal.
```bash
code --install-extension ms-python.python 
code --install-extension ms-toolsai.jupyter
conda install -n base ipykernel --update-deps --force-reinstall
code random_file_name.py
```
Click on "Select interpreter" link in the lower right corner of vscode. Select the python installed by Conda. 

Restart vscode

## First jupyter Notebook

Refer to [First jupyter Notebook](../jupyter-vscode-wsl-conda#first-jupyter-notebook)

