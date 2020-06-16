# Genetic Algorithm Applied to UAV's Path Planning

Reorganizing and adding reproducible features to this project was part of the final project of the course "IA369 - Reproducibility in Computational Research", School of Electrical Engineering, UNICAMP.

## Repository Organization

This repository is organized as follows:

- `data` contains all the data used in this work, it is mostly maps and configurations
- `design` contains auxiliary files to understand the design of the proposed system
- `experiments` contains the result files of the experiments
- `reports` contains textual files that further explain this work [The paper is here!]
- `src` contains all the source files
- `test` contains testing files to assure everything is working

## Dependencies

For the code to work, you need to have the following:

- The platform [Docker](https://docs.docker.com/get-docker/) installed;
- The image `path-planning-hga`; (check how to build it [here](#building-the-image))

## Executing the Paper

### Using Makefile (recommended)

This is the easiest way of executing the paper. This Makefile was prepared so you don't need to worry. You do not need to build the image if usign this method, this make command will build the image for you. Simply run this command on your bash terminal:

```bash
make open-paper
```

Sometimes it is necessary to run in `sudo` mode.

## Building the Image

You can build the docker image for this work in two manners: (1) using the Makefile target or (2) running the commands yourself.

### Using Makefile (recommended)

This is the easiest way of building the image. This Makefile was prepared so you don't need to worry. Simply run this command on your bash terminal:

```bash
make build
```

### Docker Build

If you want to, you can compile the code and build the image yourself by running this command on your bash terminal:

```bash
sed \
    -e 's|{NAME}|$IMAGE_NAME|g' \
    -e 's|{VERSION}|$TAG|g' \
    Dockerfile \
    | docker build -t $IMAGE_NAME:$TAG $DIRECTORY_PATH
```

where:

> `IMAGE_NAME`: the name given to the image built. We strongly recommend using `path-planning-hga`.
>
> `TAG`: the tag used to generate the image, and further to run the container. _eg: `latest`_.
>
> `DIRECTORY_PATH`: the directory where the Dockerfile of this repository is at. It needs to be the _absolute_ path. _eg: `/home/path-planning/`_.

Example:

```bash
sed \
    -e 's|{NAME}|path-planning-hga|g' \
    -e 's|{VERSION}|latest|g' \
Dockerfile \
    | docker build -t path-planning-hga:latest /home/path-planning/
```
