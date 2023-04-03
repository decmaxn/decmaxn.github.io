---
title: "Interactive Login and Non Login Shell"
date: 2023-03-22T16:35:32-04:00
draft: false
tags = ["Shell","Linux"]
---

## TL;DR  

.bash_profile 和 .bashrc 文件包含在 Bash shell 启动时要运行的 shell 命令。.bash_profile 文件在交互式登录 shell 中被读取和执行，而.bashrc 文件在非登录 shell 中被读取和执行。

.profile 文件是一个针对 Unix shell（如 bash、sh、ksh 等）的配置文件。当使用 Unix shell 登录时，它会在用户主目录下寻找并执行该文件。与 .bash_profile特定于 bash shell不同，.profile 文件适用于多种 Unix shell，因此具有更广泛的适用性。

### vscode 

In vscode, the terminal wil run .profile, which will call .bashrc. So let's put all command completers or PATH in .bashrc

## SHELL 交互式和非交互式 登录和非登录

在 Unix/Linux 系统中，有 交互式（interactive）和非交互式 两种 shell。  
    1. 交互式是指可以从终端或命令行界面中输入和接收命令的 shell。
    1. 非交互式没有终端，比如运行一个脚本时。

交互式 shell有两种类型：登录 shell 和非登录 shell。下面详细介绍交互式登录和非登录 shell 的概念。

    1. 交互式登录 shell：当您首次登录到 Unix/Linux 系统时，系统会要求您输入用户名和密码。此时，系统会在系统中为您创建一个新的 shell 进程，并将其标识为登录 shell。登录 shell 通常会执行用户的登录脚本（例如 .bash_profile），以初始化 shell 的环境变量、别名和函数等。在登录 shell 中，您可以通过终端或命令行界面输入命令，并且这些命令将在 shell 中运行。

    1. 交互式非登录 shell：当您在系统中已经登录并打开了一个终端或命令行界面时，您可以通过输入命令打开一个新的 shell 进程。此时，系统会为您创建一个新的 shell 进程，并将其标识为非登录 shell。与登录 shell 不同，非登录 shell 通常不会执行用户的登录脚本，而是执行用户的 shell 配置文件（例如 .bashrc）。在非登录 shell 中，您也可以通过终端或命令行界面输入命令，并且这些命令将在 shell 中运行。

需要注意的是，当您使用 ssh 或其他远程登录工具远程登录到 Unix/Linux 系统时，系统会将您的登录 shell 标识为交互式登录 shell。而在本地打开终端或命令行界面时，系统会将您的 shell 标识为交互式非登录 shell。

