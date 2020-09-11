from flask import Flask, render_template, request, Response, redirect
import json
from classes.Updater import Updater
from classes.DI import DI
from classes.Config import Config

app = Flask(__name__)

# pip install requests
# pip install json-rpc

@app.route('/bootstrap.css')
def bootstrap_css():
    f = open('css/bootstrap.min.css', "r")
    content = f.read()
    f.close()
    return Response(content, mimetype='text/css')

@app.route('/jquery.js')
def jquery_js():
    f = open('js/jquery-3.5.1.min.js', "r")
    content = f.read()
    f.close()
    return Response(content, mimetype='text/js')

@app.route('/bootstrap.js')
def bootstrap_js():
    f = open('js/bootstrap.bundle.min.js', "r")
    content = f.read()
    f.close()
    return Response(content, mimetype='text/js')


@app.route('/')
def hello_world():
    blk = DI.get_blockchain()
    try:
        data = blk.get_info()
        return render_template('main.html', data=data['result'])
    except Exception:
        return redirect('/config')


@app.route('/my')
def show_my():
    blk = DI.get_blockchain()
    if not blk.check():
        return render_template('error_rpc.html', nav='my')

    records = blk.get_my()
    my_records = []

    for record in records:
        record['decoded'] = json.loads(record['value'])
        record['expires_in'] = round(record['expires_in']/175)

    for record in records:
        if 'network' in record['decoded'] and 'type' in record['decoded'] and 'lang' in record['decoded'] and 'tags' in record['decoded']:
            my_records.append(record)

    return render_template('my.html', records=my_records, nav='my')


@app.route('/my_descriptions')
def show_my_descriptions():
    blk = DI.get_blockchain()
    if not blk.check():
        return render_template('error_rpc.html', nav='my_descriptions')

    records = blk.get_my()
    my_records = []

    for record in records:
        record['decoded'] = json.loads(record['value'])
        record['expires_in'] = round(record['expires_in']/175)

    for record in records:
        if 'network' not in record['decoded'] and 'type' not in record['decoded'] and 'lang' not in record['decoded'] and 'tags' not in record['decoded']:
            my_records.append(record)

    return render_template('my_descriptions.html', records=my_records, nav='my_descriptions')


@app.route('/submit', methods=['GET'])
def show_submit():
    return render_template('submit.html', nav='submit')


@app.route('/submit', methods=['POST'])
def submit():
    if 'days' not in request.form:
        return render_template('error.html', error='No "days" in POST params', code='NONE', backlink='/submit')
    if 'url' not in request.form:
        return render_template('error.html', error='No "url" in POST params', code='NONE', backlink='/submit')
    if 'network' not in request.form:
        return render_template('error.html', error='No "network" in POST params', code='NONE', backlink='/submit')
    if 'type' not in request.form:
        return render_template('error.html', error='No "type" in POST params', code='NONE', backlink='/submit')
    if 'tags' not in request.form:
        return render_template('error.html', error='No "tags" in POST params', code='NONE', backlink='/submit')
    if 'description' not in request.form:
        return render_template('error.html', error='No "description" in POST params', code='NONE', backlink='/submit')

    resource = {
        'url': request.form['url'],
        'network': request.form['network'],
        'type': request.form['type'],
        'lang': request.form['lang'],
        'tags': request.form['tags'],
        'description': request.form['description']
    }
    blk = DI.get_blockchain()
    data = blk.post_resource(resource, int(request.form['days']))

    if data['error'] and data['error']['code'] < 0:
        return render_template('error.html', error=data['error']['message'], code=data['error']['code'], backlink='/my')
    else:
        return render_template('ok.html', message='Resource submitted OK', backlink='/my')


@app.route('/add/<int:resource_id>', methods=['GET'])
def show_add(resource_id):
    rep = DI.get_repository()
    resource = rep.read_resource(resource_id)
    tags = rep.read_tags(resource['network_id'], resource['lang_id'], resource['type_id'])
    return render_template('add.html', nav='submit', resource=resource, tags_id=tags[0]['id'])


@app.route('/add/<int:resource_id>', methods=['POST'])
def add(resource_id):
    if 'days' not in request.form:
        return render_template('error.html', error='No "days" in POST params', code='NONE', backlink='/add/'+resource_id)
    if 'url' not in request.form:
        return render_template('error.html', error='No "url" in POST params', code='NONE', backlink='/add/'+resource_id)
    if 'description' not in request.form:
        return render_template('error.html', error='No "description" in POST params', code='NONE', backlink='/add/'+resource_id)

    resource = {
        'url': request.form['url'],
        'description': request.form['description']
    }
    blk = DI.get_blockchain()
    data = blk.post_resource(resource, int(request.form['days']))

    if data['error'] and data['error']['code'] < 0:
        return render_template('error.html', error=data['error']['message'], code=data['error']['code'], backlink='/my')
    else:
        return render_template('ok.html', message='Resource submitted OK', backlink='/my')


