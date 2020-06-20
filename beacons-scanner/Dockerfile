# The base image to start from
FROM python:3
# Author & Maintainer data
LABEL Author="Agustin Bassi"
LABEL E-mail="jagustinbassi@gmail.com"
LABEL version="1.0.0"
# Create and set the app dir
RUN mkdir -p /app/src
WORKDIR /app/src
# This port will be exposed outside the container
EXPOSE 5000

##### RUN IN DEV MODE (passing source code as volume) #########################

# Copy the requirements to the container
COPY src/requirements.txt ./
# Install all dependencies
RUN pip install -r requirements.txt

##### RUN IN PROD MODE (source code bundled into image) #######################

# # Copy the requirements to the container
# COPY src ./
# # Install all dependencies
# RUN pip install -r requirements.txt
# # Execute this command as default
# CMD ["python", "app.py"]
