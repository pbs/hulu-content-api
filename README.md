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

 ## Making Requests

### `GET /`

Submit a GET request to this base endpoint to verify the API is up and running

```
curl http://localhost:8080/
```

### `POST /authenticate`

Submit a POST request to the authenticate endpoint to retrieve a signed API token. 

### `POST /content_portal`

Submit a POST request to the content portal endpoint to generate a Hulu Content report. 

The following headers are required for this protected endpoint:
```
{
    "Content-Type": "application/json,
    "Authorization": f"Bearer {your_api_token}
}
```

Sample API request 

```
# retrieve an API token 
response = requests.post(
    url = "http://localhost:8080/authenticate
    json = {
        username = "YOUR_API_USERNAME",
        password = "YOUR_API_PASSWORD"
    }
)

api_token = response.json()["payload"]

# set report parameters
report_params = {
    "metric": METRIC,
    "content_partner": CONTENT_PARTNER,
    "series_movie": SERIES_MOVIE,
    "season": SEASON,
    "package": PACKAGE,
    "playback_type": PLAYBACK_TYPE,
    "time_increment": TIME_INCREMENT,
    "start_date": START_DATE,
    "end_date": END_DATE
}

# set headers 
headers = {
    "Content-Type": "application/json,
    "Authorization": f"Bearer {your_api_token}
}

# make request 
response = requests.post(
    url="https://localhost:8080/content_portal,
    headers=headers,
    json=report_params
)
```