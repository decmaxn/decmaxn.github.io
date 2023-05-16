# collections


## Map

Map can store any types key and value pairs, there is no order. There is no fixed size, so you can tell it's a pointer.

Key 不能是复杂的，不能比较的type.

### 声明

We have to give map key word to tell it's type, it's not like this before. Follow that is key type in [] and value type.

```go
	m := map[string]int{"foo": 1, "bar": 2} 
	fmt.Println(m)
    // map[bar:2 foo:1]
    fmt.Println(m["foo"])
    // 1
	m["foo"] = 11   // modify
	fmt.Println(m["foo"])
    // 11
	delete(m, "foo")   // delete a key value pair
	fmt.Println(m)
    // map[bar:2]
	fmt.Println(m["foo"])
    // 0 Access a non-exist key will return 0, so check your return
```

下面声明会报错panic: assignment to entry in nil map， 意为向 nil map 中赋值，这是不允许的操作。
```go
// 变量 m 被声明为一个 map 类型，但一个 nil 的 map 并没有被分配任何的内存
	var m map[string]int
	m["foo"] = 42
```
在 Go 中，一个 nil 的 map 并没有被分配任何的内存，因此不能直接进行操作，否则会导致运行时 panic。

为了解决这个问题，你需要先使用 make 函数来分配内存:
```go
	m := make(map[string]int)
	m["foo"] = 42
```

### 取值
```go
	// map[key] 实际上返回 两个值， 第二个boolean表示是否存在。
	value, exists := m["bar"] 
	println(value, exists)
	// 2 true
	println(m["bar"]) //缺省是返回value
	// 2 
	
	//题外话，回顾一下为什么没有使用:=， 而是=
	value, exists = m["noexist"]   
	println(value) //如果不存在value 是 0
	// 0  
	println(value, exists)  // 验证确实不存在
	// 0 false

	// 所以实际使用中都是先检查是否存在，再使用返回值
	if exists {   
		println(value)
	}

	//实际使用中还有一种方法是range遍历所有key, value
	for k, v := range m {  
		println(k, v)
	}
```
## Struct

Similar to python's dictionary. 

This is the only data type allow to associate disparate types together. Map's keys have to be same type, and values have to be the same type, although can be different with keys.

```go
	type user struct { //define a struct type named as user
		ID        int //define the fields it's going to contain
		FirstName,LastName string //题外话，回顾一下：可以不分两行
	}
	var u user // 声明user类型的变量u.
	fmt.Println(u)
    // {0  } u exit with 一个0 和两个 空格（blank string）
    // Zero value of int is 0, string is a blank string !!!
    u.ID = 11
	u.FirstName = "Elon"
	fmt.Println(u, u.FirstName)
    // {11 Elon } Elon

	// 另一种方法声明user类型的变量u2，同时付值
    u2 := user{ID: 22, FirstName: "Elon2", LastName: "Musk"} 
	fmt.Println(u2)
    // {22 Elon2 Musk}
```
Note, when doing this in multiple lines, Go's automatic semicolon insertion is going to make problem.  You'd better add a comma after the last item.
```go
	u2 := user{
		ID:        22,
		FirstName: "Elon2",
		LastName:  "Musk", // last item
	}
	fmt.Println(u2)
```