@app.route('/my/edit/<string:resource>', methods=['GET'])
def show_edit(resource):
    blk = DI.get_blockchain()
    data = blk.show_resource(resource)
    resourse = data['result']
    decoded = json.loads(resourse['value'])
    resourse.update(decoded)
    return render_template('edit.html', nav='my', resourse=resourse)


@app.route('/my/edit/<string:name>', methods=['POST'])
def edit(name):
    if 'days' not in request.form:
        return render_template('error.html', error='No "days" in POST params', code='NONE', backlink='/my/edit/'+name)
    if 'url' not in request.form:
        return render_template('error.html', error='No "url" in POST params', code='NONE', backlink='/my/edit/'+name)
    if 'network' not in request.form:
        return render_template('error.html', error='No "network" in POST params', code='NONE', backlink='/my/edit/'+name)
    if 'type' not in request.form:
        return render_template('error.html', error='No "type" in POST params', code='NONE', backlink='/my/edit/'+name)
    if 'tags' not in request.form:
        return render_template('error.html', error='No "tags" in POST params', code='NONE', backlink='/my/edit/'+name)
    if 'description' not in request.form:
        return render_template('error.html', error='No "description" in POST params', code='NONE', backlink='/my/edit/'+name)

    resource = {
        'url': request.form['url'],
        'network': request.form['network'],
        'type': request.form['type'],
        'lang': request.form['lang'],
        'tags': request.form['tags'],
        'description': request.form['description']
    }
    blk = DI.get_blockchain()
    data = blk.edit_resource(name, resource, int(request.form['days']))

    if data['error'] and data['error']['code'] < 0:
        return render_template('error.html', error=data['error']['message'], code=data['error']['code'], backlink='/my')
    else:
        return render_template('ok.html', nav='my', message='Resource "'+name+'" edited OK', backlink='/my')


@app.route('/my_descriptions/edit/<string:resource>', methods=['GET'])
def show_edit_description(resource):
    blk = DI.get_blockchain()
    data = blk.show_resource(resource)
    resourse = data['result']
    decoded = json.loads(resourse['value'])
    resourse.update(decoded)
    return render_template('descr.html', nav='my_descriptions', resourse=resourse)


@app.route('/my_descriptions/edit/<string:name>', methods=['POST'])
def edit_description(name):
    if 'days' not in request.form:
        return render_template('error.html', error='No "days" in POST params', code='NONE', backlink='/my/edit/'+name)
    if 'url' not in request.form:
        return render_template('error.html', error='No "url" in POST params', code='NONE', backlink='/my/edit/'+name)
    if 'description' not in request.form:
        return render_template('error.html', error='No "description" in POST params', code='NONE', backlink='/my/edit/'+name)

    resource = {
        'url': request.form['url'],
        'description': request.form['description']
    }

    blk = DI.get_blockchain()
    data = blk.edit_resource(name, resource, int(request.form['days']))

    if data['error'] and data['error']['code'] < 0:
        return render_template('error.html', error=data['error']['message'], code=data['error']['code'], backlink='/my_descriptions')
    else:
        return render_template('ok.html', nav='my', message='Resource "'+name+'" edited OK', backlink='/my_descriptions')


@app.route('/my/show/<string:resource>')
def show(resource):
    blk = DI.get_blockchain()
    data = blk.show_resource(resource)
    resourse = data['result']
    resourse['decoded'] = json.loads(resourse['value'])
    return render_template('resourse.html', nav='my', resourse=resourse)


@app.route('/my/delete/<string:resource>')
def delete(resource):
    blk = DI.get_blockchain()
    data = blk.delete_resource(resource)

    if data['error'] and data['error']['code'] < 0:
        return render_template('error.html', error=data['error']['message'], code=data['error']['code'], backlink='/my')
    else:
        return render_template('ok.html', message='DELETED OK', backlink='/my')


@app.route('/sync')
def sync():
    rep = DI.get_repository()
    blk = DI.get_blockchain()
    upd = Updater(rep, blk)
    upd.sync()
    return 'ok'


@app.route('/networks')
def show_networks():
    rep = DI.get_repository()
    blk = DI.get_blockchain()
    upd = Updater(rep, blk)
    upd.check()

    networks = rep.read_networks()
    return render_template('list/networks.html', title='Main', nav='tags', networks=networks)


