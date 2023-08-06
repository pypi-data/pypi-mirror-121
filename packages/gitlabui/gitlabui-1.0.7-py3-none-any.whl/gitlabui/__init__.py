import os
import logging
from flask import Flask
from gitlabui.gitlab import GitlabApi

app = Flask(__name__)
app.config.update({
    'GITLAB_URL': os.environ.get('GITLAB_URL', 'http://localhost/api/v4'),
    'GITLAB_TOKEN': os.environ.get('GITLAB_TOKEN')
})

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

api = GitlabApi(
    url=app.config.get('GITLAB_URL'),
    token=app.config.get('GITLAB_TOKEN'),
    logger=app.logger
)

if 1 == 1:
    from gitlabui import views
