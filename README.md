# Thumbanail Generator Service
## Overview
Simple thumbnail generator service haing below features:
- Upload image (specially PNG)
- Provides the thumbnail for uploaded file 

It provides the rest api for uploading images and fetching the associative thumbnails based on python, golang, redis and rabbitmq.
Service has 4 main components:
- api
- queue (rabbitmq)
- redis as main data store
- worker (thumbnail generator) 

with the help of rest api, user can upload the file using api which then stores the image related data into redis and sends the thumbnail generator task to rabbitmq based queue `ImageConverter` and our worker which has subscribed to the queue, listens to the messages and proceeds with the thumbnail generator.

## Project Structure
```
Thumbnail
├── README.md
├── api
│   ├── Dockerfile
│   ├── Dockerfile.test
│   ├── gazo
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── commands.py
│   │   ├── exceptions.py
│   │   ├── extensions.py
│   │   ├── image
│   │   │   ├── __init__.py
│   │   │   └── index.py
│   │   ├── settings.py
│   │   └── utils.py
│   ├── requirements
│   │   ├── dev.txt
│   │   └── prod.txt
│   ├── requirements.txt
│   ├── run.py
│   └── tests
│       ├── __init__.py
│       ├── __pycache__
│       ├── conftest.py
│       ├── test_get_thumbmail.py
│       ├── test_image_upload.py
│       └── test_utils.py
├── docker-compose.dev.yml
├── docker-compose.test.yml
├── docker-compose.yml
├── rabbitmq
│   ├── Dockerfile
│   ├── definitions.json
│   └── rabbitmq.config
├── run-tests.sh
├── sampledata
│   ├── cologne.png
│   ├── tokyo.jpg
│   ├── tokyo.png
│   ├── wrong.png
│   └── zero_byte.png
└── worker
    ├── Dockerfile
    ├── config
    │   ├── config.go
    │   ├── dev.json
    │   ├── prod.json
    │   └── test.json
    ├── consumer.go
    ├── go.mod
    ├── go.sum
    ├── main.go
    ├── redisdb.go
    └── resizer.go
```


## API Documentation:

#### `POST`  /image
File uploader endpoint specific to `png` format
##### parameters 
- file (required): type(Content-Type: image/png)>
  validation cases:
    - PNG with size > 0B or size < 10MB

##### Response codes and description:

###### success cases 
```sh
{
    "request_id" : "XXXXXXXXX"
}
```
###### error cases
```sh
{
    "message" : "XXXXXXXXX"
}
```

Here are the response codes and messages descriptions 
| Request |Response_Code | Response_Keys | Sample response |
| ------ | ------ | ------ | ------ |
| Valid png |200 | request_id: type(string:uuid) | {“request_id” : “990663a4-1bd8-4cde-ace6-8592c3baaf52”} | 
| Upload file other than PNG format or PNG with zero size |400 | message: type(string) | {“message” : “Bad request”} | 
| Exceptions like Connection errors with redis or rabbitmq|503 | message: type(string) | {“message” : “Internal Server Error, Try again later”} | 

#### `GET` /image/${request_id}/thumbnail
Thumbnail endpoint providing status of thumbnail generation and thumnnail  
##### parameters 
- request_id (required): type(string)

##### Response codes and description:

###### **success cases** 
- thumbnail generation successful
    ```sh
    {
       "request_id": "ba009385-27d2-4e6e-9005-64c45066a23f",
       "thumbnail_status": "COMPLETED",
       "result": {
          "thumbnail_100x100": "http://localhost:5000/image/ba009385-27d2-4e6e-9005-64c45066a23f_100x100.png",
          "original_image": "http://localhost:5000/image/ba009385-27d2-4e6e-9005-64c45066a23f.png"
       }
    }
    ```

-  thumbnail generation processing 
    request has been submitted to service but still thumbnail generation is not yes finished by worker process
    ```sh
   {
        "request_id": "4a6f11ec-855b-4671-9b69-70ab57685bc9",
        "thumbnail_status": "PROCESSING",
    }
    ```
  
-  thumbnail generation failed 
   request has been submitted to service but thumbnail generation is failed by worker process
    ```sh
   {
        "request_id": "97d715cc-16e3-420a-af63-6c0a30c12f44",
        "thumbnail_status": "FAILED",
    }
    ```
###### **error cases**
- 404 
    ```sh
    {
        "message" : "No such request registered in system"
    }
    ```
- 503
   ```sh
   {
       "message" : "Internal Server Error, Try again later"
   }
   ```
  
