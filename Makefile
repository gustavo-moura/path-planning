DIRECTORY_PATH=$(shell pwd)


IMAGE_NAME=path-planning
TAG=$(shell git describe --tags --always --dirty)

CONTAINER_NAME_JUPYTER=path-planning-jupyter


# Build docker image
build:
	@echo "\nBuilding Production image with labels:\n"
	@echo "    name: ${IMAGE_NAME}"
	@echo "    version: $(TAG)"
	@sed \
		-e 's|{NAME}|$(IMAGE_NAME)|g' \
		-e 's|{VERSION}|$(TAG)|g' \
		Dockerfile \
	| docker build -t $(IMAGE_NAME):$(TAG) $(DIRECTORY_PATH)


# Run docker image starting the jupyter notebook
open-paper:
	docker run \
		-it --rm -a stdout \
		-u `id -u`:`id -g` \
		-v /etc/passwd:/etc/passwd \
		--name=$(CONTAINER_NAME_JUPYTER) \
		-p 8888:8888 \
		--entrypoint=/bin/bash \
		$(IMAGE_NAME):$(TAG) \
		-c "jupyter notebook \"./reports/Paper - Genetic Algorithm Applied in UAV's Path Planning.ipynb\" --ip 0.0.0.0 --allow-root"


docker-rm:
	docker rm $(CONTAINER_NAME_JUPYTER)