### Setup secret keys for token validation

#### Create keys
From `auth` service directory run the following:
```shell
mkdir auth/data
cd auth/data
openssl genrsa -out jwt-key 4096
openssl rsa -in jwt-key -pubout > jwt-key.pub
```
The commands above will create private key `jwt-key` and public key 
`jwt-key.pub` at `services/auth/auth/data`.

#### Set environment variables for keys: 

- PRIVATE_KEY_PATH: full path to `jwt-key`
- PUBLIC_KEY_PATH: full path to `jwt-key.pub`

