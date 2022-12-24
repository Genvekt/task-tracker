# Task Traker system

![](https://img.shields.io/badge/Python-3.11-blue)
![](https://img.shields.io/badge/Poetry-1.2.2-blue)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)


## Architecture overview
System consists of several python microservices, that store
data in PostgreSQL databases and communicate asynchronously through RabbitMQ.
For detailed discribtion look at `services/READ.me`.
![](media/system-diagram.png)

