---
title: "Constant"
date: 2023-02-26T15:04:15-05:00
draft: false
tags: ["coding","Go","course"]
---

## 声明

const identifier type = value

Normal side of Go constant:
1. declare and assign at the same time, can not be done separately. 
2. Value has to be determined in complie time, not run time
3. The type of constant can be implicit, or explicit if you need to

```go
	const pi = 3 // type not assigned
	fmt.Println(pi)  // pi is treated as int
    fmt.Println(pi + 0.14) // pi is treated as float
	pi = 3.1415 // you can NOT　change value of a constant（这是与VAR的区别）
    //./main.go:10:5: cannot assign to pi
```

## 在K8s中用法示例： 类型重命名

These list of const have been limited to a new string type "ServiceType", so you will never have a typo on the strings. 

```go
type ServiceType string

const (
	ServiceTypeClusterIP ServiceType = "ClusterIP"
	ServiceTypeNodePort ServiceType = "NodePort"
	ServiceTypeLoadBalancer ServiceType = "LoadBalancer"
	ServiceTypeExternalName ServiceType = "ExternalName"
)
```
## Iota

Constant block, you can have multiple of them and iota will start from 0 in each block.
```go
const (
	pi       = 3
	greeting = "hello"
)
```
You can build long chain of constants using iota.
```go
const (
	Monday    = iota // 0 iota starts at 0 and increase by 1 every time it is used
	Tuesday          // 1 reuse the constant expression above, 
	Wednesday        // 2 which is simply iota
	Thursday         // 3 其实就是行数
	Friday           // 4
	Saturday         // 5
	Sunday           // 6
)
```
You can also use complex constant expresssion
```go
const (
	_  = iota             // Ignore the first iota, which is 0
	KB = 1 << (10 * iota) // 1 << (10 * 1)，bit shift operator
	MB                    // 1 << (10 * 2)，same as 1 times 2^20
	GB                    // 1 << (10 * 3)，2^10 = 1024...
	TB                    // 1 << (10 * 4)，
)
```
The purpose of iota is for convinient.

## 跨包全局常量（或变量）

名字首字母大写即可