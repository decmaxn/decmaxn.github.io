---
title: "Command Line Parameters"
date: 2023-03-21T22:08:44-04:00
draft: true
---

Example from https://github.com/cncamp/golang.git

```bash
$ cat <<EOF > main.go
> package main
> 
> import (
>         "flag"
>         "fmt"
>         "os"
> )
> 
> func main() {
>         name := flag.String("name", "world", "specify the name you want to say hi")
>         flag.Parse()
>         fmt.Println("os args is:", os.Args)
>         fmt.Println("input parameter is:", *name)
>         fullString := fmt.Sprintf("Hello %s from Go\n", *name)
>         fmt.Println(fullString)
> }
> EOF
$ go fmt main.go  # if the format messed up during copy/paste
$ go build main.go 

$ ./main 
os args is: [./main]  # the whole command line from OS
input parameter is: world  # the default name is world
Hello world from Go

$ ./main fake_parameter
os args is: [./main fake_parameter]
input parameter is: world
Hello world from Go

$ ./main --name vma
os args is: [./main --name vma]
input parameter is: vma  # flag parsed --name vma to a named parameter
Hello vma from Go
```
This remind me about kubectl command parameters
 
## vet
 ```bash
 $ cat <<EOF > main.go
> package main
> 
> import (
>         "fmt"
> )
> 
> func main() {
>         name := "testing"
>         fmt.Printf("%d\n", name)
>         fmt.Printf("%s\n", name, name)
> }
> EOF
$ go vet main.go
# command-line-arguments
./main.go:9:9: Printf format %d has arg name of wrong type string
./main.go:10:9: Printf call needs 1 arg but has 2 args
```

## for loop
```go
package main

import (
	"fmt"
)

func main() {
	// take away i := 0; i < 3 will make a endless loop
    // take away i := 0 and i++ make it same with while ( you need to change i inside the loop)
	for i := 0; i < 3; i++ {
		fmt.Println(i)
	}
	fullString := "hello U"
	fmt.Println(fullString)
	for i, c := range fullString { // assign index and value at the same time
		fmt.Println(i, string(c))
	}

}
```