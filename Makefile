default: docker-build

lorem.py:
	echo you need to create a lorem.py file

docker-build: lorem.py
	docker build -t jlewallen/voight-kampff .

docker-run:
	docker run --rm jlewallen/voight-kampff
