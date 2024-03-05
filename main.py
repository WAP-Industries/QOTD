import nextcord
from nextcord.ext import commands, tasks
from dotenv import load_dotenv
from os import environ
from json import dumps, load
from datetime import datetime, time

class QOTD:
    Bot = commands.Bot(intents=nextcord.Intents.all())
    QFile = "questions.json"
    Config = {}

    @Bot.event
    async def on_ready():
        print("im running nigga")
        await QOTD.SendQuestion()

    @staticmethod
    def CheckTime(h, m) -> bool:
        d = datetime.now().date()
        t = datetime.now().time()
        return datetime.combine(d, time(t.hour, t.minute, t.second))==datetime.combine(d, time(h, m, 0))

    async def SendQuestion():
        while True:
            while not QOTD.CheckTime(7, 0):
                await __import__("asyncio").sleep(1)

            with open(QOTD.QFile) as f:
                QOTD.Config = load(f)
            Question, Reply = QOTD.Config["Questions"][QOTD.Config["Index"]]

            await (
                await (
                    await QOTD.Bot.get_channel(int(environ.get("CHANNEL"))).send(f"QOTD: {Question} @everyone")
                ).create_thread(name=f"{Question[0].upper()+Question[1:]}", auto_archive_duration=4320)
            ).send(Reply)
            
            QOTD.Config["Index"]+=1*(QOTD.Config["Index"]<len(QOTD.Config["Questions"])-1)
            with open(QOTD.QFile, "w") as f:
                f.write(dumps(QOTD.Config, indent=4))

            print(f"Question: {Question}\nReply: {Reply}\n")


def main():
    load_dotenv()
    QOTD.Bot.run(environ.get("TOKEN"))


if __name__=="__main__":
    main()