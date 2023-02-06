from sanic import Sanic,text,Request,empty
from enum import Enum, auto
from my_blueprint import bp
from datetime import date
from sanic.response import json


class Flavours(Enum):
    VANILLA = auto()
    CHOCOLATE = auto()
    STRAWBERRY = auto()
    MANGO = auto()


class ParticipantType(Enum):
    FARMER = auto()
    UNKNOWN = auto()
    RESTRUANT = auto()
    CONSUMER = auto()


flavour_pattern = "|".join(
    f.lower() for f in Flavours.__members__.keys()
)

def parse_flavour(flavour:str)->Flavours:
    try:
        return Flavours[flavour.upper()]
    except KeyError:
        raise ValueError(f"NO Ice Cream named {flavour} ")


app = Sanic(__name__)


app.router.register_pattern(
    "ice_cream_pattern",
    parse_flavour,
    flavour_pattern,
)



@app.on_request
async def one(request):
    request.ctx.numbers = []
    request.ctx.numbers.append(1)

@bp.on_request
async def two(request):
    request.ctx.numbers.append(2)


@app.on_request
async def one(request):
    request.ctx.numbers.append(3)

@bp.on_request
async def two(request):
    request.ctx.numbers.append(4)


@app.on_request
async def one(request):
    request.ctx.numbers.append(5)


@bp.on_request
async def two(request):
    request.ctx.numbers.append(6)



@app.route("/")
async def handler(request:Request):
    return json(request.ctx.numbers)

@bp.get("/")
async def bp_handler(request):
    return json(request.ctx.numbers)

app.blueprint(bp)
@app.route("/ilikecookies")
async def cookie_setter(request):
    res = text("YUM Delicious")
    res.cookies["flavour"] = "Chococlate"
    res.cookies["Car"] = "Toyota"
    return res

@app.get("icecream/<flavours:ice_cream_pattern>")
async def get_flavour(request: Request , flavours:Flavours):
    return text(f"You chose {flavours}")



@app.get("/stalls/<flavours:ice_cream_pattern>")
async def marks_stuff(request:Request, flavours:Flavours):
    header = request.headers.get("participant-type","unknown")
    try:
        participant_type = ParticipantType[header.upper()]
    except KeyError:
        participant_type = ParticipantType.UNKNOWN

    return text(f'The particiaont type is {participant_type.name}')


if __name__ == '__main__':
    app.run(port=9999, debug=True)





