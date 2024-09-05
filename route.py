import json
import os
import urllib.error
import urllib.request
from aiohttp import web
from server import PromptServer
from .config.data import apiserver
from .api.menu import getmenu
from .api.workflow import getworkflow


@PromptServer.instance.routes.get("/wymcomfy/showcases")
async def set_api_key_page(request):
    data = getmenu(apiserver,1)
    return web.Response(
        text=json.dumps(data, ensure_ascii=False), content_type="application/json"
    )

@PromptServer.instance.routes.post("/wymcomfy/workflow")
async def get_file_content(request):
    try:
        req = await request.json()
    except json.JSONDecodeError:
        return web.Response(
            text=json.dumps({"error": "Invalid JSON body"}),
            status=400,
            content_type="application/json",
        )
    data = getworkflow(apiserver,req.get('file'))
    if data:
        return web.Response(
            text=json.dumps(data, ensure_ascii=False), content_type="application/json"
        )
    else:
        return web.Response(
            text=json.dumps({"error": "Invalid file name"}),
            status=400,
            content_type="application/json",
        )