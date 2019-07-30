package main

import (
	"log"
	"os"
	"time"
	"worker/config"

	"github.com/go-redis/redis"
	"github.com/streadway/amqp"
)

var (
	globalConfig     *config.Configuration
	redisClient      *redis.Client
	rabbitConn       *amqp.Connection
	rabbitCloseError chan *amqp.Error
)

func init() {
	var err error
	globalConfig, err = config.Config(os.Getenv("env"))
	if err != nil {
		log.Fatalf("%s", err)
	}
	redisClient = redis.NewClient(&redis.Options{
		Addr:         globalConfig.ReddisAddress,
		DB:           0,
		DialTimeout:  10 * time.Second,
		ReadTimeout:  30 * time.Second,
		WriteTimeout: 30 * time.Second,
		PoolSize:     10,
		PoolTimeout:  30 * time.Second,
	})
}
func main() {
	// create the rabbitmq error channel
	rabbitCloseError = make(chan *amqp.Error)

	// run the callback in a separate thread
	go RabbitMQConsumer(globalConfig.RabbitmqAMQPUri, globalConfig.RabbitmqQueue)

	// an error and thus calling the error callback
	rabbitCloseError <- amqp.ErrClosed
	select {}
	log.Printf("Worker has been started")
}
