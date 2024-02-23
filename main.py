import nextcord, argparse
from nextcord.ext import commands
from dotenv import load_dotenv
from os import environ

Parser = argparse.ArgumentParser()
for i in ["question", "reply"]:
    Parser.add_argument(f"--{i}", required=True)

Bot = commands.Bot(intents=nextcord.Intents.all())

def main():
    load_dotenv()
    global Args
    Args = Parser.parse_args()
    Bot.run(environ.get("TOKEN"))

@Bot.event
async def on_ready():
    question = f"QOTD: {Args.question}"
    await (
        await (
            await Bot.get_channel(int(environ.get("CHANNEL"))).send(f"{question} @everyone")
        ).create_thread(name=question)
    ).send(Args.reply)
    await Bot.close()


if __name__=="__main__":
    main()