# Practice Go with S3 buckets


## Practice Go deleting s3 buckets
Create an test env

```bash
go mod init test  # this will create a go.mod file
go get github.com/aws/aws-sdk-go # this will add 2 requirements in go.mod file
```

Here is the main.go file to learn from:
```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
)

// 声明getBucketRegion函数，main 调用来得到某个 s3 bucket的region 
// 接受一个 svc 参数，类型为 *s3.S3，和一个 bucketName 参数，类型为 *string。
func getBucketRegion(svc *s3.S3, bucketName *string) (string, error) {
	//s3.GetBucketLocationInput 是一个结构体类型, 用&对结构体进行取址操作
	input := &s3.GetBucketLocationInput{
		Bucket: bucketName,
	}

	//svc 是一个 *s3.S3 类型的指针，表示 AWS S3 服务的客户端。
	// 使用 := 运算符对返回的结果进行声明和赋值。
	result, err := svc.GetBucketLocation(input)
	if err != nil {
		return "", err
	}

	// 解析存储桶的区域
	region := ""
	// 判断 result.LocationConstraint 是否为 nil。
	if result.LocationConstraint != nil {
		//如果 result.LocationConstraint 是一个空字符串
		if *result.LocationConstraint == "" {
			region = "us-east-1" // 则存储桶在US East
		} else {
			region = *result.LocationConstraint
		}
	}

	return region, nil
}

func main() {
	// 创建一个新的AWS会话
	sess, err := session.NewSession(&aws.Config{
		Region: aws.String("us-west-2"), 
	})
	if err != nil {
		fmt.Println("无法创建AWS会话:", err)
		return
	}

	// 创建S3服务客户端
	svc := s3.New(sess)

	// 读取用户输入的模式
	fmt.Print("请输入要匹配的模式：")
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	pattern := scanner.Text()

	// 列出存储桶
	result, err := svc.ListBuckets(nil)
	if err != nil {
		fmt.Println("无法列出存储桶:", err)
		return
	}

	//创建一个空(最后的0的意义）的切片 matchedBuckets，
	//其元素类型为 *s3.Bucket。
	//make 函数用于创建一个指定类型、指定长度和容量的切片.
	matchedBuckets := make([]*s3.Bucket, 0)
	for _, bucket := range result.Buckets {
		//bucket.Name 是一个指向 *string 类型的指针，
		//通过调用 aws.StringValue 函数可以获取其指向的字符串值。
		bucketName := aws.StringValue(bucket.Name)
		//检查 bucketName 是否包含指定的 pattern 字符串
		if strings.Contains(bucketName, pattern) {
			matchedBuckets = append(matchedBuckets, bucket)
		}
	}

	if len(matchedBuckets) == 0 {
		fmt.Println("没有找到匹配的存储桶")
		return
	}

	// 打印匹配的存储桶列表
	fmt.Println("匹配的存储桶列表:")
	for _, bucket := range matchedBuckets {
		fmt.Println(aws.StringValue(bucket.Name))
	}

	// 确认删除存储桶
	fmt.Print("是否确认删除这些存储桶？(yes/no): ")
	scanner.Scan()
	confirmation := scanner.Text()

	if confirmation == "yes" {
		// 删除存储桶
		for _, bucket := range matchedBuckets {
			bucketRegion, err := getBucketRegion(svc, bucket.Name)
			if err != nil {
				fmt.Printf("无法获取存储桶 %s 的区域: %v\n", aws.StringValue(bucket.Name), err)
				continue
			}

			// TODO: investigate if virginia's bucket is like this
			if bucketRegion == "" {
				fmt.Printf("无法确定存储桶 %s 的区域\n", aws.StringValue(bucket.Name))
				continue
			}

			// 为这个BUCKET创建一个新的AWS会话
			bucketSvc := s3.New(session.Must(session.NewSession(&aws.Config{
				Region: aws.String(bucketRegion),
			})))

			_, err = bucketSvc.DeleteBucket(&s3.DeleteBucketInput{
				Bucket: bucket.Name,
			})
			if err != nil {
				fmt.Printf("无法删除存储桶 %s: %v\n", aws.StringValue(bucket.Name), err)
			} else {
				fmt.Printf("已成功删除存储桶 %s\n", aws.StringValue(bucket.Name))
			}
		}
	} else {
		fmt.Println("已取消删除操作")
	}
}
```
