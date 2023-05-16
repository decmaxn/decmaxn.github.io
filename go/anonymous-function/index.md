# Anonymous Function


## 闭包 （匿名函数）

### 不能独立存在，只能存在于其他函数中

### 可以赋值给其他变量 

```x:=func(){}```，其实就是声明
函数也是一种数据类型，因为它虽然不是变量，但是存在于内存中的地址块。函数名的本质是一个指向其内存地址的针常量。


### 可以直接掉用
```func(x,y int){println(x+y)}(1,2)```
注意直接调用是在声明的后面加上参数，其实就是 invoke 的格式。 

function 不等同于 invoke function

### 可以作为函数返回值
1. func：表示这是一个函数。
1. Add：是函数的名称。
1. ()：是函数的参数列表。在这个例子中，Add 函数没有接受任何参数。
1. (func(b int) int)：是函数的返回类型是一个函数。
	1. 这个函数接受一个整数参数 b，返回一个整数值。 

```go
func Add() (func(b int) int) {
    sum := 0

    // 返回一个函数，该函数将参数与 sum 相加并返回
    return func(b int) int {
        sum += b
        return sum
    }
}

func main() {
	// addFunc 就是那个返回的函数
    addFunc := Add()

    result := addFunc(5)   // 调用返回的函数，将 5 与 sum 相加
    fmt.Println(result)    // 输出结果：5

    result = addFunc(10)   // 再次调用返回的函数，将 10 与 sum 相加
    fmt.Println(result)    // 输出结果：15
}
```

