# Go Commands


## Some go commands
### build - complile packages and dependencies
```bash
$ go build main.go
$ ls 
main  main.go
$ ./main
Hello world
$ GOOS=linux GOARCH=amd64 go build main.go
$ ./main
 error if this is not linux os and amd64 arch
```
### fmt, like linter - gofmt(reformat) package sources
```bash
$ go fmt main.go
```
### get - add dependencies to current module and install them
```bash
$ go get github.com/decmaxn/goLab
# Above command will use git to pull and create the following folder
$ ls -l $GOPATH/src/github.com/decmaxn/goLab
```
install - compile and install packages and dependencies. 
    Use this in dockerFile together with source code, instead of add prebuilt package binary, to make sure compatibility.

### mod - module maintenance. Created by community
```bash
$ go mod init github.com/decmaxn/goLab
go: creating new go.mod: module github.com/decmaxn/goLab
$ go run github.com/decmaxn/goLab
Hello world!
```
### test 

Go doesn't support assert natively, we can use "github.com/stretchr/testify/assert"

convention: We have foo.go together with foo_test.go in the same place, always.

test command can run all *_test.go in the folder.

### vet
Find error which can pass build phrase without error out. For example, a boolean check will always return true or false.
