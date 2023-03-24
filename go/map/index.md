# Map


# Map

Map can store any types key and value pairs, there is no order. There is no fixed size, so you can tell it's a pointer.

Key 不能是复杂的，不能比较的type.

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

# Struct

Similar to python's dictionary. 

This is the only data type allow to associate disparate types together. Map's keys have to be same type, and values have to be the same type, although can be different with keys.

```go
	type user struct { // define a struct type named as user
		ID        int // define the fields it's going to contain
		FirstName string
		LastName  string
	}
	var u user // 
	fmt.Println(u)
    // {0  } u exit with zero values. 
    // Zero value of int is 0, string is a blank string
    u.ID = 11
	u.FirstName = "Elon"
	fmt.Println(u, u.FirstName)
    // {11 Elon } Elon
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
