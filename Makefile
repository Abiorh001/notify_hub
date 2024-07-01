
IMAGE_NAME = "notify_hub"
install:
	@echo "Installing dependencies..."
	pip install --upgrade pip && pip install -r requirements.txt

format:
	@echo "Formatting code..."
	black .
	isort .

lint:
	@echo "Linting code..."
	pylint --disable=R,C,W1203 src

build:
	@echo "Building the project container..."
	docker build -t $(IMAGE_NAME) .

run-docker:
	@echo "Running the project container..."
	docker run -d -p 8000:8000 $(IMAGE_NAME)

all: install format lint build run-docker