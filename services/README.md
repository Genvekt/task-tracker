## Microservices 
All microservices of the task-tracker system.

Each service is the poetry project with its onw dependencies. Services are independent and do not import each other. 
The only one dependence - rmq queues, that are created by publishers to 
avoid messages lost.

## Description

Here is the list of all services and words about what they do.

## How to create new service
To create service `service_a`, simply run the following command from this folder:
```shell
poetry new service_a
```