# Auth service
Custom auth service that registers new users and generates access JWT tokens for authenticated users.
JWTs are encoded and decoded using asymmetric encryption (RSA Private and Public key pair). 
Only public key is available for outside world, which protects system from being compromised. 

## Authentication and Authorization flows
The following diagram illustrates the flow of user authentication and authorization
in the system.

![](../../media/auth-flow.png)

## Run service

### Setup
Environment variables (`auth/settings.py`):
- `DATABASE_URL`: PostgreSQL URI in form of "postgresql://`user`:`password`@`host`:`port`/`database`".
- `RABBITMQ_URL`: RabbitMQ URI in form of "amqp://`user`:`password`@`host`:`port`".
- `USER_EVENTS_EXCHANGE`: The name of RabbitMQ exchange to publish events to.
- `PRIVATE_KEY_PATH`: Absolute path to RSA private key
- `PUBLIC_KEY_PATH`: Absolute path to RSA public key
- `ACCESS_TOKEN_EXPIRES`: TTL of token in seconds.


### Manually setup secret keys for token validation
Dockerfile already designed to generate keys automatically, however for local run the keys may be created as follows:
#### Create keys
From `services/auth` directory run the following:
```shell
mkdir auth/data
cd auth/data
openssl genrsa -out jwt-key 4096
openssl rsa -in jwt-key -pubout > jwt-key.pub
```
The commands above will create private key `jwt-key` and public key 
`jwt-key.pub` at `services/auth/auth/data`.

#### Set environment variables for keys: 

- PRIVATE_KEY_PATH: absolute path to `jwt-key`
- PUBLIC_KEY_PATH: absolute path to `jwt-key.pub`

