package main

import (
	"encoding/json"
	"fmt"
	"log"
	"time"

	"github.com/streadway/amqp"
)

type QueueMessage struct {
	ImageKey string `json:"image_id"`
}

type Consumer struct {
	conn    *amqp.Connection
	channel *amqp.Channel
	uid     string
	done    chan error
}

func connectToRabbitMQ(uri string) *amqp.Connection {
	for {
		conn, err := amqp.Dial(uri)
		//log.Println(conn)
		if err == nil {
			return conn
		}
		log.Println(err)
		log.Printf("Trying to reconnect to RabbitMQ at %s\n", uri)
		time.Sleep(500 * time.Millisecond)
	}
}

func RabbitMQConsumer(uri, messageQueue string) {
	var rabbitErr *amqp.Error

	for {
		rabbitErr = <-rabbitCloseError
		if rabbitErr != nil {
			log.Printf("Connecting to %s", uri)

			rabbitConn = connectToRabbitMQ(uri)
			rabbitCloseError = make(chan *amqp.Error)
			rabbitConn.NotifyClose(rabbitCloseError)

			channel, err := rabbitConn.Channel()
			if err != nil {
				log.Fatalf("Channel error: %s", err)
			}
			messages, err := channel.Consume(messageQueue, "random-tag", true, false, false, false, nil)
			if err != nil {
				log.Fatalf("Channel consume message error: %s", err)
			}
			go readMessages(messages)

		}
	}
}

func readMessages(messages <-chan amqp.Delivery) {
	for d := range messages {
		queueMessage := &QueueMessage{}

		err := json.Unmarshal(d.Body, queueMessage)
		if err != nil {
			log.Printf("Error decoding JSON: %s", err)
			continue
		}
		log.Printf("Received image with key: %s", queueMessage.ImageKey)

		imageData := GetRedisHash(queueMessage.ImageKey)

		if imageData != nil {
			thumbnailHeight := uint(globalConfig.ThumbnailHeight)
			thumbnailWidth := uint(globalConfig.ThumbnailWidth)

			format := imageData["image_ext"]
			srcImagePath := imageData["image_path"]
			destImagePath := globalConfig.ThumbnailStoragePath + queueMessage.ImageKey + "_" + fmt.Sprint(thumbnailHeight) + "x" + fmt.Sprint(thumbnailWidth) + "." + format

			err := Resizer(srcImagePath, destImagePath, thumbnailHeight, thumbnailWidth)

			resizeStatus := "FAILED"

			if err == nil {
				resizeStatus = "COMPLETED"
				setThumbmailPath := SetRedisHashField(queueMessage.ImageKey, "thumbnail_path", destImagePath)
				if !setThumbmailPath {
					log.Printf("Redis connection error while setting thumbnail path")
				}
			}
			updateThumbnailStatus := SetRedisHashField(queueMessage.ImageKey, "thumbnail_status", resizeStatus)
			if !updateThumbnailStatus {
				log.Printf("Redis connection error while setting thumbnail processing status")
			}
		}
	}
	log.Printf("handle: messages channel closed")
}