@app.route('/langs/<int:network_id>')
def show_langs(network_id):
    rep = DI.get_repository()
    langs = rep.read_langs(network_id)
    network = rep.get_network_name_by_id(network_id)
    return render_template('list/langs.html', title='Main', nav='tags', langs=langs,
                           network_id=network_id, network=network)


@app.route('/types/<int:network_id>/<int:lang_id>')
def show_types(network_id, lang_id):
    rep = DI.get_repository()
    types = rep.read_types(network_id, lang_id)
    network = rep.get_network_name_by_id(network_id)
    lang = rep.get_lang_name_by_id(lang_id)
    return render_template('list/types.html', title='Main', nav='tags', types=types,
                           network_id=network_id, lang_id=lang_id,
                           network=network, lang=lang)


@app.route('/tags/<int:network_id>/<int:lang_id>/<int:type_id>')
def show_tags(network_id, lang_id, type_id):
    rep = DI.get_repository()
    tags = rep.read_tags(network_id, lang_id, type_id)
    network = rep.get_network_name_by_id(network_id)
    lang = rep.get_lang_name_by_id(lang_id)
    type = rep.get_type_name_by_id(type_id)
    return render_template('list/tags.html', title='Main', nav='tags', tags=tags,
                           network_id=network_id, lang_id=lang_id, type_id=type_id,
                           network=network, lang=lang, type=type)


@app.route('/links/<int:network_id>/<int:lang_id>/<int:type_id>/<int:tags_id>')
def show_resources(network_id, lang_id, type_id, tags_id):
    rep = DI.get_repository()
    resources = rep.read_resources(network_id, lang_id, type_id, tags_id)
    network = rep.get_network_name_by_id(network_id)
    lang = rep.get_lang_name_by_id(lang_id)
    type = rep.get_type_name_by_id(type_id)
    tag = rep.get_tag_name_by_id(tags_id)
    return render_template('list/resources.html', title='Main', nav='tags', resources=resources,
                           network_id=network_id, lang_id=lang_id, type_id=type_id, tags_id=tags_id,
                           network=network, lang=lang, type=type, tag=tag)


@app.route('/show/<int:network_id>/<int:lang_id>/<int:type_id>/<int:tags_id>/<int:resource_id>')
def show_resource(network_id, lang_id, type_id, tags_id, resource_id):
    rep = DI.get_repository()
    network = rep.get_network_name_by_id(network_id)
    lang = rep.get_lang_name_by_id(lang_id)
    type = rep.get_type_name_by_id(type_id)
    tag = rep.get_tag_name_by_id(tags_id)
    tags = rep.read_tags(network_id, lang_id, type_id)
    resource = rep.read_resource(resource_id)
    descriptions = rep.read_descriptions(resource_id)
    return render_template('list/resource.html', title='Main', nav='tags',
                           network_id=network_id, lang_id=lang_id, type_id=type_id, tags_id=tags_id,resource_id=resource_id,
                           network=network, lang=lang, type=type, tag=tag, tags=tags,
                           resource=resource, descriptions=descriptions)


@app.route('/search', methods=['GET'])
def show_search():
    return render_template('list/search.html', nav='search', title='Search', type='description', resources=[])


@app.route('/search', methods=['POST'])
def search():
    rep = DI.get_repository()
    blk = DI.get_blockchain()
    upd = Updater(rep, blk)
    upd.check()

    resources = []
    if request.form['type'] =='url':
        resources = rep.search_resources_by_url(request.form['search'])
    elif request.form['type'] == 'description':
        resources = rep.search_resources_by_description(request.form['search'])
    # print(resources)
    return render_template('list/search.html', nav='search', title='Search',
                           search=request.form['search'], type=request.form['type'], resources=resources)


@app.route('/config', methods=['POST'])
def post_config():
    Config.save_config({
            'host':       request.form['host'],
            'port':       int(request.form['port']),
            'user':       request.form['user'],
            'password':   request.form['password']
    })

    blk = DI.get_blockchain()
    if blk.check():
        result = 'Connection OK =)'
    else:
        result = 'FAILED'

    return render_template('config.html', nav='config', title='Config', result=result, data=request.form)


@app.route('/config', methods=['GET'])
def show_config():
    data = Config.get_config()
    return render_template('config.html', nav='config', title='Config', data=data)


@app.route('/test')
def test():
    # rep = DI.get_repository()
    # res = rep.search_resources_by_url('youtube')
    # print(res)
    # res = rep.search_resources_by_description('Биткоин')
    # print(res)
    # rep = DI.get_repository()
    # blk = DI.get_blockchain()
    # upd = Updater(rep, blk)
    # print(upd.check())

    blk = DI.get_blockchain()
    print(blk.check())
    return 'OK'


# app.run()