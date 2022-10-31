import asyncio
import hashlib
from os import getcwd, path
from subprocess import Popen
import sys
from threading import Thread
from rasa.model_training import train_nlu


async def GetFileHash(dir: str, block_size=65536):
    loop = asyncio.get_running_loop()
    task_return = asyncio.Future()
    file_hash = hashlib.sha256()

    def HashThread():
        with open(dir, 'rb') as f:
            fb = f.read(block_size)
            while len(fb) > 0:
                loop.call_soon_threadsafe(file_hash.update, fb)
                (fb)
                fb = f.read(block_size)
            loop.call_soon_threadsafe(task_return.set_result, file_hash)

    Thread(daemon=True, target=HashThread, group=None).start()

    result = await task_return

    return result


async def TrainModel(dir: str, block_size=65536):
    loop = asyncio.get_running_loop()
    task_return = asyncio.Future()

    def TrainModelThread():
        train_nlu(config=path.join(getcwd(), 'rasa', 'config.yml'), nlu_data=path.join(getcwd(), 'temp_nlu.yml'),
                  output=path.join(getcwd(), 'models'), fixed_model_name='nlu')

        loop.call_soon_threadsafe(task_return.set_result, None)

    Thread(daemon=True, target=TrainModelThread, group=None).start()

    await task_return

    return


def _start_proxy():
    Popen(['npm', 'start'], stdout=sys.stdout,
          stderr=sys.stderr, shell=True).communicate()


def RunProxy():
    Thread(daemon=True, target=_start_proxy, group=None).start()
