# Array_slice


# Array
It's similar with Python's array. In Go, array is also a continues memoery block in fixed size, so it's faster but not dynamic. 

It also stores same type objects. What different is Go array is not a pointer. 

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

Slice from an array, or another slice

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
	slice := []int{1, 2, 3} // note you didn't mention size
	fmt.Println(slice)
    // [1 2 3]
	slice = append(slice, 4, 5) // what happen if run out of space
	fmt.Println(slice)
    // [1 2 3 4 5]
```
Go will copy the array to anohter place if it run out of continues space, we don't need to worry about that under normal circumstances. 
