from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.message.components import BaseMessageComponent, ComponentType
import astrbot.api.message_components as Comp
from pyAPart import convert_asciiart


@register("asciiart", "swl", "将图片转成ascii字符画的差距", "0.1.0")
class AsciiArt(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.save_dir = "./ascii_art/"

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        pass

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("asciiart", alias=["字符画", "asciiart"], description="将图片转为ascii字符画")
    async def convert2asciiart(self, event: AstrMessageEvent):
        """将图片转为ascii字符画"""
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages()
        message: list[BaseMessageComponent] = event.get_messages()
        images = [msg for msg in message if msg.type == ComponentType.Image]
        chain = [Comp.At(qq=event.get_sender_id()),]
        for image in images:
            img = convert_asciiart(image.url, colorful=False)
            img.save(f"{self.save_dir}{user_name}_{image.id}.png")
            chain.append(Comp.Image.fromFileSystem(img))
            
        yield event.chain_result(chain)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        pass