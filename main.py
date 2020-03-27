from aiohttp import web, hdrs
from pathlib import Path
import os

app = web.Application()

async def storage_video_handler(request):
    reader = await request.multipart()

    # dir_path
    part = await reader.next()
    dp = (await part.read()).decode()
    dir_path = os.getenv('HOME') + dp
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    # video part
    video = await reader.next()
    filename = video.filename
    with open(os.path.join(dir_path, filename), 'wb') as f:
        while True:
            chunk = await video.read_chunk()
            if not chunk:
                break
            f.write(chunk)
    # audio part
    audio = await reader.next()
    filename = audio.filename
    with open(os.path.join(dir_path, filename), 'wb') as f:
        while True:
            chunk = await audio.read_chunk()
            if not chunk:
                break
            f.write(chunk)
    # mpd part
    mpd = await reader.next()
    filename = mpd.filename
    with open(os.path.join(dir_path, filename), 'wb') as f:
        while True:
            chunk = await mpd.read_chunk()
            if not chunk:
                break
            f.write(chunk)
    return web.json_response({'dir_path': dir_path + "/" + filename})


async def storage_doc_handler(request):
    reader = await request.multipart()
    # dir_path
    part = await reader.next()
    dp = (await part.read()).decode()
    dir_path = os.getenv('HOME') + dp
    Path(dir_path).mkdir(parents=True, exist_ok=True)

    # doc
    doc = await reader.next()
    filename = doc.filename
    with open(os.path.join(dir_path, filename), 'wb') as f:
        while True:
            chunk = await doc.read_chunk()
            if not chunk:
                break
            f.write(chunk)
    return web.json_response({'dir_path': dir_path + "/" + filename})

app.router.add_routes([
    web.post('/storage_video', storage_video_handler),
    web.post('/storage_doc', storage_doc_handler)
])

if __name__ == "__main__":
    web.run_app(app, port=8080)
