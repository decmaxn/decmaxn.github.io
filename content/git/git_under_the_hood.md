---
title: "What_is_git"
date: 2023-02-20T15:05:13-05:00
draft: false
tags: ["coding","git","course"]
---

# Meet SHA1 
Every Object in Git has its own SHA1.  SHA1 are unique in the universe?!
> This cryptograph concept and technology is also used for bitcoin.

```bash
:~$ mkdir gitdemo
:~$ cd gitdemo/
:~/gitdemo$ echo "Apple Pie" | git hash-object  --stdin # Create a SHA1. 
23991897e13e47ed0adb91a0082c31c82fe0cbe5
:~/gitdemo$ echo "Apple Pie" | git hash-object  --stdin -w # -w write it to GIT repository. 
fatal: Not a git repository (or any of the parent directories): .git
:~/gitdemo$ git init # Create a workplace
Initialized empty Git repository in /home/vma/gitdemo/.git/
:~/gitdemo$ ls -a
.  ..  .git   # .git makes it a repo and keeping every thing in.

:~/gitdemo$ echo "Apple Pie" | git hash-object  --stdin -w  # it works now after the workplace is created 
23991897e13e47ed0adb91a0082c31c82fe0cbe5
:~/gitdemo$ ls -la .git/objects/23/991897e13e47ed0adb91a0082c31c82fe0cbe5 # the file created
-r--r--r-- 1 vma vma 26 Jun  4 14:13 .git/objects/23/991897e13e47ed0adb91a0082c31c82fe0cbe5
:~/gitdemo$ git cat-file 23991897e13e47ed0adb91a0082c31c82fe0cbe5 -t # Type of the SHA1
blob
:~/gitdemo$ git cat-file 23991897e13e47ed0adb91a0082c31c82fe0cbe5 -p # Content of the SHA1
Apple Pie
```

# Content Tracker

Let's make a commit with 3 files, in 2 folders. Two of the files have same content.

```bash
:~$ mkdir gitdemo1
:~$ cd gitdemo1
:~/gitdemo1$ echo "Apple Pie" > menu.txt    # Content is same with recipes/apple_pie.txt
:~/gitdemo1$ mkdir recipes
:~/gitdemo1$ echo "One receipe per file please" > recipes/README.txt
:~/gitdemo1$ echo "Apple Pie" > recipes/apple_pie.txt
:~/gitdemo1$ git init  # The .git directory has nothing new
Initialized empty Git repository in /home/vma/gitdemo1/.git/
:~/gitdemo1$ git status # GIT doesn't know what to do with these files
On branch master

Initial commit

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        menu.txt
        recipes/

nothing added to commit but untracked files present (use "git add" to track)
:~/gitdemo1$ git add menu.txt # file can be added
:~/gitdemo1$ git add recipes/ # Directory and files under it can be added
:~/gitdemo1$ git status
On branch master

Initial commit

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   menu.txt
        new file:   recipes/README.txt
        new file:   recipes/apple_pie.txt

:~/gitdemo1$ git commit -m "First commit!"  
[master (root-commit) acc3790] First commit!
 3 files changed, 3 insertions(+)
 create mode 100644 menu.txt
 create mode 100644 recipes/README.txt
 create mode 100644 recipes/apple_pie.txt
:~/gitdemo1$ git log 
commit acc3790dd4196ddb0109da375f44574b36ac42f3
Author: Your Name <you@example.com>
Date:   Sun Jun 4 14:29:05 2017 -0400

    First commit!
```
# Let's see the content, and type.
```bash
:~/gitdemo1$ cd .git ; tree objects 
objects
├── 23 # SHA1 of the menu.txt and recipes/apple_pie.txt
│   └── 991897e13e47ed0adb91a0082c31c82fe0cbe5
├── 40 # SHA1 of the README.txt file
│   └── fd423f20087b88abfe1d0938b3eb1b60203063
├── ac #  The SHA1 of the commit itself 
│   └── c3790dd4196ddb0109da375f44574b36ac42f3 
├── b3 # SHA1 and type of the root folder.
│   └── 6957a8fcacfd058efe81cd78d23e1905e8aea4
├── c7 # SHA1 of the recipes folder
│   └── c5f73d3b5f56ed11817709b3a2a7a86379b6a7
├── info
└── pack
# Every sub-folders together with the file name blow is a SHA1
# GIT save files this way to limit too much items in one directory
7 directories, 5 files

:~/gitdemo1/.git$ git cat-file acc3790dd4196ddb0109da375f44574b36ac42f3 -p
tree b36957a8fcacfd058efe81cd78d23e1905e8aea4 # commit includes root folder
author Your Name <you@example.com> 1496600945 -0400
committer Your Name <you@example.com> 1496600945 -0400

First commit!
:~/gitdemo1/.git$ git cat-file acc3790dd4196ddb0109da375f44574b36ac42f3 -t
commit # type of the SHA1 is commit
```

