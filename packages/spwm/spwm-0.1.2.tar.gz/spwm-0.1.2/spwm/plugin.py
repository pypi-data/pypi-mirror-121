import os
import json
import logging
import requests
from typing import TYPE_CHECKING, Any, List, Optional, Union

from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import get_user_model
from django.core.signing import Signer

from saleor.plugins.base_plugin import BasePlugin
from saleor.core.auth import get_token_from_request

User = get_user_model()
signer = Signer()


class SpwmPlugin(BasePlugin):
    """."""

    PLUGIN_ID = "riiy.spwm"
    PLUGIN_NAME = "spwm"

    def webhook(self, request: WSGIRequest, path: str, previous_value) -> HttpResponse:
        # check if plugin is active
        # check signatures and headers.
        if path == '/get-token/':
            # do something with the request
            data = request.data
            open_id = OpenidUtils(data["code"]).get_openid()
            user, _ = User.objects.get_or_create(email=f"wx_{open_id}")
            token = signer.sign(user.id)
            return JsonResponse(data={"token": token})

        return HttpResponseNotFound()

    def authenticate_user(self, request: WSGIRequest, previous_value) -> Optional["User"]:
        """."""

        token = get_token_from_request(request)
        uid = signer.unsign(token)
        user = User.objects.get(uid)
        return user


class OpenidUtils(object):
    def __init__(self, jscode):
        self.url = "https://api.weixin.qq.com/sns/jscode2session"
        self.appid = os.environ.get('WX_MP_APPID')
        self.secret = os.environ.get('WX_MP_APPSECRET')
        self.jscode = jscode

    def get_openid(self):
        url = (self.url + "?appid=" + self.appid + "&secret=" + self.secret + "&js_code=" + self.jscode + "&grant_type=authorization_code")
        r = requests.get(url)
        openid = r.json()["openid"]
        return openid
