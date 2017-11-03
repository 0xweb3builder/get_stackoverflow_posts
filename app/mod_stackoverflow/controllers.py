# Import flask dependencies
from flask import Blueprint, render_template, request, make_response, current_app, redirect, session

# Import module models
from app.mod_stackoverflow.models import Posts

# Import module stackapi
from app.mod_stackapi.stackapi import StackAPI
from app.mod_stackapi.stackapi import StackAPIError

# Import module auth
from app.mod_auth import OAuthSignIn

# Import module utility
from app.mod_utility import DictObjHelper

# Define the blueprint: 'stackoverflow', set its url prefix: app.url/stackoverflow
mod_stackoverflow = Blueprint('stackoverflow', __name__, url_prefix='/stackoverflow', static_folder='../../static', template_folder='../../templates')


# Set the route and accepted methods
@mod_stackoverflow.route('/', methods=['GET'])
def default_page():
    _uid = DictObjHelper.get_value(session, 'uid', '')
    return render_template('stackoverflow/getposts.html', uid=_uid)


@mod_stackoverflow.route('/authorize')
def oauth_authorize():
    oauth = OAuthSignIn.get_provider('stackoverflow')
    return oauth.authorize()


@mod_stackoverflow.route('/callback/<provider>')
def oauth_callback(provider):
    _oauth = OAuthSignIn.get_provider(provider)
    _access_token = _oauth.callback()
    _user_id = 0
    try:
        SITE = StackAPI('stackoverflow', key=current_app.config['SE_API_KEY'], access_token=_access_token)
        _res = SITE.fetch('me', order='desc')
        _items = DictObjHelper.get_value(_res, 'items', None)
        if _items is not None and len(_items) > 0:
            _user_id = DictObjHelper.get_value(_items[0], 'user_id', 0)
    except StackAPIError as e:
        pass

    session['uid'] = str(_user_id)
    return redirect('stackoverflow/')


@mod_stackoverflow.route('/getposts', methods=['POST'])
def get_posts():
    _uid = DictObjHelper.get_value(request.form, 'uid', None)
    _query_pos = DictObjHelper.get_value(request.form, 'querypos', 0)
    _page_size = DictObjHelper.get_value(request.form, 'pagesize', 0)
    _max_pages = DictObjHelper.get_value(request.form, 'maxpages', 0)

    if _query_pos <= 0:
        _query_pos = 1

    if _page_size <= 0 or _page_size > 100:
        _page_size = 10

    if _max_pages <= 0 or _max_pages > 10:
        _max_pages = 1

    _page = int((_query_pos - 1) / _page_size) + 1
    _itempos = int((_query_pos - 1) % _page_size)

    try:
        SITE = StackAPI('stackoverflow', key=current_app.config['SE_API_KEY'])
        SITE.page_size=_page_size
        SITE.max_pages=_max_pages
        _res = SITE.fetch('users/'+str(_uid)+'/posts', page=_page, order='desc', sort='activity', filter=current_app.config['FILTER_TITLE_BODY'])

        _posts = Posts.load(_res, _itempos)

        if hasattr(_posts, 'items'):
            _posts.query_pos = _query_pos
    except StackAPIError as e:
        return make_response(Posts.error(e.error, e.code, e.message).toJSON(), e.error)
    except:
        return make_response(Posts.error(500, "internal_error", "unknown error").toJSON(), 500)

    return _posts.toJSON()

