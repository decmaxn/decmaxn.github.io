---
title: "Var_primitives_pointer"
date: 2023-02-26T12:40:50-05:00
draft: false
tags: ["coding","Go","course"]
---

# Declaring var with Primitive Data Types
Easy to understand way:
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
```
Normal way:
```go
	num := 11
	greeting := "Hello"
	fmt.Println(num, greeting)
```
declaring multiple vars at the same time
```go
	// Declare three integer variables named "x", "y", and "z" with initial values of 1, 2, and 3, respectively
	x, y, z := 1, 2, 3
	fmt.Println(x, y, z)
	// var x, y, z int = 1, 2, 3
	x, y, z := 1, "hello", true
	fmt.Println(x, y, z)
```

# Pointers
Like in python, big and complex objects are natively pointer, like Slice, Map, Function. Small of simple objects are not, like int, bool, string, array.

Go has a interesting feature to expose this machenisim. For example, declare a var "prt" point to a string variable.
```go
    var prt *string // * is pointer operator 
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