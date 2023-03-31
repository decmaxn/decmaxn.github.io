---
title: "Function"
date: 2023-03-24T19:34:48Z
draft: true
---


## main function

Default entry

```go
package main

import (
	"fmt"
)

func main() {
	err, result := DuplicateString("bbb")
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

	if input == "aaa" {
		return fmt.Errorf("I did nothing wrong"), ""
	}
	return nil, input + input
}
```


### 输入参数的两种方法

os.Args, refer to [example](/workspaces/decmaxn.github.io/content/Go/flow-control.md)

flat.Parse, refer to [example](/Go/command-line-parameters.md)

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
```go
```
### 
```go

```