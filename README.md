# Victor Ma

<img width="200" height="200" src="static/images/avatar.png" alt="Victor Ma Avatar" />

## Overview
This blog uses [LoveIt](https://themes.gohugo.io/themes/loveit/) theme

## Build and Tooling

### Initialize the site

```
$ hugo new site decmaxn.hithub.io && cd decmaxn.hithub.io 
$ Github Repo creation
$ git init
$ git add .
$ git commit -m "hugo new site"
$ git branch -M main
$ git remote add origin https://github.com/decmaxn/decmaxn.github.io.git
$ git push -u origin main
```

### Initialize the Theme

```
$ git submodule add https://github.com/dillonzq/LoveIt themes/LoveIt
$ cp themes/LoveIt/exampleSite/config.toml .
$ hugo server -D
Error: module "LoveIt" not found; either add it as a Hugo Module or store it in "/home".: module does not exist
```
Above problem can be solved by modify config.toml to replace ```themesDir = "../.."``` with ```themesDir = "themes"```

Test by add one post

```
$ hugo new posts/mypost1.md
$ hugo server -D
```

### Migrate existing Blogger site here using [blogimport](https://github.com/natefinch/blogimport)

First make a backup xml file "blog-01-15-2023.xml" of my Blogger site and install GO properly.

```
$ git clone https://github.com/natefinch/blogimport
$ cd blogimport
$ go run main.go ~/Downloads/blog-01-15-2023.xml ../decmaxn.github.io/content/posts
```
There is a log of errors when testing with ```hugo server```, I make the following 2 changes to fix that:
1. Made sure there is not double quotes in the title of each markdown file imported
2. Remove every imported markdown file has no Author section.