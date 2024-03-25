# Hulu Content Portal API

## Prerequisites 
- Docker

## Getting Started

### Configuration 

To run this project, you will need an `.env` file with the following variables:

```
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

HULU_CONTENT_USERNAME = ""
HULU_CONTENT_PASSWORD = ""

API_USERNAME = ""
API_PASSWORD = ""

JWT_SECRET_KEY = ""
```

### Installation 

Clone the repository 
```
git clone https://github.com/pbs/hulu-content-api.git
```

Navigate to the project directory 
```
cd hulu-content-api
```

### Deploy using Docker
 Build the docker image 
 ```
 docker-compose build 
 ```

 Start a container for the image 
 ```
 docker-compose up 
 ```

 To verify your Docker container is running, use the following command.
 ```
 docker-compose ps 
 ```

 Your API is now up and running on the specified port.
