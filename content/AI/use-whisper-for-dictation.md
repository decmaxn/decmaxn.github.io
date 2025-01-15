---
title: "Use Whisper for Dictation"
date: 2023-04-18T23:18:59-04:00
draft: false
tags: ["python", "ai", "windows", "conda"]
---

## Install python

Refer [Install python with Miniconda](../jupyter-vscode-windows-conda#conda) to install python 3.10.10

## Install PyTorch

Get the following conda command from https://pytorch.org/get-started/locally/
```powershell
# Start "Anaconda prompt", or 
%windir%\System32\cmd.exe "/K" C:\Users\vma\miniconda3\Scripts\activate.bat C:\Users\vma\miniconda3

conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

## Install Chocolatey
Refer https://chocolatey.org/Finstall to get a one liner (from Administrator prompt) like this:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

## Install FFMPEG

To read different formats of audio files. run the following command from Administrator prompt to install.
```powershell
choco install ffmpeg
```

## Install Whisper
Refer https://github.com/openai/whisper to get instructions.
```powershell
pip install -U openai-whisper
```

## Use Whisper
1. set language can save time to detect languages.
1. fp16 False is for CPU machine.
1. Refer to [Available models and languages](https://github.com/openai/whisper#available-models-and-languages) for --model choices.

```powershell
# Start "Anaconda prompt", or 
%windir%\System32\cmd.exe "/K" C:\Users\vma\miniconda3\Scripts\activate.bat C:\Users\vma\miniconda3

(base) C:\Users\vma\Documents\Sound recordings>whisper Recording.m4a --language Chinese --fp16 False --model medium
```
> medium is the sweet spot, much better than default and faster than large.

You can also translate (only to English) with --task translate option.

