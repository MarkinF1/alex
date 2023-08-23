# echo-client.py
import asyncio
import socket
import subprocess

import pyglet
import random
import os
import vlc

from yandex_music import ClientAsync

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65433  # The port used by the server

token_ya = "y0_AgAAAAATcVUFAAG8XgAAAADRYTEtzsxY8-GoT8OinblEpIJRJT5_7UI"

client = ClientAsync(token=token_ya)
queue_ = []

vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()


turn_on = True


async def play_music_from_queue():
    global queue_, turn_on, player, vlc_instance

    while turn_on:
        if len(queue_):
            song, duration = queue_.pop(0)
            vlc_media = vlc_instance.media_new(song)
            player.set_media(vlc_media)
            player.play()
            await asyncio.sleep(duration)
        else:
            await asyncio.sleep(1)


def clean_song_name(filename):
    symbolics = ['!', '@', '#', '№', '$', '%', '^', '&', '*', '"', '№', ';', ':', '?', '<', '>', ',', '\\', "'"]
    for symbolic in symbolics:
        filename = filename.replace(symbolic, '')
    return filename


dls_uuid = None
async def download_liked_songs():
    global queue_, turn_on, dls_uuid

    # Добавить создние uuid и специальную переменную хранения его

    liked_short_track = await client.users_likes_tracks()
    queue_ = []
    for track in liked_short_track:
        full_track = await track.fetch_track_async()
        filename = r"./music/{}_-_{}.mp3".format(full_track["albums"][0].title.replace(' ', '_'),
                                                 full_track['artists'][0].name.replace(' ', '_'))
        filename = clean_song_name(filename=filename)
        await full_track.download_async(filename)
        queue_.append((filename, full_track.duration_ms // 1000))
        print(queue_)
        await asyncio.sleep(full_track.duration_ms // 1000 - 1)
        if not turn_on:
            return

    turn_on = False


async def play_yandex_music_liked_songs():
    tasks = [asyncio.create_task(download_liked_songs()),
             asyncio.create_task(play_music_from_queue())]
    for task in tasks:
        await task


async def get_command():
    reader, _ = await asyncio.open_connection(HOST, PORT)
    data = await reader.read(1024)
    data = data.decode("utf-8")
    return data


async def listen():
    global turn_on

    task = None
    reader, _ = await asyncio.open_connection(HOST, PORT)
    while True:
        data = await reader.read(1024)
        print(data)
        data = data.decode("utf-8")

        print(f"Команда - {data}")
        if data == 'play':
            turn_on = True
            task = asyncio.create_task(play_yandex_music_liked_songs())
        elif data == 'stop':
            player.stop()
            turn_on = False
        elif data == 'disconnect':
            player.stop()
            turn_on = False
            exit(0)
        else:
            print(f"I don't know")

    if task:
        await task


async def main():
    global client
    await client.init()

    listen_task = asyncio.create_task(listen())
    await listen_task


asyncio.run(main())