##### Response codes and description:
 Here are the response codes and messages 
| Request |Response_Code | Response_Keys | Sample response |
| ------ | ------ | ------ | ------ |
| Valid request_id(from POST /image response) |200 | request_id: type(string:uuid) (always), thumbnail_status: string:(COMPLETED,PROCESSING,FAILED) (always), result:type(json) (on successful image generation) | {“request_id” : “990663a4-1bd8-4cde-ace6-8592c3baaf52”} | 
| Upload file other than PNG format or PNG with zero size |400 | message: type(string) | {“message” : “No such request registered in system”} | 
| Exceptions like Connection errors with redis or rabbitmq|503 | message: type(string) | {“message” : “Internal Server Error, Try again later”} | 

#### `GET` /image/${request_id}
Provide Thumbnail image 
##### parameters 
- request_id (required): type(string)

##### Response codes and description:

###### **success cases** 
- 200 or 304 (cached) thumbnail image

###### **error cases**
- 404 
    ```sh
    {
        "message" : "File not found"
    }
    ```
- 503 service error
  
##### Response codes and description:
 Here are the response codes and messages 
| Request |Response_Code | Response_Keys | Sample response |
| ------ | ------ | ------ | ------ |
| Valid request_id(from POST /image response) |200 | N/A | image bytes | 
| Invalid request_id | 404 | message: type(string) | {“message” : “File not found”} | 

## Execution (User Acceptance testing)
### System requirement
Development and testing is done on below docker environment
| Utility | Desctiption |
| ------ | ------ |
| Docker (mac/linux) | latest version(Docker version 18.09.0, build 4d60db4) |
| Docker compose (mac/linux) | latest version (docker-compose version 1.23.2, build 1110ad01) |

feel free to upgrade your personal computer to work service properly.

`Note`: make sure your don't have any service running on your local machine with ports  5000,5672,15672,6379 otherwise kill that process for time being

```sh
cd Thumbnail
docker-compose up
# wait for all containers to build and start as this is first time exection
```

### SUCCESS CASE
- Thumbnail generation successful
    ```sh
    # already some sample data for png,jpg, 0B png are added into sampledata 
    # Open New terminal
    curl -F 'file=@./sampledata/tokyo.png' 127.0.0.1:5000/image
    export reqId=${request_id}
    curl "http://127.0.0.1:5000/image/$reqId/thumbnail"
    ```
- Thumbnailgeneration inprogress
   ```sh
    # already some sample data for png,jpg, 0B png are added into sampledata 
    # Open New terminal and go to our project directory `Thumbnail`
    docker-compose stop worker
    curl -F 'file=@./sampledata/cologne.png' 127.0.0.1:5000/image
    export reqId=${request_id}
    curl "http://127.0.0.1:5000/image/$reqId/thumbnail" # this one will have "PROCESSING" thumbnail_status
    docker-compose start worker
    curl "http://127.0.0.1:5000/image/$reqId/thumbnail" # this one will have "COMPLETED" thumbnail_status
    ```
    
- Thumbnailgeneration failed
   ```sh
    # already some sample data for png,jpg, 0B png are added into sampledata 
    # Open New terminal and go to our project directory `Thumbnail` or you can change any files extension to png and make request 
    curl -F 'file=@./sampledata/wrong.png' 127.0.0.1:5000/image
    export reqId=${request_id}
    curl "http://127.0.0.1:5000/image/$reqId/thumbnail" #this one will have "PROCESSING" thumbnail_status
    ```
### ERROR CASE
- Bad request_id
   ```sh
    curl "http://127.0.0.1:5000/image/45794930453080-fhdjsf-y54i/thumbnail"
    ```
- Internal server error
   ```sh
    # already some sample data for png,jpg, 0B png are added into sampledata 
    # Open New terminal and go to our project directory `Thumbnail`
    curl -F 'file=@./sampledata/cologne.png' 127.0.0.1:5000/image
    export reqId=${request_id}
    docker-compose stop redis
    curl "http://127.0.0.1:5000/image/$reqId/thumbnail" # this gives internal server error
    docker-compose start redis
    ```

Remove your container once testing is done executing below command from `Thumbnail` directory
```sh
docker-compose down
```

### Unit/Intergration testing:
Execute test cases using `Thumbnail/run-tests.sh` script
`Nore`: Make sure your previous docker-compose up should be terminated and executed docker-compose down then execute below commands
```sh
cd Thumbnail
chmod +x run-tests.sh
./run-tests.sh
```