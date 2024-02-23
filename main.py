import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from os import environ

Bot = commands.Bot(intents=nextcord.Intents.all())

def main():
    load_dotenv()

    global Question, Reply
    Question, Reply = __import__("sys").argv[1:]
    Bot.run(environ.get("TOKEN"))

@Bot.event
async def on_ready():
    await (
        await (
            await Bot.get_channel(int(environ.get("CHANNEL"))).send(f"QOTD: {Question} @everyone")
        ).create_thread(name=Question)
    ).send(Reply)
    await Bot.close()


if __name__=="__main__":
    main()
