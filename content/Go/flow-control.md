---
title: "Flow Control"
date: 2023-03-21T21:56:10-04:00
draft: false
tags: ["coding","Go","course"]
---

## if
```go
package main

import "fmt"

func main() {
    var x int = 5
	// if x:= 5; x >10 { 类似 for, 可以在条件表达式前执行一个简单语句。这里可以取代上下两句
    if x > 10 {
        fmt.Println("x is greater than 10")
    } else if x > 5 {
        fmt.Println("x is greater than 5 but not greater than 10")
    } else {
        fmt.Println("x is less than or equal to 5")
    }
}
```
## switch
```go
package main

import (
    "fmt"
    "os"
)

func main() {
    var fruit string

    if len(os.Args) > 1 {
        fruit = os.Args[1]
    } else {
        fruit = "" // Default value
    }

    switch fruit {
    case "banana":
        fmt.Println("This is a banana.")
    case "apple":
        fmt.Println("This is an apple.")
    case "orange":
        // This is a blank branch 空分枝
    case "pear":
        fmt.Println("This is a pear.")
        fallthrough // 穿透 will cause the next case to be executed
    case "peach":
        fmt.Println("This is a peach.")
    default:
        fmt.Println("I'm not sure what fruit this is.")
    }
}
```
```bash
$ go run main.go // 付空值，不在任何选择中，所以到 default
I'm not sure what fruit this is. 
$ go run main.go apple
This is an apple.
$ go run main.go orange // 空分枝，此处没做任何事
$ go run main.go pear // fallthrough, 也执行下一个选择
This is a pear.
This is a peach. 
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

}
```
###  for-range
```go
package main

import (
	"fmt"
)

func main() {
	fullString := "hello U"
	fmt.Println(fullString)
	for i, c := range fullString { // assign index and value at the same time
		fmt.Println(i, string(c))
	}

}
```

### break and continue
1. break: jump out the loop
1. continue: jump to next item

## lable and goto
Not suggested since it's confusing.