from pyrogram import Client
import os
import random
from pyrogram import raw
import asyncio

filepath = os.path.abspath(__file__)
proxy_dir = filepath.replace("\\main.py", "\\proxy")
users_dir = filepath.replace('\\main.py', '\\users')
sessions_dir = os.path.join(os.path.dirname(filepath), 'sessions')

with open(f'{proxy_dir}/' + 'proxy.txt', 'r') as fl:
    proxy_list = fl.read().split('\n')

with open(f'{users_dir}/' + 'users.txt', 'r') as fl:
    users_list = fl.read().split('\n')

sessions = []

for files in os.listdir(sessions_dir):
    if files.endswith(".sessions"):
        files = files.split('.')
        sessions.append(files[0])

cur_proxy = random.choice(proxy_list)

app = Client(sessions[0], workdir=sessions_dir)


async def read_stories():
    for user in users_list:
        try:
            res = await app.invoke(raw.functions.stories.GetUserStories(user_id=await app.resolve_peer(user)))
            if len(res.stories.stories) > 0:
                await app.invoke(raw.functions.stories.ReadStories(user_id=await app.resolve_peer(user), max_id=30))
                print(f'All stories of {user} were seen')
                await asyncio.sleep(30)
            else:
                print(f'User {user} has no stories')
                await asyncio.sleep(30)
        except Exception as e:
            print(f'There is an error: {e}')
            await asyncio.sleep(30)

if __name__ == "__main__":
    app.start()
    asyncio.get_event_loop().run_until_complete(read_stories())
