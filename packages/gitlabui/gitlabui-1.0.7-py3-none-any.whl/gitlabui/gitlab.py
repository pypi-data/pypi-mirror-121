import json
import os
import re
import sys
import urllib.parse

from requests_cache import CachedSession


class GitlabApi:
    def __init__(self, url, token, logger=None, cache_expire_after=60):
        self.url = url
        self.token = token
        self.logger = logger
        self.db = './projects.json'
        self.session = CachedSession(backend='memory', expire_after=cache_expire_after)

    def request(self, method, path, **kwargs):
        return self.session.request(method, self.url + path, headers={'PRIVATE-TOKEN': self.token}, **kwargs)

    def get(self, path, **kwargs):
        return self.request('get', path, **kwargs)

    def post(self, path, **kwargs):
        return self.request('post', path, **kwargs)

    def put(self, path, **kwargs):
        return self.request('put', path, **kwargs)

    def patch(self, path, **kwargs):
        return self.request('patch', path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request('delete', path, **kwargs)

    def get_project(self, id_or_name):
        return self.get('/projects/' + urllib.parse.quote_plus(id_or_name)).json()

    def get_projects(self, search=None, opts=None):

        if os.path.exists(self.db):
            self.logger.info('load from file')
            with open(self.db, 'r') as f:
                projects = json.load(f)['projects']
        else:
            self.logger.info('load from api')
            page = 1
            projects = []

            res = self.get('/projects?per_page=100&page=' + str(page)).json()

            while len(res) > 0:
                projects += res
                page += 1
                res = self.get('/projects?per_page=100&page=' + str(page)).json()

            projects = sorted(projects, key=lambda p: p['path_with_namespace'])

            self.save(projects)

        if search:
            projects = [p for p in projects if re.search(search, p['path_with_namespace'], flags=re.IGNORECASE)]

        if opts and 'kind' in opts:
            projects = [p for p in projects if p['namespace']['kind'] == opts['kind']]

        if opts and 'archived' in opts:
            projects = [p for p in projects if p['archived'] == (opts['archived'].lower() == 'true')]

        if opts and 'sortby' in opts:
            sortby = opts['sortby']
            is_desc = opts['sortbydirection'] == 'desc' if 'sortbydirection' in opts else False
            default_value = '' if is_desc else chr(sys.maxunicode)
            projects = sorted(projects,
                              key=lambda p: p[sortby] if sortby in p else default_value,
                              reverse=is_desc)

        return projects

    def refresh_tags(self, delta=None):
        previous = self.get_refresh_tags_time()
        if previous is not None and delta is not None:
            from datetime import datetime, timedelta
            if type(delta) == str:
                delta = int(delta)
            if type(delta) == int:
                delta = timedelta(seconds=delta)
            current_delta = datetime.now() - datetime.fromisoformat(previous)
            if current_delta < delta:
                self.logger.info('skip refresh tags, current_delta = ' + str(current_delta))
                return None
        projects = [self.get_latest_tag(p) for p in self.get_projects()]
        from datetime import datetime
        self.save(projects, datetime.now().isoformat(timespec='seconds'))

    def get_refresh_tags_time(self):
        if os.path.exists(self.db):
            with open(self.db, 'r') as f:
                return json.load(f)['refresh_tags_time']
        else:
            return None

    def reset(self):
        self.session.cache.clear()
        try:
            os.remove(self.db)
        except FileNotFoundError:
            self.logger.debug('nothing to reset')

    def save(self, projects, refresh_tags_time=None):
        with open(self.db, 'w') as f:
            json.dump({'refresh_tags_time': refresh_tags_time, 'projects': projects}, f)

    def get_latest_tag(self, p):
        res = self.get('/projects/' + str(p['id']) + '/repository/tags?order_by=name&search=^v').json()
        if type(res) == dict:
            return p
        if len(res) == 0:
            res = self.get('/projects/' + str(p['id']) + '/repository/tags?order_by=name').json()
        if len(res) > 0:
            p['tag'] = res[0]['name']
            p['tag_created_at'] = res[0]['commit']['created_at'][0:10]
        return p

    def get_repository_file_content(self, p, filepath, ref):
        import base64
        url = '/projects/' + str(p['id']) + '/repository/files/' + urllib.parse.quote_plus(filepath) + '?ref=' + ref
        file = self.get(url).json()
        if 'content' in file:
            return base64.b64decode(file['content']).decode('utf8')
        else:
            return None

    def search(self, search, filepath, ref, project_search=None, project_opts=None):
        res = []
        for p in self.get_projects(project_search, project_opts):
            content = self.get_repository_file_content(p, filepath, ref)
            if content and re.search(search, content, flags=re.IGNORECASE):
                p['match'] = [line
                              for line in content.splitlines()
                              if re.search(search, line, flags=re.IGNORECASE)]
                res.append(p)
        return res

    def version(self):
        import pkg_resources

        try:
            version = pkg_resources.get_distribution('gitlabui').version
        except pkg_resources.DistributionNotFound as e:
            version = '0.0.0'
            self.logger.error(e)

        try:
            gitlab = self.get('/version', timeout=5).json()
        except Exception as e:
            gitlab = {'error': str(e)}

        return {'version': version, 'gitlab': gitlab}
