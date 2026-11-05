from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.message.components import BaseMessageComponent, ComponentType
import astrbot.api.message_components as Comp
from pyAPart import convert_asciiart
from astrbot.core.utils.astrbot_path import get_astrbot_data_path
import time
from pathlib import Path
import os

@register("asciiart", "swl", "将图片转成ascii字符画", "0.1.0")
class AsciiArt(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.save_dir = (Path(get_astrbot_data_path()) / "plugin_data" / self.name)
        if not os.path.exists(self.save_dir):
            # 如果目录不存在，则创建它
            os.makedirs(self.save_dir)
        

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        pass

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("asciiart", alias=["字符画", "asciiart"], description="将图片转为ascii字符画")
    async def convert2asciiart(self, event: AstrMessageEvent):
        """该插件可以将图片转为ascii字符画"""
        user_name = event.get_sender_name()
        message: list[BaseMessageComponent] = event.get_messages()
        images = [msg for msg in message if msg.type == ComponentType.Image]
        chain = [Comp.At(qq=event.get_sender_id()),]
        for image in images:
            img = convert_asciiart(image.url, colorful=False)
            
            img.save(f"{self.save_dir}/{time.localtime}.png")
            chain.append(Comp.Image.fromFileSystem(img))
            
        yield event.chain_result(chain)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        pass