# Let's see the content, and type of a directory "recipes", and content of directory "."
```bash
:~/gitdemo1/.git$ git cat-file c7c5f73d3b5f56ed11817709b3a2a7a86379b6a7 -t
tree # # type of the SHA1 is tree
:~/gitdemo1/.git$ git cat-file c7c5f73d3b5f56ed11817709b3a2a7a86379b6a7 -p
100644 blob 40fd423f20087b88abfe1d0938b3eb1b60203063    README.txt
100644 blob 23991897e13e47ed0adb91a0082c31c82fe0cbe5    apple_pie.txt 
:~/gitdemo1/.git$ git cat-file b36957a8fcacfd058efe81cd78d23e1905e8aea4 -p
100644 blob 23991897e13e47ed0adb91a0082c31c82fe0cbe5    menu.txt
040000 tree c7c5f73d3b5f56ed11817709b3a2a7a86379b6a7    recipes
```

# There are 3 files, why only 2 SHA1 left?
TWO files have same content, thus shared the same SHA1!!! 
```bash
:~/gitdemo1/.git$ git cat-file 40fd423f20087b88abfe1d0938b3eb1b60203063 -t
blob
:~/gitdemo1/.git$ git cat-file 23991897e13e47ed0adb91a0082c31c82fe0cbe5 -p
Apple Pie
:~/gitdemo1/.git$ git cat-file 40fd423f20087b88abfe1d0938b3eb1b60203063 -p
One receipe per file please
```
So SHA1 is the unique identifier of the blob, and the blob itself will not be saved twice, even it will show up in other places of the directory, due to the content of the tree.  What a brilliant idea! 

Also commit is point to tree, make it link to a certain version:- 

# Versioning made easy

```bash
:~/gitdemo1/.git$ cd ..
:~/gitdemo1$ echo "Cheescake" >> menu.txt # modify a file 
:~/gitdemo1$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   menu.txt

no changes added to commit (use "git add" and/or "git commit -a")
:~/gitdemo1$ git add menu.txt
:~/gitdemo1$ git commit -m "Add cake"
[master b05633d] Add cake
 1 file changed, 1 insertion(+)
:~/gitdemo1$ git status
On branch master
nothing to commit, working directory clean
:~/gitdemo1$ git log
commit b05633d30ed6700852d5e1b8a38c2569f1ad0263  # Here is the SHA1 of the new commit.
Author: Your Name <you@example.com>
Date:   Sun Jun 4 15:00:04 2017 -0400

    Add cake

commit acc3790dd4196ddb0109da375f44574b36ac42f3
Author: Your Name <you@example.com>
Date:   Sun Jun 4 14:29:05 2017 -0400

    First commit!
:~/gitdemo1$ git cat-file b05633d30ed6700852d5e1b8a38c2569f1ad0263 -p
tree a74452e195a35c8b8c7c3d01e982cf1fdcd4165d  # Here is the SHA1 of the new directory.
parent acc3790dd4196ddb0109da375f44574b36ac42f3 # Here is the SHA1 of the old. commit.
author Your Name <you@example.com> 1496602804 -0400
committer Your Name <you@example.com> 1496602804 -0400

Add cake
:~/gitdemo1$ git cat-file a74452e195a35c8b8c7c3d01e982cf1fdcd4165d -p
100644 blob 84678c2bdfee0c6410d38a09126691b76f45ce0d    menu.txt #new directory is due to a new file
040000 tree c7c5f73d3b5f56ed11817709b3a2a7a86379b6a7    recipes # old SHA1 is still there
:~/gitdemo1$ git cat-file 84678c2bdfee0c6410d38a09126691b76f45ce0d -p
Apple Pie
Cheescake
```

# So one more of commit, tree and file are added to this system. 
```bash
:~/gitdemo1$ git count-objects
8 objects, 32 kilobytes
```
IT STILL SAVE OBJECT ONLY ONCE EVEN AFTER VERSIONING. It's believed it's also avoid save same block of content twice! 

# What is Tag
```bash
:~/gitdemo1$ git tag -a mytag -m "I love cheesecake"
:~/gitdemo1$ git tag
mytag
:~/gitdemo1$ git cat-file -p mytag # view content of the tag
object b05633d30ed6700852d5e1b8a38c2569f1ad0263  # It's point to a commit. 
type commit
tag mytag
tagger Your Name <you@example.com> 1496605763 -0400

I love cheesecake
```