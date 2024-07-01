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