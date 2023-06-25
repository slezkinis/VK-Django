from django.core.management.base import BaseCommand
from datacenter.models import *
from project.settings import BOT_TOKEN
import asyncio
from pprint import pprint
from django.utils import timezone
class Command(BaseCommand):
    help = 'bot'


    def handle(self, *args, **options):
        print('Start')
        bot1()


def bot1():
    import os
    from vkbottle import GroupEventType, GroupTypes, Keyboard, Text, VKAPIError
    from vkbottle.bot import Bot, Message
    from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink, Callback
    from vkbottle.tools import DocMessagesUploader
    from logging import disable, WARN, CRITICAL
    import json
    import asyncio

    disable(level=WARN)

    bot_token = BOT_TOKEN
    vk = Bot(bot_token)
    # ADMIN_ID = int(os.getenv('ADMIN_ID'))


    @vk.on.private_message(text=['Начать'])
    @vk.on.private_message(payload={'cmd': 'menu'})
    async def start(message: Message):
        loop = asyncio.get_running_loop()
        all_users = await loop.run_in_executor(None, lambda: [i.vk_id for i in Vk_user.objects.all()])
        if message.from_id not in all_users:
            users_info = await vk.api.users.get(message.from_id)
            await loop.run_in_executor(None, lambda name, last, id: Vk_user.objects.create(name=f'{name} {last}', vk_id=id), users_info[0].first_name, users_info[0].last_name, message.from_id)
    #         db.add_user((message.from_id, ''))
    #     keyboard = Keyboard()
    #     keyboard.add(Text('🛒 Товары'), color=KeyboardButtonColor.PRIMARY)
    #     keyboard.add(Text('📱 Профиль'))
    #     keyboard.row()
    #     keyboard.add(Text('🛍️ Корзина'), color=KeyboardButtonColor.POSITIVE)
    #     await message.answer(
    #         message = 'Привет! Добро пожаловать в онлайн магазин',
    #         keyboard = (
    #         keyboard
    #         )
    #     )

    # @vk.on.private_message(text='🛒 Товары')
    # async def products(message: Message):
    #     products = db.get_all_sections()
    #     keyboard = Keyboard(one_time = False, inline = True)
    #     for product in products:
    #         keyboard.add(Callback(product[0], payload={'cmd': product[1]}))
    #     keyboard.add(Text('Назад 🔙', payload={'cmd': 'menu'}))
    #     await message.answer(
    #         message=f'Вот доступные категории:)',
    #         keyboard=(keyboard)
    #     )


    # @vk.on.private_message(text='⚙️ Настройка магазина')
    # async def settings(message: Message):
    #     global admin
    #     admin = True
    #     sections = db.get_all_sections()
    #     keyboard = Keyboard(inline=True)
    #     keyboard.add(Callback('✏️ Добавить новую категорию', payload={'cmd': 'add_new_section'}))
    #     keyboard.row()
    #     for section in sections:
    #         keyboard.add(Callback(section[0], payload={'cmd': f'set-adm_{section[1]}'}))
    #     keyboard.row()
    #     keyboard.add(Callback('🚫 Закрыть', payload={'cmd': 'close'}))
    #     await message.answer('Это настройка магазина! Вот все категории', keyboard=keyboard)


    # @vk.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
    # async def message_event_handLer(event: GroupTypes.MessageEvent):
    #     global admin, add_section_val, add_new, product1, section1, need_delete
    #     await vk.api.messages.delete(peer_id=event.object.peer_id, message_ids=event.object.conversation_message_id, delete_for_all=True, group_id=event.group_id)
    #     if event.object.payload['cmd'] == 'close':
    #         a = 1
    #     elif event.object.payload['cmd'] == 'cancel':
    #         admin = False
    #         add_section_val = False
    #         product1 = []
    #         add_new = ''
    #         section1 = ''
    #         print(need_delete[::len(need_delete) - 1])
    #         for i in need_delete[::len(need_delete) - 1]:
    #             await vk.api.messages.delete(peer_id=event.object.peer_id, message_ids=i, delete_for_all=True, group_id=event.group_id)
    #         need_delete = []
    #         # admin = True
    #         # sections = db.get_all_sections()
    #         # keyboard = Keyboard(inline=True)
    #         # keyboard.add(Callback('✏️ Добавить новую категорию', payload={'cmd': 'add_new_section'}))
    #         # keyboard.row()
    #         # for section in sections:
    #         #     keyboard.add(Callback(section[0], payload={'cmd': f'set-adm_{section[1]}'}))
    #         # keyboard.row()
    #         # keyboard.add(Callback('🚫 Закрыть', payload={'cmd': 'cancel'}))
    #         # await vk.api.messages.send(
    #         #     user_id=event.object.user_id,
    #         #     random_id=0,
    #         #     peer_id=event.object.peer_id,
    #         #     message='Это настройка магазина! Вот все категории',
    #         #     keyboard=keyboard
    #         # )
    #     elif event.object.payload['cmd'] == 'to_adm':
    #         admin = True
    #         sections = db.get_all_sections()
    #         keyboard = Keyboard(inline=True)
    #         keyboard.add(Callback('✏️ Добавить новую категорию', payload={'cmd': 'add_new_section'}))
    #         keyboard.row()
    #         for section in sections:
    #             keyboard.add(Callback(section[0], payload={'cmd': f'set-adm_{section[1]}'}))
    #         keyboard.row()
    #         keyboard.add(Callback('🚫 Закрыть', payload={'cmd': 'cancel'}))
    #         await vk.api.messages.send(
    #             user_id=event.object.user_id,
    #             random_id=0,
    #             peer_id=event.object.peer_id,
    #             message='Это настройка магазина! Вот все категории',
    #             keyboard=keyboard
    #         )
    #     elif event.object.payload['cmd'] == 'add_new_section':
    #         add_section_val, admin = True, True
    #         await vk.api.messages.send(
    #             user_id=event.object.user_id,
    #             random_id=0,
    #             peer_id=event.object.peer_id,
    #             message='Введите название для новой категории:'
    #         )
    #     elif 'set-adm_' in event.object.payload['cmd']:
    #         section_id = int(event.object.payload['cmd'].replace('set-adm_', ''))
    #         products = db.get_products_section(section_id)
    #         keyboard = Keyboard(inline=True)
    #         keyboard.add(Callback('🗑️ Удалить эту категорию', payload={'cmd': f'category_remove_{section_id}'}), color=KeyboardButtonColor.NEGATIVE)
    #         keyboard.row()
    #         keyboard.add(Callback('➕ Добавить товар в эту категорию', payload={'cmd': f'create_product_{section_id}'}))
    #         # if products:
    #         keyboard.row()
    #         section = db.get_section(section_id)
    #         for product in products:
    #             keyboard.add(Callback(product[0], payload={'cmd': f'product_remove_{product[1]}'}))
    #         if products:
    #             keyboard.row()
    #         keyboard.add(Callback('⚙️ Вернуться к редактированию', payload={'cmd': 'to_adm'}))
    #         await vk.api.messages.send(
    #             user_id=event.object.user_id,
    #             random_id=0,
    #             peer_id=event.object.peer_id,
    #             message=f'Это все товары из категории "{section[0]}". Нажмите на товар, чтобы его удалить!',
    #             keyboard=keyboard
    #         )
    #     elif 'create_product_' in event.object.payload['cmd']:
    #         keyboard = Keyboard(inline=True)
    #         keyboard.add(Callback('🚫 Отменить', payload={'cmd': 'cancel'}))
    #         add_new = f'Название'
    #         need_delete.append(event.object.conversation_message_id)
    #         section1 = event.object.payload["cmd"].replace("create_product_", "")
    #         await vk.api.messages.send(
    #             user_id=event.object.user_id,
    #             random_id=0,
    #             peer_id=event.object.peer_id,
    #             message=f'Введите название для нового товара',
    #             keyboard=keyboard
    #         )
    #     # await vk.api.messages.send_message_event_answer(
    #     #     event_id=event.object.event_id,
    #     #     peer_id=event.object.peer_id,
    #     #     user_id=event.object.user_id,
    #     #     event_data=json.dumps({'type': 'show_snackbar', 'text': 'text'})
    #     # )
    # @vk.on.private_message()
    # async def new_section(message: Message):
    #     global admin, add_section_val, add_new, product1, section1, need_delete
    #     if message.from_id == ADMIN_ID:
    #         if add_section_val:
    #             need_delete.append(message.conversation_message_id)
    #             admin = False
    #             add_section_val = False
    #             product1 = []
    #             add_new = ''
    #             section1 = ''
    #             db.create_section(message.text)
    #             keyboard = Keyboard(inline=True)
    #             keyboard.add(Callback('🚫 Закрыть', payload={'cmd': 'close'}))
    #             await message.answer(f'Создана новая категория с названием "{message.text}"', keyboard=keyboard)
    #         elif add_new == 'Название':
    #             need_delete.append(message.conversation_message_id)
    #             product1.append(message.text)
    #             keyboard = Keyboard(inline=True)
    #             keyboard.add(Callback('🚫 Отменить', payload={'cmd': 'cancel'}))
    #             add_new = 'Описание'
    #             await message.answer(f'Введите описание: ', keyboard=keyboard)
    #         elif add_new == 'Описание':
    #             need_delete.append(message.conversation_message_id)
    #             product1.append(message.text)
    #             keyboard = Keyboard(inline=True)
    #             keyboard.add(Callback('🚫 Отменить', payload={'cmd': 'cancel'}))
    #             add_new = 'Ссылка'
    #             await message.answer(f'Введите ссылку на товар: ', keyboard=keyboard)
    #         elif add_new == 'Ссылка':
    #             need_delete.append(message.conversation_message_id)
    #             product1.append(message.text)
    #             keyboard = Keyboard(inline=True)
    #             keyboard.add(Callback('🚫 Отменить', payload={'cmd': 'cancel'}))
    #             add_new = 'Цена'
    #             await message.answer(f'Введите цену: ', keyboard=keyboard)
    #         elif add_new == 'Цена':
    #             need_delete.append(message.conversation_message_id)
    #             keyboard = Keyboard(inline=True)
    #             keyboard.add(Callback('🚫 Отменить', payload={'cmd': 'cancel'}))
    #             if message.text.isdigit():
    #                 product1.append(int(message.text))
    #                 add_new = 'Картинка'
    #                 await message.answer(f'Отправьте картинку для товара: ', keyboard=keyboard)
    #             else:
    #                 await message.answer(f'Укажите правильную цену! {message.text} - это не число', keyboard=keyboard)
    # # Толик видиорегистратор система мене
    vk.run_forever()