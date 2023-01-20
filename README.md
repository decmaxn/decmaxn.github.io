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

### host to github pages

Create ```.github/workflows/gh-pages.yml``` with content from Hugo official [instruction](https://gohugo.io/hosting-and-deployment/hosting-on-github/)

That commit will trigger an action. The log of the action shows a error ```Module "LoveIt" is not compatible with this Hugo version; run "hugo mod graph" for more information.```

Based on my local hugo version, which has no problem when doing ```hugo server```, modify the workflow file like this:
```
          hugo-version: '0.68.3'
          extended: true
```

The log of action now have another error ```Error: Error building site: render of "404" failed: execute of template failed: template: 404.html```

Convert content's md files' ```draft: true``` to ```draft: false``` solved this 404 error.

Next error is "the github page isn't here", change ```baseURL = "https://example.com"``` to my the site URL solved this problem.

Finally, chage the repo's "Settings / Code and automation / Pages / Build and deployment / Source" to "deploy from branch" and choice the gh-pages branch.

