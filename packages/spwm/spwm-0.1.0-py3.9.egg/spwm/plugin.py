import json
import logging
from typing import TYPE_CHECKING, Any, List, Optional, Union

from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.core.handlers.wsgi import WSGIRequest

from saleor.plugins.base_plugin import BasePlugin


class SpwmPlugin(BasePlugin):
    """."""

    PLUGIN_ID = "riiy.spwm"
    PLUGIN_NAME = "spwm"

    def webhook(self, request: WSGIRequest, path: str, previous_value) -> HttpResponse:
        # check if plugin is active
        # check signatures and headers.
        if path == '/get-token/':
            # do something with the request
            return JsonResponse(data={"token":True})

        return HttpResponseNotFound()
