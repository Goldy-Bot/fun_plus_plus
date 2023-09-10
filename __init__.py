import random
import GoldyBot
from io import BytesIO

class FunPlusPlus(GoldyBot.Extension):
    def __init__(self):
        super().__init__()

        self.http_session = self.goldy.http_client._session
        self.rip_footer = GoldyBot.EmbedFooter(
            text = "🖤 Rest in piece, Telk (the original creator of the API used here). You will be missed."
        )
        self.cat_embed_titles = ["😺 Meow!", "😻 Kitty!", "😽 Kitty Cat"]

    @GoldyBot.command(description = "😺 Returns a random adorable meow meow.", wait = True)
    async def cat(self, platter: GoldyBot.GoldPlatter):
        r = await self.http_session.get("https://some-random-api.com/img/cat")
        data = await r.json()

        cat_image_response = await self.http_session.get(data["link"])

        cat_image_bytes = await cat_image_response.read()
        cat_image = GoldyBot.File(BytesIO(cat_image_bytes), file_name = "image.png")

        embed = GoldyBot.Embed(
            colour = GoldyBot.Colours.from_image(cat_image),  
            image = GoldyBot.EmbedImage(cat_image.attachment_url),
            footer = self.rip_footer if random.randint(0, 4) == 0 else None
        )

        await platter.send_message(
            embeds = [embed], 
            files = [cat_image],
            reply = True
        )


load = lambda: FunPlusPlus()