from flask import render_template, request, redirect, url_for

from gitlabui import app, api


@app.route('/')
def index():
    return redirect(url_for('tags'))


@app.route('/tags')
def tags():
    projects = api.get_projects(request.args.get('q'), opts=request.args)
    refresh_tags_time = api.get_refresh_tags_time()
    if request.args.get('format') == 'json':
        return {'refresh_tags_time': refresh_tags_time, 'results': projects}
    else:
        return render_template('index.html', projects=projects, refresh_tags_time=refresh_tags_time)


@app.route('/reset')
def reset():
    api.reset()
    return redirect(url_for('tags'))


@app.route('/refresh_tags')
def refresh_tags():
    api.refresh_tags(request.args.get('delta'))
    return redirect(url_for('tags'))


@app.route('/search')
def search():
    if 'search' in request.args and 'filepath' in request.args and 'ref' in request.args:
        results = api.search(
            request.args['search'],
            request.args['filepath'],
            request.args['ref'],
            project_search=request.args.get('q'),
            project_opts=request.args
        )
        if request.args.get('format') == 'json':
            return {'results': results}
        else:
            return render_template('search.html', results=results)
    else:
        return render_template('search.html')


@app.route('/version')
def version():
    return api.version()
