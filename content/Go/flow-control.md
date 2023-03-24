---
title: "Flow Control"
date: 2023-03-21T21:56:10-04:00
draft: true
tags: ["coding","Go","course"]
---

## if

## switch
```go


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
## for-range
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