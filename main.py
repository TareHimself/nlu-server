import asyncio
from glob import glob
from os import getcwd, path
from re import A
from tkinter import N
from utils import TrainModel, RunProxy
from regex import F
from server import WebServer
from aiohttp import web
from rasa.core.agent import Agent
from nlu2json import dict2nlu
from subprocess import Popen

DEFAULT_NLU_DATA = path.join(getcwd(), 'rasa', 'nlu.yml')
NLU_MODEL_DIR = path.join(getcwd(), 'models', 'nlu.tar.gz')
TEMP_NLU_DATA = path.join(getcwd(), 'temp_nlu.yml')

is_training_model = False


async def init():
    if not path.exists(TEMP_NLU_DATA):
        with open(TEMP_NLU_DATA, 'wb') as tmp_file:
            with open(DEFAULT_NLU_DATA, 'rb') as tmp_file_og:
                print('GENERATING TEMP FILE')
                tmp_file.write(tmp_file_og.read())

    if not path.exists(NLU_MODEL_DIR):
        await TrainModel(TEMP_NLU_DATA)

    print(is_training_model)


loop = asyncio.new_event_loop()

loop.run_until_complete(init())

app = WebServer()

agent = Agent.load(model_path=NLU_MODEL_DIR)


def JsonResponse(data="", error=""):
    return web.json_response({'data': data, 'error': error})


@app.Get('/')
async def Home(request: web.Request):
    return web.Response(text="YAMETEHHH")


@app.Get('/parse')
async def ParseString(request: web.Request):
    global is_training_model
    if is_training_model:
        return JsonResponse(error="TRAINING_MODEL")

    if 'q' in request.rel_url.query.keys():
        return JsonResponse(data=await agent.parse_message(request.rel_url.query['q']))

    return JsonResponse(error="No Text Sent")


@app.Post('/train')
async def RetrainNlu(request: web.Request):
    global is_training_model
    global DEFAULT_NLU_DATA
    global NLU_MODEL_DIR

    if is_training_model:
        return JsonResponse(error="TRAINING_MODEL")

    is_training_model = True

    try:
        if request.can_read_body:
            body = await request.json()
            print(body)
            with open(TEMP_NLU_DATA, 'w') as tmp_file:
                tmp_file.write(dict2nlu(body))
        else:
            with open(TEMP_NLU_DATA, 'wb') as tmp_file:
                print("Opened Temp File")
                with open(DEFAULT_NLU_DATA, 'rb') as tmp_file_og:
                    print("Opened NORMAL FILE")
                    tmp_file.write(tmp_file_og.read())

        await TrainModel(TEMP_NLU_DATA)

        agent.load_model(NLU_MODEL_DIR)

        is_training_model = False

        return JsonResponse(data="NO HASH SYSTEM")
    except Exception as e:
        print(e)
        is_training_model = False
        return JsonResponse(data="NO HASH SYSTEM")

RunProxy()
app.listen('localhost', 8097)
