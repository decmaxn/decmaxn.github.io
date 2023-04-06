# Simple Web Server 1


## Simple web API server to put everything together

main.go
```go
package main

import (
        "net/http"

        "github.com/pluralsight/webservice/controllers"
)

func main() {
        controllers.RegisterControllers()
        http.ListenAndServe(":3000", nil)
}
```
controllers/front.go
```go
package controllers

import "net/http"

func RegisterControllers() {
        uc := newUserController()
        // uc 是一个指向 userController 结构体的指针类型，因此需要使用 *uc 表示 uc 所指向的实际对象。
        // 使用 *uc 就是为了将 uc 指针类型转换为 Handler 接口类型。
        http.Handle("/users", *uc)
        http.Handle("/users/", *uc)
}
```
controllers/user.go
```go
package controllers

import (
        "net/http"
        "regexp"
)

type userController struct {
        userIDPattern *regexp.Regexp
}
// userController 结构体定义了一个 ServeHTTP 方法，该方法的签名与 http.Handler 接口的 ServeHTTP 方法的签名完全一致。
// 这就是在 Go 中实现接口的方式：只要方法的签名与接口定义的方法签名一致，那么该方法就被认为实现了该接口。
func (uc userController) ServeHTTP(w http.ResponseWriter, r *http.Request) {
        // 调用了 http.ResponseWriter 对象的 Write 方法，将字符串 "Hello ...!" 写入到 HTTP 响应中。这个字符串是一个简单的示例
        w.Write([]byte("Hello from the User Controller!"))
        // 实际情况下，我们可以在这里执行任何必要的操作，例如：从 models 包中获取用户信息，并将其以 JSON 格式返回给客户端。
}

// 创建一个新的 userController 实例并返回其指针
func newUserController() *userController {
        return &userController{
                // 使用 regexp.MustCompile 函数创建了一个新的 *regexp.Regexp 对象，并将其存储在 userController 结构体的 userIDPattern 字段中。
                userIDPattern: regexp.MustCompile(`^/users/(\d+)/?`),
                // 在 ServeHTTP 函数中，我们将使用 userIDPattern 字段来解析 URL，从而确定请求中的用户 ID
        }
}
```
models/user.go
```go
package models


type User struct {
        ID        int
        FirstName string
        LastName  string
}

// 全局变量是指在所有函数之外声明的变量，它们的作用域是整个程序。
var (
        //  users 切片是一个全局变量。
        // 存储了所有用户的指针。每个指针都指向一个 User 结构体
        users  []*User
        //users 和 nextID 是在 models/user.go 文件的顶部声明的，因此它们是全局变量。
        nextID = 1
)

func GetUsers() []*User {
        return users
}

//AddUser 函数是向 users 全局变量中添加新用户的函数，其参数为 User 结构体，返回一个 User 结构体和一个 error 类型的值。
func AddUser(u User) (User, error) {
        u.ID = nextID
        nextID++
        //使用 append 函数将一个新的指向 User 结构体的指针添加到 users 中。
        //这样做可以避免复制 User 结构体的开销，并且可以保证在函数外部修改 users 切片的效果。
        users = append(users, &u)
        // 返回一个新的 User 结构体和 nil 值的 error，表示添加用户操作没有出现任何错误。
        return u, nil
}
```
