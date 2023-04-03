---
title: "Method"
date: 2023-03-28T22:35:58-04:00
draft: false
tags: ["coding","Go","course"]
---

## Medthod vs. Function

方法（method）和函数（function）都是用于封装一段代码以便重复使用的工具，但:

1. 方法是与特定类型相关联的函数，它们通过接收器（receiver）来绑定到某个类型上。在方法内部，可以使用接收器来访问该类型的成员变量或方法，从而实现对该类型的操作

1. 函数是一段独立的代码块，在函数内部，可以访问函数内定义的变量，但不能访问其他作用域内的变量或函数。

因此，方法和函数的主要区别在于：

1. 方法是与特定类型相关联的，而函数是独立的。
1. 方法需要通过接收器来访问类型的成员变量或方法，而函数只能访问函数内定义的变量。
1. 方法的定义方式需要指定接收器和方法名称，而函数的定义方式只需要指定函数名称(其实还要包的名字做前缀)即可。

```go
// 先定义一个结构体，名为 Rectangle。 用作 Area和Scale 方法的Receiver
type Rectangle struct {   
    width, height float64
}
// 定义方法 Area用于计算矩形面积，
func (r Rectangle) Area() float64 {
    // 在 Area 方法内部，我们通过 receiver r 来访问 Rectangle 类型的成员变量 width 和 height
    return r.width * r.height
}
// 定义方法 Scale 用于按比例缩放矩形的大小
// 由于需要修改 Rectangle 类型的成员变量，所以我们需要将 receiver 定义为指向 Rectangle 类型的指针
func (r *Rectangle) Scale(scaleFactor float64) {
    // 在方法内部，我们通过 r 指针来访问 Rectangle 类型的成员变量 width 和 height，并按比例缩放它们的值。
    r.width *= scaleFactor
    r.height *= scaleFactor
}

func main() {
    r := Rectangle{3, 4}  // 首先创建一个 Rectangle 类型的变量 r
    fmt.Println(r.Area())  // 调用 Area 方法来计算它的面积: 输出 12
    // 要想改变r object的值，Scale方法必须用r的指针做receiver
    r.Scale(2) // 用 Scale 方法将矩形的大小按比例缩放了两(2)倍
    fmt.Println(r.Area())  // 调用 Area 方法来计算它的面积: 输出 48
}

```