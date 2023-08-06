# gitlabui

[![Docker Pulls](https://img.shields.io/docker/pulls/batou9150/gitlabui.svg)](https://hub.docker.com/r/batou9150/gitlabui/)
[![Docker Stars](https://img.shields.io/docker/stars/batou9150/gitlabui.svg)](https://hub.docker.com/r/batou9150/gitlabui/)
[![pypi version](https://img.shields.io/pypi/v/gitlabui.svg)](https://pypi.org/project/gitlabui/)

Flask App over Gitlab Api to browse projects tags and to search into repository files

## Installation
```shell
pip install gitlabui
```

## Run Flask App

### Run with gunicorn
```shell
export GITLAB_URL=http://localhost/api/v4
export GITLAB_TOKEN=<YOUR_PRIVATE_TOKEN>
gunicorn -b 0.0.0.0:5000 gitlabui:app
```

### Run with docker
```shell
docker run -d \
  -e GITLAB_URL=http://localhost/api/v4 \
  -e GITLAB_TOKEN=<YOUR_PRIVATE_TOKEN> \
  -p 5000:5000 batou9150/gitlabui gunicorn -b 0.0.0.0:5000 gitlabui:app
```
