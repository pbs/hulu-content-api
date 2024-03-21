# set python base image
FROM python:3.12.1-slim

# set working directory within docker image
WORKDIR /app

# copy the entirety of the current directory into the docker /app dir
COPY . /app

# install packackes in requirements
RUN pip --no-cache-dir install -r requirements.txt

# # expose port 
# EXPOSE 5000

# run the app
CMD [ "python3", "app.py" ]
