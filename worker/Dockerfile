FROM patil16nit/golang-imagemagick:1.0

ENV GO111MODULE=on
ENV environment=$ENV 

WORKDIR /go/src/worker
COPY . .

RUN go get -d -v ./...
RUN go install -v ./...

CMD ["worker"]