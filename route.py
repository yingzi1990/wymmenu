import json
import os
import urllib.error
import urllib.request
from aiohttp import web
from server import PromptServer
from .api.menu import getmenu
from .api.workflow import getworkflow


@PromptServer.instance.routes.get("/wymcomfy/showcases")
async def get_route_menu(request):
    return handle_request(getmenu, 1)

@PromptServer.instance.routes.post("/wymcomfy/workflow")
async def get_route_file(request):
    req = await request.json()
    file_param = req.get('file')
    if file_param is None:
        return web.Response(
            text=json.dumps({"error": "Missing 'file' parameter"}),
            status=400,
            content_type="application/json"
        )
    return handle_request(getworkflow, file_param)

def handle_request(handler_func, *args, **kwargs):
    try:
        data = handler_func(*args, **kwargs)
        return web.Response(
            text=json.dumps(data, ensure_ascii=False),
            content_type="application/json"
        )
    except json.JSONDecodeError:
        return web.Response(
            text=json.dumps({"error": "Invalid JSON body"}),
            status=400,
            content_type="application/json"
        )
    except Exception as e:
        return web.Response(
            text=json.dumps({"error": f"API Error: {str(e)}"}),
            status=500,
            content_type="application/json"
        )