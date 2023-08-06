# CoffeePaginator

Простой модуль для создания страниц в Disnake

## Пример использования

```py
import disnake
from disnake.ext import commands
from CoffeePaginator.CoffeePaginator import Paginator # да, немного тупонул, позже исправлю

Bot = commands.Bot(command_prefix='^')

@Bot.command()
async def test(ctx):
    emb1 = disnake.Embed(title='1 страница')
    emb2 = disnake.Embed(title='1 страница')
    emb3 = disnake.Embed(title='1 страница')
    emb4 = disnake.Embed(title='1 страница')
    
    embs = [emb1, emb2, emb3, emb4]
    message = await ctx.send(embed=emb1)
    
    pages = Paginator(message, embs)
    await pages.start()
    
Bot.run('токен')
```
