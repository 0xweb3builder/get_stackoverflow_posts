from flask import url_for, current_app, redirect, request
from rauth import OAuth2Service

import json
from urllib import parse

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for(self.provider_name + '.oauth_callback', provider=self.provider_name,
                        _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers={}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class StackOverflowSignIn(OAuthSignIn):
    def __init__(self):
        super(StackOverflowSignIn, self).__init__('stackoverflow')
        self.service = OAuth2Service(
                name='stackoverflow',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url='https://stackexchange.com/oauth',
                base_url='https://api.stackexchange.com/2.2/me?order=desc&sort=reputation&site=stackoverflow&filter=!)s6)1w2OzDQ_mRCVl1UI',
                access_token_url='https://stackexchange.com/oauth/access_token'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            redirect_uri=self.get_callback_url())
            )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'redirect_uri': self.get_callback_url()
                     },
                decoder = decode
        )
        #me = oauth_session.get('').json()
        return oauth_session.access_token[0]


def decode(data):
    return parse.parse_qs(str(data, "utf-8"))

