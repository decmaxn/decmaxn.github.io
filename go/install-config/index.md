# Install Config


# Installation

download [Go itself](https://go.dev/dl/) for windows and install, confirm with ```go version``` after. 
```
go version go1.20.1 windows/amd64
```
Use "go help doc" for more information about doc command, for example.
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

