---
title: "Array_slice"
date: 2023-02-26T15:48:50-05:00
draft: false
tags: ["coding","Go","course"]
---

# Array
Similar with Python's array， array in Go is also a continues memoery block in fixed size, so it's faster but not dynamic. 

It also stores same type objects.

What different is Go array is not a pointer. 在 Go 中，数组是值类型，传递数组作为参数时会复制整个数组。而在 Python 中，数组（列表）是引用类型，传递数组作为参数时传递的是指向数组的引用，不会复制整个数组。

```go
	var myarray [3]int // signature of array is [size]type
	fmt.Println(myarray)
    // [0 0 0]
	myarray[0] = 3
	fmt.Println(myarray[0])
    // 3
	arr := [3]int{1, 2, 3} // declare implicitly, it's not [1 2 3]
	fmt.Println(arr)
    // [1 2 3]
```

# Slice

Slice from an array, or another slice.

Python提供了切片（Slice）操作符，主要用于对下标操作的时候。简化对数组的操作。每一个切片返回的数据都是原数组的一个副本。不会对原数组有影响. Go与Python完全不一样的是，切片并不存储任何数据，它只是描述了底层数组中的一段。更改切片的元素会修改其底层数组中对应的元素。与它共享底层数组的切片都会观测到这些修改。

```go
	myslice := arr[:]  // implicitly, : means from index 0 to last
	fmt.Println(myslice)
    // [1 2 3]
	myslice2 := arr[:2] // from index 0 to 2, not inclusive 
	fmt.Println(myslice2)
    // [1 2]
    myslice3 := arr[1:] // from index 1 to last
	fmt.Println(myslice3)
    // [2 3]
	arr[0] = 11
	myslice2[1] = 22
	fmt.Println(arr, myslice, myslice2) //they point to the same
    // [11 22 3] [11 22 3] [11 22] 
```

Since most of time you work with slice only, you don't really care about array under it as long as it is managed for you.
```go
	slice := []int{1, 2, 3} // note for slice, you don't mention size
	fmt.Println(slice)
    // [1 2 3]
	slice = append(slice, 4, 5) // what happen if run out of space
	fmt.Println(slice)
    // [1 2 3 4 5]
```
Go will copy the array to anohter place if it run out of continues space, we don't need to worry about that under normal circumstances. 

声明一个切片时，可以使用以下方式之一：
```go
	// 声明空的切片
    slice := []int{} 
	// 使用 var 关键字声明一个 nil 切片(一个未分配底层数组的切片,这意味着在使用 nil 切片之前必须将其make初始化)
    var slice []int 
	// 使用 make 函数创建一个长度为 5，容量为 10 的切片. 容量表示底层数组的长度
    slice := make([]int, 5, 10) 
```

# Make and New

1. new return pointer
1. Make return the first(?) element. 

```go
slice := make([]int, 5, 10)
fmt.Println(slice, &slice[0])
// [0 0 0 0 0] 0xc0000b2000
```