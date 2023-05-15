# Install_and_Config


## Installation

download [Go itself](https://go.dev/dl/) for windows and install, confirm with ```go version``` after. 
```
go version go1.20.1 windows/amd64
```
For linux: https://go.dev/doc/install
```bash
wget https://go.dev/dl/go1.20.4.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.20.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go version
```

## Configuration

### Use "go help doc" for more information about doc command
```
> go doc json.Decoder.Decode
package json // import "encoding/json"

func (dec *Decoder) Decode(v any) error
    Decode reads the next JSON-encoded value from its input and stores it in the
    value pointed to by v.

    See the documentation for Unmarshal for details about the conversion of JSON
    into a Go value.
```
json package, Decoder object within json package, and Decode method on that Decoder object.

### IDE

Install vscode using choco and confirmed with ```choco list -l```
```
vscode 1.70.1
vscode.install 1.70.1
```

After installing golang.go extension.  Got a prompt to install the gopls and go-ouitline.

```bash
code --install-extension golang.go 
```

Now, try creat a hello world program and try to features of those tool

1. type pack to see it suggests {}package main
2. type fm to see it suggests func main{}
3. type fmt.Println("Hello world!") slowly to see it suggests the rest.
4. save this file to see it added import "fmt"
5. start a terminal and use go run . to see it runs properly.

Suggest to install ```go  code --install-extension formulahendry.code-runner```, this way you can run go file with an shortcut.

### GOPATH

This is where the packages live, weather download with go get command or created by your self.

Since Go 1.11, you don't have to use GOPATH anymore. Simply go to your project directory and do this once: 

```bash
$ go mod init github.com/decmaxn/goLab
go: creating new go.mod: module github.com/decmaxn/goLab
$ go run github.com/decmaxn/goLab
Hello world!
```
For older version of Go, you need to set and export it. To be compatible with old packages, it's BEST to set it.

```bash
$ tail -3 ~/.bashrc 
export GOROOT=/usr/lib/go
export GOPATH=$HOME/go
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
```
After the $GOPATH in place, you can go get another package online, like the command example above.

