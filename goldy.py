from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, List, Awaitable
    from GoldyBot.goldy.recipes import RECIPE_CALLBACK

import random
from PIL import Image
from io import BytesIO
from .utils import uwuify_string

import GoldyBot

class Goldy(GoldyBot.Extension):
    def __init__(self):
        super().__init__()

        self.member_attempts: Dict[str, int] = {}

        self.actions: Dict[int, List[Awaitable | RECIPE_CALLBACK]] = {
            1: [
                lambda x: x.send_message(
                    f"""
                    > Okay let's stop here, I don't want you to end up like the last guy so please ignore this command and continue with your day. Thank you!
                    > 
                    > Kind regards,
                    > {self.goldy.config.branding_name}
                    """, 
                    reply = True
                ),
            ],
            2: [
                self.uwuify,
                lambda x: x.send_message(f"HEY I'M FROM THE FUTURE, Goldy Corp will take over the world in 2036 with A.I robots!", reply = True),
                lambda x: x.send_message(f"**{self.goldy.config.branding_name} A.I** Soon™", reply = True),
            ],
            3: [
                self.squash_member,
                lambda x: x.send_message("Alright you've found the special command, now stop invoking it please.", reply = True),
            ],
            4: [
                lambda x: x.send_message(
                    "Alright please stop, I think I'm running out of responses. I'm not an A.I you know.... *not **yet** at least* but you get the point.", 
                    reply = True
                ),
            ],
            5: [
                lambda x: x.send_message("mf you reached your limit.", reply = True),
                lambda x: x.send_message("❤️ You're now banned from the ``/goldy`` command. Have fun!", reply = True),
                lambda x: x.send_message("You've reached your limit, go mfing cry 😭 about it...", reply = True),
            ],
            6: [
                lambda x: x.send_message("**🛑 ALRIGHT FU#K IT, I'M NOT RESPONDING TO YOU ANYMORE!!! 🛑**", reply = True),
            ]
        }

    @GoldyBot.command(
        name = "goldy",
        description = "✨ Huh, a mysterious command has appeared. The heck is this?!"
    )
    async def goldy_cmd(self, platter: GoldyBot.GoldPlatter):
        member_id = platter.author.id

        if not member_id in self.member_attempts:
            self.member_attempts[member_id] = 1

        elif self.member_attempts[member_id] > len(self.actions):
            return False

        action = random.choice(self.actions[self.member_attempts[member_id]])
        await action(platter)

        self.member_attempts[member_id] += 1


    async def squash_member(self, platter: GoldyBot.GoldPlatter):
        r = await self.goldy.http_client._session.get(platter.author.avatar_url)
        bytes = await r.read()
        author_avatar = Image.open(BytesIO(bytes))
        author_avatar = author_avatar.resize((author_avatar.width, int(author_avatar.height / 4)))

        buffer = BytesIO()
        author_avatar.save(buffer, format="png")

        await platter.send_message("*🫳🧑 Squash*", files = [GoldyBot.File(buffer, "image.png")])

    async def uwuify(self, platter: GoldyBot.GoldPlatter):
        result = await uwuify_string(f"👋 Hello **{platter.author.name}**!", self.goldy)
        await platter.send_message(result)