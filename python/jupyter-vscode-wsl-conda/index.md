# Jupyter Vscode in WSL with Conda



## Install WSL 

```powershell
wsl -l -v # list installed distributions
wsl --list --online # list available distributions
wsl --install -d Ubuntu-20.04
# create yourself a user name and password for sudo in future
wsl -l -v # confirm Ubuntu-20.04 is installed
wsl --set-version Ubuntu-20.04 2 # if the version above shows 1 
```

## Install miniconda
Start Ubuntu terminal, and install Miniconda, note to let it initialize for you.
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-Linux-x86_64.sh
sha256sum Miniconda3-py310_23.3.1-0-Linux-x86_64.sh # verify online
bash Miniconda3-py310_23.3.1-0-Linux-x86_64.sh

    Do you wish the installer to initialize Miniconda3
    by running conda init? [yes|no]
    [no] >>> yes
```
This will by default install to ~/miniconda3 folder, and add to the end of .bashrc file:
```bash
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/vma/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/vma/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/vma/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/vma/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
```
Later on, whenever you start shell of this linux env, it will active base env. You can't deactive base env, but you can create/switch to another one.

## vscode setup
Start vscode from your Linux env, make sure you get the default terminal as your Linux env.
```bash
code --install-extension ms-python.python 
code --install-extension ms-toolsai.jupyter
conda install -n base ipykernel --update-deps --force-reinstall
code random_file_name.py
```
Click on "Select interpreter" link in the lower right corner of vscode. Select the python installed by Conda. 

Restart vscode

## First jupyter Notebook

Use vscode's Command Palette to "create a new Notebook". Try add a markdown section and a "Code" section.

The following error will show if you haven't complete the vscode setup section above.
```
Running cells with 'base' requires the ipykernel package.
Run the following command to install 'ipykernel' into the Python environment. 
Command: 'conda install -n base ipykernel --update-deps --force-reinstall'
```
Save the file, be aware it will be rendered by vscode when you open it. 

## Nice to have but not relaeted to this topic: Install Docker Desktop 
Run "command prompt" or powershell as Administrator:
```powershell
choco install docker-desktop
# Settings, General, "Use the WSL 2 based engine"
```
Open WSL Ubuntu shell:
```bash
docker version
docker run hello-world
```
