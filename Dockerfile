# pull latest python image
FROM python:3.11.6-slim-bullseye

LABEL Author="Abiola Adeshina" \
      Email="abiolaadeshinaadedayo@gmail.com" \
      Description="Dockerfile for building Notify Hub" \
      Created="2024-07-01"

# install build-essential and pkg-config for installing python packages
RUN apt-get update \
    && apt-get install -y build-essential pkg-config libmariadb-dev

# set working directory
WORKDIR /src

# copy requirements.txt to working directory
COPY ./requirements.txt /src/requirements.txt

# install python packages
RUN pip install --no-cache-dir -r requirements.txt

# copy all files to working directory
COPY . /src

# expose port 8000
EXPOSE 8000

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# run the application
CMD ["fastapi", "dev"]