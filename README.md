# Task Traker system

![](https://img.shields.io/badge/Python-3.11-blue)
![](https://img.shields.io/badge/Poetry-1.2.2-blue)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
![example workflow](https://github.com/Genvekt/task-tracker/actions/workflows/check_pipeline.yaml/badge.svg?branch=main)

## Run
It is possible to run system with Docker Compose from the project root:
1. Images use default host and custom bridge network. To create bridge network, run:
```shell
docker network create -d bridge task-tracker-network
```
2. With created networks, next command will start everything:
```shell
docker-compose up --build
```

## Architecture overview
System consists of several python microservices, that store
data in PostgreSQL databases and communicate asynchronously through RabbitMQ.
For detailed discribtion look at `services/READ.me`.
![](media/system-diagram.png)

The communication between services is asynchronous and goes through RabbitMQ queues.
The following scheme defines the connection of services with exchanges and queues:
![](media/rmq-diagram.png)

## TODO
- [ ] Use user public id in all user endpoints
- [ ] Accounting system logic
- [ ] Dockerize Accounting
- [ ] Notification service
- [ ] Analytics service
- [ ] Env files
## TODO
- [ ] Use user pablic id in all user endpoints
- [ ] Accounting system logic
- [ ] Dockerize Accounting
- [ ] Notification service
- [ ] Analytics service
- [ ] Env files
