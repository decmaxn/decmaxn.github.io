---
title: "Function"
date: 2023-03-24T19:34:48Z
draft: false
tags: ["coding","Go","course"]
---

## 声明

func identifier(输入参数) (输出参数) {body 逻辑}

## main function

Default entry

```go
package main

import (
	"fmt"
)

func main() {
	err, result := DuplicateString("humble")
	if err != nil {   //因为Go多值返回被用于错误处理，这句大量被使用
		fmt.Println(err)
	} else {
		fmt.Println(result)
	}
}
// 如果一个函数需要返回一个错误，可以将其定义为返回值的第一个元素，并将其类型指定为 error。
// 这里的 (input string) 是一个string类型的输入值
// 这里的 (error, string) 实际上是两个类型，分别是 error 和 string。放在一起表示返回两个值
func DuplicateString(input string) (error, string) {

	if input == "humble" {
		return fmt.Errorf("It's not going to work"), ""
	}
	return nil, input + input
}
```


### 输入参数的两种方法

os.Args, refer to [example](../flow-control/#switch)

flat.Parse, refer to [example](../command-line-parameters)

## Init function

在 Go 语言中，每个包可以包含一个 init 函数。 

1. 它是自动执行的，无法手动调用。

1. 它没有参数和返回值，它的作用是在程序启动时完成一些初始化工作。

1. 它的执行顺序是按照导入包的顺序决定的。

具体来说，当一个程序运行时，它会按照以下步骤加载包：

1. 首先，对于每个包，Go 语言会解析该包的所有依赖项，并递归地加载它们。

1. 对于每个包，Go 语言会检查是否存在它。如果存在，就将该函数加入到待执行列表中。

1. 当所有依赖项都加载完成后，Go 语言会按照导入包的顺序依次执行每个包的 init 函数。
	
1. 需要注意的是，每个包的 init 函数只会被执行一次，即使该包被导入了多次。

> 被导入的包的 main 函数不会被执行。main 函数只会在程序的入口包中执行。

## 返回值

### 任意多返回值
常用于错误处理

### 命名返回值
被命名的返回值等同于在函数里被声明过了

```go
func DuplicateString(input string) (err error, result string) {

	if input == "humble" {
		err = fmt.Errorf("It's not going to work"), ""
		return
	}
	result = nil, input + input
	return
}
```
## 可变长度的输入参数
Allow caller to put in as many as you want parameters with same type. Here is an example frm Go itself.

Define it with ... before input Type

```go
// 接受一个切片 slice 和零个或多个类型为 Type 的参数 elems，并返回一个新的切片。
func append(slice []Type， elems ...Type) []Type
// slice []Type：第一个参数是一个切片，类型为 []Type。Type 是指定切片中元素的类型。
// elems ...Type：第二个参数是可变参数，可以接受任意数量的类型为 Type 的参数。
// 				  通过使用 ... 来表示该参数是可变参数。
// []Type：表示函数的返回类型为一个切片，其中元素的类型为 Type。
```
Call it with multiple 参数
```go
mySlice := []String{}
mySlice = append(mySlice, "a", "1", "c")
```

## 内置函数
不需要package name, 比如 close(), len() 等等。

## Callback 回调函数
函数作为另一个函数的参数， 并在这个函数内部被调用。
```go
func main() {
	DoOperation(1, increase)
	DoOperation(1, decrease)
}
func DoOperation(y int, f func(int, int)) {
	f(y, 1)
}
func increase(a, b int) {
	println("Increase result is:", a+b)
}
func decrease(a, b int) {
	println("Decrease result is:", a-b)
}
```
应用实例，比如遍历树节点，根据节点不同而采用不同的逻辑（function）处理这个节点。

