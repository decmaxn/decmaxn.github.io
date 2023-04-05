# Reflect


反射机制主要由 reflect 包提供支持。通过反射，我们可以在运行时动态地获取和设置一个变量的值、类型和属性，而不需要在编码时就确定这些信息。

## 使用 reflect 包获取一个变量的类型和值

由于反射机制会带来一些性能上的开销，因此在性能敏感的场景中应该谨慎使用。

```go
package main

import (
    "fmt"
    "reflect"
)

func main() {
    var x float64 = 3.14
    fmt.Println("type:", reflect.TypeOf(x))
    fmt.Println("value:", reflect.ValueOf(x).Float())
}
```
## better to use reflect for Struct 

通过反射获取结构体的类型信息、字段信息和方法信息
```go
package main

import (
    "fmt"
    "reflect"
)

type Person struct {
    Name string
    Age  int
}

func main() {
    p := Person{"John", 30}

    // 获取结构体类型
    t := reflect.TypeOf(p)
    fmt.Println("Type:", t)

    // 遍历结构体字段
    for i := 0; i < t.NumField(); i++ {
        f := t.Field(i) // struct的Field属性仍然是Type 的一部分
        fmt.Printf("Field %d: %s %s\n", i+1, f.Name, f.Type)
    }
}
// Type: main.Person
// Field 1: Name string
// Field 2: Age int
```

## 反射机制还可以用于动态修改结构体的值

```to
package main

import (
    "fmt"
    "reflect"
)

type Person struct {
    Name string
    Age  int
}

func main() {
    p := Person{"John", 30}

    //调用 Elem 方法获取指向结构体变量的指针
    v := reflect.ValueOf(&p).Elem() 
    // 通过 FieldByName 方法获取结构体的 Name 和 Age 字段
    v.FieldByName("Name").SetString("Tom")
    //分别调用 SetString 和 SetInt 方法修改字段的值
    v.FieldByName("Age").SetInt(35)

    fmt.Println(p) // 输出: {Tom 35}
}
```

