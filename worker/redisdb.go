package main

import (
	"fmt"
)

func GetRedisHash(key string) map[string]string {
	val, err := redisClient.HGetAll(key).Result()
	fmt.Println("get redis image data %v ", val)
	if err != nil {
		fmt.Println("No value found with error ", err)
		return nil
	}
	return val
}

func SetRedisHashField(key, field, val string) bool {
	err := redisClient.HSet(key, field, val).Err()
	if err != nil {
		fmt.Println("Failed to set key with error ", err)
		return false
	}
	return true
}
