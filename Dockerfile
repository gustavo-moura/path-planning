FROM python:3.8-rc-buster

LABEL name={NAME}
LABEL version={VERSION}


# Install requirements
COPY src/requirements.txt src/requirements.txt
RUN pip install -r src/requirements.txt


WORKDIR /opt/path-planning/


COPY . .


EXPOSE 8000
