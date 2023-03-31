package main

import (
	"fmt"
)

func main() {
	err, result := DuplicateString("bbb")
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(result)
	}
}
// 如果一个函数需要返回一个错误，可以将其定义为返回值的第一个元素，并将其类型指定为 error。
// 这里的 (input string) 是一个string类型的输入值
// 这里的 (error, string) 实际上是两个类型，分别是 error 和 string。放在一起表示返回两个值
func DuplicateString(input string) (error, string) {

	if input == "aaa" {
		return fmt.Errorf("I did nothing wrong"), ""
	}
	return nil, input + input
}
