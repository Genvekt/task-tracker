## API Gateway
It routes requests from frontend to backend, uniting endpoints of microservices 
into one. Additionally, it handles user authorisation for each request.

### How to run
From current directory run next command:
```shell
docker run -p 5555:8080 -v $PWD:/etc/krakend/ devopsfaith/krakend run --config /etc/krakend/krakend.json
```