# Install Config


# Installation

download [Go itself](https://go.dev/dl/) for windows and install, confirm with ```go version``` after. 
```
go version go1.20.1 windows/amd64
```
## Use "go help doc" for more information about doc command
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


Install vscode using choco and confirmed with ```choco list -l```
```
vscode 1.70.1
vscode.install 1.70.1
```

After installing golang.go extension.  Got a prompt to install the gopls and go-ouitline. 

Now, try creat a hello world program and try to features of those tool

1. type pack to see it suggests {}package main
2. type fm to see it suggests func main{}
3. type fmt.Println("Hello world!") slowly to see it suggests the rest.
4. save this file to see it added import "fmt"
5. start a terminal and use go run . to see it runs properly.

Also create a project and try it.

```bash
$ go mod init github.com/decmaxn/goLab
go: creating new go.mod: module github.com/decmaxn/goLab
$ go run github.com/decmaxn/goLab
Hello world!
```
