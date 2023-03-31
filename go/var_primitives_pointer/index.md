# Var_primitives_pointer


## Declaring var with Primitive Data Types
Primitive Data Types 指的是一些基本的数据类型，这些类型不依赖于其他类型，是构成更复杂的数据类型的基础

函数外的每个语句都必须以关键字开始(var, func 等等)
```go
	var num int
	num = 11
	fmt.Println(num)
```
Esay to write way:
```go
	var num int = 11
	var greeting string = "Hello"
	fmt.Println(num, greeting)
	// 如果初始化值已存在，则可以省略类型;变量会从初始值中获得类型
	var i,j = 1,2
```
在函数中，简洁赋值语句 := 可在类型明确的地方代替 var 声明。
```go
	num := 11
	greeting := "Hello"
	fmt.Println(num, greeting)
```
declaring multiple vars at the same time
```go
	// Declare three integer variables named "x", "y", and "z" with initial values of 1, 2, and 3, respectively. GO简洁的特色！
	x, y, z := 1, 2, 3
	fmt.Println(x, y, z)
	// var x, y, z int = 1, 2, 3
	x, y, z := 1, "hello", true
	fmt.Println(x, y, z)
```
### 显示转换 and 类型推到

```go
num := 11
float64 := float64(num)
// 隐式转换导致容易混淆
var i int
j := i // j is a int from i
```

## Pointers
Like in python, big and complex objects are natively pointer, like Slice, Map, Function. Small of simple objects are not, like int, bool, string, array.

Go has a interesting feature to expose this machenisim. For example, declare a var "prt" point to a string variable.
```go
    var prt *string // *string is a type 
	fmt.Println(prt)
    // <nil>  This is an empty pointer, since prt has not been initiallized
    var greeting string = "hello"
	prt = &greeting // & is "address operator". 
	fmt.Println(prt)
    // 0xc0000741e0  address of greet var
```
Using dereference operator in '*prt' expression access the varlue of string var "greeting".
```go
    *prt = "world"  // * is dereference operator 
	fmt.Println(greeting)
    // world  - no longer hello
```
However, if you haven't initialize prt var, it's going to fail.
```go
	var prt2 *string
	*prt2 = "world"
	fmt.Println(*prt2)
    // panic: runtime error: invalid memory address or nil pointer dereference
```
One way to fix it without create a string var is:
```go
	var prt2 *string = new(string)
	*prt2 = "world"
	fmt.Println(*prt2)
```
Since pointer arithmetic is dangous, Go doesn't allow it.
