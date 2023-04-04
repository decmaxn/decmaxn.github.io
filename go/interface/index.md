# Interface


## An examle of Interface

接口（interface）在 Go 语言中是一种类型, 它定义了一组方法的集合.
如果某个类型实现了接口中定义的所有方法，那么该类型就可以被认为是实现了该接口。
实际上就是方法的抽象

```go

//定义一个名为 Shape 的接口类型，它包含了一个计算面积的方法 Area
type Shape interface {
    Area() float64
    // 接口是一组方法的签名（signature）集合
    // Method2(args) returnType
    // Method3(args) returnType
}

//定义两个具体struct类型 Rectangle 和 Circle，
type Rectangle struct {
    width, height float64
}
type Circle struct {
    radius float64
}

// 它们都实现了 Shape 接口中的 Area(此例中是全部)方法，用于计算矩形和圆形的面积
func (r Rectangle) Area() float64 {
    return r.width * r.height
}
func (c Circle) Area() float64 {
    return math.Pi * c.radius * c.radius
}

// 在 main 函数中
func main() {
    // 我们首先创建一个矩形 Rectangle 和一个圆形 Circle 的实例
    r := Rectangle{3, 4}
    c := Circle{5}

    //将这两个实例存储在一个 Shape 类型的切片 shapes 中
    shapes := []Shape{r, c}
    // 虽然r是Rectangle 类型，c是Circle类型，且切片的元素必须是同一种类型
    // 但是上述例子中的 shapes 切片的元素类型是 Shape，
    // 而 Rectangle 和 Circle 类型都实现了 Shape 接口中的 Area 方法，
    // 因此它们都实现了 Shape 接口, 可以放在一个Shape类型的切片里。

    // 循环遍历 shapes 切片中的每个元素，并调用它们的 Area 方法来计算它们的面积
    for _, shape := range shapes {
        // _ 丢掉index
        fmt.Println(shape.Area())
    }
}

```

1. Struct 除了实现 interface定义的接口外，还可以有其他方法。
1. 所以，一个Struct可实现多个接口
1. 接口不接受属性定义, 因为它是一种行为描述，而不是属性描述
1. 接口可以嵌套以他接口. 此例中任何实现了 Mammal 接口的类型都必须同时实现 Animal 接口中的 Speak() 方法。
    ```go
    type Animal interface {
        Speak() string
    }

    type Mammal interface {
        Animal  // Mammal 接口嵌套了 Animal 接口
        Eat() string
    }
    ```

