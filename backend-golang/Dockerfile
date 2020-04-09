FROM golang:1.13

WORKDIR /go/src/app
COPY . .
RUN go get -d -v ./...
#CMD ["go-wrapper", "run"]
#RUN go install -v ./...


EXPOSE 8000
CMD [ "go", "run", "main.go"]