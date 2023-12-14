import random
import GoldyBot
from io import BytesIO

from .goldy import Goldy
from .utils import uwuify_string

class FunPlusPlus(GoldyBot.Extension):
    def __init__(self):
        super().__init__()

        self.http_session = self.goldy.http_client._session
        self.rip_footer = GoldyBot.EmbedFooter(
            text = "🖤 Rest in piece, Telk (the original creator of the API used here). You will be missed."
        )
        self.cat_footers = ["😺 Meow!", "😻 Kitty!", "😽 Kitty Cat!"]


    @GoldyBot.command(description = "😺 Returns a random adorable meow meow.", wait = True)
    async def cat(self, platter: GoldyBot.GoldPlatter):
        r = await self.http_session.get("https://some-random-api.com/img/cat")
        data = await r.json()

        cat_image_response = await self.http_session.get(data["link"])

        cat_image_bytes = await cat_image_response.read()
        cat_image = GoldyBot.File(BytesIO(cat_image_bytes), file_name = "image.png")

        embed = GoldyBot.Embed(
            colour = GoldyBot.Colours.from_image(cat_image),  
            image = GoldyBot.EmbedImage(data["link"])
        )

        embed.set_random_footer([self.rip_footer] + self.cat_footers)

        await platter.send_message(
            embeds = [embed], 
            reply = True
        )

    @GoldyBot.command("uwuify", description = "😳 Translates English into UwU language.", wait = True)
    async def uwuify_cmd(self, platter: GoldyBot.GoldPlatter, text: str):
        result = await uwuify_string(text, self.goldy)

        embed = GoldyBot.Embed(
            "🟧 UwUify", 
            description = f"""
            ```
            {result}
            ```
            """, 
            colour = GoldyBot.Colours.AKI_ORANGE
        )

        await platter.send_message(embeds = [embed])


def load():
    Goldy()
    FunPlusPlus()