import aiohttp 
import aiofiles
import asyncio 
import pandas as pd 
import os


def get_categories(file:str):
    df = pd.read_csv(file)

    df['категория рейтинга'] = pd.cut(df['рейтинг'], 5)

    return df

async def download(session, image_link, category, id):
    print(image_link)
    async with session.get(url=image_link) as response:
        name = os.path.join(f'images/{category}', f'{id}.jpg')
        print(name)
        os.makedirs(os.path.dirname(name), exist_ok=True)
        async with aiofiles.open(name, 'wb') as file:
            await file.write(await response.read())

async def save_images(df):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, row in df.iterrows():
            for i, link in enumerate(row['ссылка на фото'].split(';')[:3]):
                if link != "":
                    task = asyncio.create_task(download(session, link, str(row['категория рейтинга']), f"{row['id']}_{i}"))
                    tasks.append(task)
        await asyncio.gather(*tasks)

def get_images(file, inplace=False):
    if inplace:
        df = get_categories(file)
        df.to_csv(file)
        asyncio.run(save_images(df))
    else:
        df = get_categories(file)
        asyncio.run(save_images(df))

if __name__ == "__main__":
    get_images('wb_parse_subject=406.csv')
