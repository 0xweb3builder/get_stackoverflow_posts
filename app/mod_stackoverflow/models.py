
import json

from app.mod_utility import DictObjHelper


class Owner:
    @staticmethod
    def load(dict_obj):
        if dict_obj is None:
            return None

        _owner = Owner()

        _profile_image = DictObjHelper.get_value(dict_obj, 'profile_image', None)
        if _profile_image is not None:
            _owner.profile_image = _profile_image
        _display_name = DictObjHelper.get_value(dict_obj, 'display_name', None)
        if _display_name is not None:
            _owner.display_name = _display_name
        _link = DictObjHelper.get_value(dict_obj, 'link', None)
        if _link is not None:
            _owner.link = _link

        return _owner

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Post:
    @staticmethod
    def load(dict_obj):
        if dict_obj is None:
            return None

        _post = Post()

        _owner = Owner.load(DictObjHelper.get_value(dict_obj, 'owner', None))
        if _owner is not None:
            _post.owner = _owner

        #_post_id = DictObjHelper.get_value(dict_obj, 'post_id', None)
        #if _post_id is not None:
        #    _post.post_id = _post_id
        _post_type = DictObjHelper.get_value(dict_obj, 'post_type', None)
        if _post_type is not None:
            _post.post_type = _post_type
        _creation_date = DictObjHelper.get_value(dict_obj, 'creation_date', None)
        if _creation_date is not None:
            _post.creation_date = _creation_date
        _last_edit_date = DictObjHelper.get_value(dict_obj, 'last_edit_date', None)
        if _last_edit_date is not None:
            _post.last_edit_date = _last_edit_date
        _last_activity_date = DictObjHelper.get_value(dict_obj, 'last_activity_date', None)
        if _last_activity_date is not None:
            _post.last_activity_date = _last_activity_date
        _link = DictObjHelper.get_value(dict_obj, 'link', None)
        if _link is not None:
            _post.link = _link
        _title = DictObjHelper.get_value(dict_obj, 'title', None)
        if _title is not None:
            _post.title = _title
        _body = DictObjHelper.get_value(dict_obj, 'body', None)
        if _body is not None:
            _post.body = _body

        return _post

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Posts:
    @staticmethod
    def error(id, name, message):
        #self.items = []
        #self.has_more = False
        _posts = Posts()
        _posts.error_id = id
        _posts.error_name = name
        _posts.error_message = message
        return _posts

    def add_item(self, post):
        if not hasattr(self, 'items') or self.items is None:
            self.items = []
        self.items.append(post)

    @staticmethod
    def load(dict_obj, item_pos):
        if dict_obj is None:
            return Posts.error(500, "not_reach", "could not reach out server")

        _items = DictObjHelper.get_value(dict_obj, 'items', None)
        if _items is None or DictObjHelper.check_value(dict_obj, 'error_id'):
            return Posts.error(DictObjHelper.get_value(dict_obj, 'error_id', 0), DictObjHelper.get_value(dict_obj, 'error_name', None), DictObjHelper.get_value(dict_obj, 'error_message', None))

        _posts = Posts()

        _posts.has_more = DictObjHelper.get_value(dict_obj, 'has_more', False)

        _i = item_pos
        _count = len(_items)
        while _i < _count:
            _post = Post.load(_items[_i])
            if _post:
                _posts.add_item(_post)
            _i = _i + 1

        return _posts

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

