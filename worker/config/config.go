package config

import (
	"encoding/json"
	"fmt"
	"os"
)

type Configuration struct {
	Environment          string
	RabbitmqAMQPUri      string
	RabbitmqQueue        string
	ConsumerTag          string
	ReddisAddress        string
	ThumbnailStoragePath string
	ThumbnailHeight      int
	ThumbnailWidth       int
}

var Conf Configuration

func Config(env string) (*Configuration, error) {
	conf := &Configuration{
		Environment:          "",
		RabbitmqAMQPUri:      "",
		RabbitmqQueue:        "",
		ConsumerTag:          "",
		ReddisAddress:        "",
		ThumbnailStoragePath: "",
		ThumbnailHeight:      100,
		ThumbnailWidth:       100,
	}
	file, err := os.Open(`config/` + env + `.json`)
	if err != nil {
		return nil, fmt.Errorf("Failed to read config file: %s", err)
	}
	decoder := json.NewDecoder(file)
	err = decoder.Decode(&conf)
	if err != nil {
		return nil, fmt.Errorf("Missmatch between config mapping with json config: %s", err)
	}
	return conf, nil
}
