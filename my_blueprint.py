from sanic import Blueprint,Request,text
from sanic import request
from sanic.response import json

bp = Blueprint("my_Blueprint",url_prefix="/account")

@bp.route("/state",methods = ["GET","POST"])
async def get_name(request):
    request.ctx.numbers.append(7)
    return json(request.ctx.numbers)

