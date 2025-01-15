---
title: "Whisper Writer_for_dictation"
date: 2025-01-12T21:32:26-05:00
draft: false
tags: ["python", "ai", "windows"]
---

# Install WhisperWriter on Windows
```
D:\Documents> git clone https://github.com/savbell/whisper-writer.git
D:\Documents> cd whisper-writer
```
Read the README.md file, and follow the installation instruction like this:

## Install python and create virtual environment.
I used miniconda, but you can just download the package of v3.11 and install it directly to Windows.

Start "Anaconda prompt" and create a virtual environment of 3.11. 
```
(base) D:\Documents\whisper-writer>conda create -n venv python=3.11
```
If you installed python 3.11 directly, you can do
```
python -m venv venv
venv\Scripts\activate
```

## Install required modules and start the program
```
(venv) D:\Documents\whisper-writer>pip install -r requirements.txt
(venv) D:\Documents\whisper-writer>python run.py
```
Click on Setting button. Modify the language according to your usage senario and select a model depend on your computer. 

## Create a batch file to start it automatically
Create the following batch file on my desktop C:\Users\vma\Desktop\WhiperWriter.bat
```
@echo off
REM Navigate to the folder containing your virtual environment and script
D:
cd /d D:\Documents\whisper-writer

REM Activate the virtual environment
call C:\Users\vma\miniconda3\Scripts\activate.bat venv1

# if you are using a venv module instead of conda
# call venv\Scripts\activate

REM Run the Python script
python run.py

REM Keep the command prompt open after execution
cmd
```
## Double click the batch file and Enjoy it!