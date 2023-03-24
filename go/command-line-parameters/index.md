# Command Line Parameters


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

