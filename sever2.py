import logging

import ujson

from models import Users
from tortoise.contrib.sanic import register_tortoise
from sanic import Sanic,response,text,Request,json

logging.basicConfig(level=logging.DEBUG)

app = Sanic(__name__)

@app.route("/user/create/",methods=["GET","POST"])
async def add_user(request):
    message = request.json
    user = await Users.create(name=message.get('name'))
    await user.save()
    return text("Done")

@app.route("/user")
async def list_all(request):
    users = await Users.all()
    if users is None:
        return text("No Database")
    newdict = []
    for user in users:
        newdict.append({"id":user.id,"name":user.name})
    return response.json({"user" : newdict})


@app.route("/user/identify/<id:int>")
async def get_user(request,id:int ):
    user = await Users.filter(id=id).first()
    return response.json({"id": user.id , "name": user.name})


@app.post("/user/update")
async def update_user(request:Request):
    message = request.json
    await Users.update_or_create(id = message.get('id') ,name = message.get('name'))
    return json({"id": message.get('id')}, status=200)


@app.post("/user/delete")
async def delete_user(request:Request):
    message = request.json
    await Users.filter(id = message.get('id')).delete()
    return text("Done")


register_tortoise(
    app, db_url="sqlite://db.sqlite3", modules={"models": ["models"]}, generate_schemas=True
)







if __name__ == '__main__':
    app.run(debug=True,port = 9999,auto_reload=True)