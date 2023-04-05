# Defer Panic Recovery


## Defer 在函数返回之前执行

等同于 Java和C# 的 finally

常使用在记的关闭你打开的资源， 比如文件，锁，错误处理等。

如果不用defer, 而是简单的把关闭动作放到逻辑后面，如果执行逻辑时出错退出，关闭就被跳过了。

## Panic 和 Recover

Panic主动使当前线程 crash， Recover函数从panic或错误场景中恢复

## 解释使用方法的 Example

```go
	defer func() {
		fmt.Println("defer func is called") 
		if err := recover(); err != nil {
			fmt.Println(err)
		}
	}()
	panic("a panic is triggered")
// defer func is called
// a panic is triggered
```
## 实际使用的example
如果 doSomething() 里panic, defer 的函数会执行，包括recovery 的部分，因为mainI()里的panic
```go
func main() {
    defer func() {
        // 因为有panic，recover() 会得到非nil
        if r := recover(); r != nil {
            fmt.Println("Recovered from", r)
        }

        fmt.Println("Cleaning up...")
    }()

    fmt.Println("Performing some tasks...")
    // 因为 err != nil, main()里的panic 执行，
    if err := doSomething(); err != nil {
        panic(err)
    }
    // 上面的panic 会跳过下面"All tasks completed successfully." 直接defer
    fmt.Println("All tasks completed successfully.")
}
// 被调用的函数panic产生的crush会跳过return nil. 回到main()
func doSomething() error {
    fmt.Println("Doing something...")

    // 模拟一个异常
    panic("Something went wrong!")

    return nil
}
// Performing some tasks...
// Doing something...
// Recovered from Something went wrong!
// Cleaning up...
```
如果 doSomething() 里不会panic,defer依然会执行。但是"Recovered from"会被跳过
```go
// Performing some tasks...
// Doing something...
// All tasks completed successfully.
// Cleaning up...
```
