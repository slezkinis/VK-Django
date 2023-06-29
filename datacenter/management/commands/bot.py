from django.core.management.base import BaseCommand
from datacenter.models import *
from project.settings import BOT_TOKEN, ADMIN_ID
import asyncio
import phonenumbers
from pprint import pprint


class Command(BaseCommand):
    help = 'bot'


    def handle(self, *args, **options):
        print('Start')
        bot1()
need_register = []


def bot1():
    import os
    from vkbottle import GroupEventType, GroupTypes, Keyboard, Text, VKPayEvent
    from vkbottle.bot import Bot, Message
    from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink, Callback, VKPay
    from vkbottle import PhotoMessageUploader
    from vkbottle.tools import DocMessagesUploader
    from logging import disable, WARN, CRITICAL
    import json
    import asyncio

    disable(level=CRITICAL)
    bot_token = BOT_TOKEN
    vk = Bot(bot_token)
    photo_uploader = PhotoMessageUploader(vk.api)


    def get_user(u):
        user = Vk_user.objects.get(vk_id=u)
        return {
            'name': user.name,
            'id': user.vk_id,
            'num_boughts': user.orders.count(),
            'phone': user.phonenumber
        }
    def get_keyboard_categories():
        keyboard = Keyboard(one_time = False, inline = True)
        for product in ProductCategory.objects.all():
            keyboard.add(Callback(product.title, payload={'cmd': f'category_{product.id}'}))
        keyboard.row()
        keyboard.add(Callback('🚫 Закрыть', payload={'cmd': 'close'}))
        return keyboard


    def update_phone(u, phone):
        user = Vk_user.objects.get(vk_id=u)
        user.phonenumber = phone
        user.save()
    def get_user_cart(user):
        cart = Vk_user.objects.get(vk_id=user).cart
        if cart is None:
            return []
        else:
            return [int(i) for i in cart.split('; ')]


    def create_order(u, products):
        user = Vk_user.objects.get(vk_id=u)
        order = Order.objects.create(
            user=user,
        )
        for i in products:
            product = Product.objects.get(id=i)
            order_el = OrderElements.objects.create(
                order=order,
                product=product,
                quantity=1,
                price=product.price
            )
    def update_uder(user, cart):
        u = Vk_user.objects.get(vk_id=user)
        if cart is None:
            u.cart = None
        else:
            u.cart = '; '.join(cart)
        u.save()
    

    def get_user_orders(u):
        user = Vk_user.objects.get(vk_id=u)
        otv = []
        for order in user.orders.all():
            all_status = {
                'first': 'В обработке',
                'second': 'В пути',
                'third': 'Доставлен',
                'canceled': 'Отменён'
            }
            order_data = {
                'status': all_status[order.status],
                'address': order.address,
                'created_at': order.created_at,
                'delivered_at': order.delivered_at,
                'products': [{'name': i.product.title, 'quantity': i.quantity, 'price': int(i.price)} for i in order.products.all()]
            }
            otv.append(order_data)
        return otv


    def get_keyboard_products(category):
        keyboard = Keyboard(one_time = False, inline = True)
        for product in Product.objects.filter(category=category):
            keyboard.add(Callback(product.title, payload={'cmd': f'product_{product.id}'}))
        keyboard.row()
        keyboard.add(Callback('Домой', payload={'cmd': 'menu'}))
        return (keyboard, ProductCategory.objects.get(id=category).title)

    def get_product(product):
        product_1 = Product.objects.get(id=product)
        return {
            'id': product_1.id,
            'title': product_1.title,
            'description': product_1.description,
            'image': product_1.image.path,
            'price': int(product_1.price),
            'category': product_1.category.id
        }
            # need_register.append(message.from_id)
            # await message.answer(
            #     message = 'Привет! Введите свой номер телефона. В дальнейшем эти данные будут использоваться для связи с Вами:) Формат ввода номера телефона: +7 000 000 00 00',
            # )
    @vk.on.private_message(text=['Начать'])
    @vk.on.private_message(payload={'cmd': 'start'})
    async def start(message: Message):
        global need_register
        loop = asyncio.get_running_loop()
        all_users = await loop.run_in_executor(None, lambda: [i.vk_id for i in Vk_user.objects.all()])
        if message.from_id not in all_users:
            # users_info = await vk.api.users.get(message.from_id)
            # await loop.run_in_executor(None, lambda name, last, id: Vk_user.objects.create(name=f'{name} {last}', vk_id=id), users_info[0].first_name, users_info[0].last_name, message.from_id)
            loop = asyncio.get_running_loop()
            users_info = await vk.api.users.get(message.from_id)
            loop.run_in_executor(None, lambda name, last, id, phone: Vk_user.objects.create(name=f'{name} {last}', vk_id=id, phonenumber=phone), users_info[0].first_name, users_info[0].last_name, message.from_id, None)
        keyboard = Keyboard()
        keyboard.add(Text('🛒 Товары'), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text('📱 Профиль'))
        keyboard.row()
        keyboard.add(Text('🛍️ Корзина'), color=KeyboardButtonColor.POSITIVE)
        await message.answer(
            message = 'Привет! Добро пожаловать в онлайн магазин',
            keyboard = (
            keyboard
            )
        )

    @vk.on.private_message(text='🛒 Товары')
    # @vk.on.private_message(payload={'cmd': 'menu'})
    async def products(message: Message):
        loop = asyncio.get_running_loop()
        keyboard = await loop.run_in_executor(None, get_keyboard_categories)
        await message.answer(
            message=f'Вот доступные категории:)',
            keyboard=(keyboard)
        )



    @vk.on.private_message(text='🛍️ Корзина')
    async def cart(message: Message):
        loop = asyncio.get_running_loop()
        user_cart = await loop.run_in_executor(None, get_user_cart, message.from_id)
        products = []
        keyboard = Keyboard(inline=True)
        for num, i in enumerate(user_cart[::-1], 1):
            product = await loop.run_in_executor(None, get_product, i)
            text = f'{num}. {product["title"]} | {product["price"]} руб.'
            products.append(text)
            keyboard.add(Callback(num, payload={'cmd': f'remove_{product["id"]}'}), color=KeyboardButtonColor.NEGATIVE)
        if products:
            keyboard.row()
            keyboard.add(Callback('Оплатить', payload={'cmd': 'pay'}), color=KeyboardButtonColor.POSITIVE)
            keyboard.row()
        keyboard.add(Callback('🚫 Закрыть', payload={'cmd': 'close'}))
        otv = "\n".join(products)
        if products:
            await message.answer(
                f'Эти товары у Вас в корзине: \n{otv}\nНажмите кнопку с цифрой товара, чтобы удалить его из корзины!',
                keyboard=keyboard
            )
        else:
            await message.answer(
                f'Ваша корзина пуста:(',
                keyboard=keyboard
            )
        
    

    @vk.on.private_message(text='📱 Профиль')
    async def profile(message: Message):
        loop = asyncio.get_running_loop()
        user = await loop.run_in_executor(None, get_user, message.from_id)
        text = f'🙍‍♂ Пользователь: {user["name"]}\n🆔 ID: {user["id"]}\n📞 Номер телефона: {user["phone"]}\n------------------\n🛒 Количество заказов: {user["num_boughts"]} шт.'
        keyboard = Keyboard(inline=True)
        keyboard.add(Callback('Ваши заказы', payload={'cmd': 'orders'}))
        keyboard.add(Callback('🚫 Закрыть', payload={'cmd': 'close'}))
        await message.answer(
            text,
            keyboard=keyboard
        )
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

    @vk.on.private_message(payload={'pays': 0})
    async def people_was_pay(message:Message):
        print(1)
        await message.answer(f'Вы успешно оплатили подписку в размере {message.attachments[0].amount} рублей!')




    @vk.on.payment(VKPayEvent)
    async def handle_payment(event: VKPayEvent):
        # Обработка платежа
        print(1)

    @vk.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
    async def message_event_handLer(event: GroupTypes.MessageEvent):
        loop = asyncio.get_running_loop()
        mes = await vk.api.messages.get_history(user_id=event.object.user_id, count=2, offset=0)
        # count = vk.api.messages.get_history(user_id=event.object.user_id)['count']
        await vk.api.messages.delete(peer_id=event.object.peer_id, message_ids=mes.items[0].id, delete_for_all=True, group_id=event.object.user_id)
        if event.object.payload['cmd'] == 'close':
            return
        elif event.object.payload['cmd'] == 'pay':
            user = await loop.run_in_executor(None, get_user, event.object.user_id)
            if not user['phone']:
                need_register.append(event.object.user_id)
                await vk.api.messages.send(
                    user_id=event.object.user_id,
                    random_id=0,
                    peer_id=event.object.peer_id,
                    message = 'Привет! Введите свой номер телефона. В дальнейшем эти данные будут использоваться для связи с Вами:) Формат ввода номера телефона: +7 000 000 00 00',
                )
                return
            loop = asyncio.get_running_loop()
            cart = await loop.run_in_executor(None, get_user_cart, event.object.user_id)
            products2 = []
            keyboard = Keyboard(inline=True)
            price = 0
            for i in cart:
                product = await loop.run_in_executor(None, get_product, int(i))
                products2.append(product['id'])
                price += product['price']
            products2 = [str(i) for i in products2]
            keyboard.add(VKPay(payload={'products': '; '.join(products2)}, hash=f'action=pay-to-group&amount={price}&group_id={221254486}'))
            keyboard.row()
            keyboard.add(Callback('🚫 Отменить', payload={'cmd': 'close'}))
            await vk.api.messages.send(
                user_id=event.object.user_id,
                random_id=0,
                peer_id=event.object.peer_id,
                message=f'С Вас {price} руб. После оплаты с Вами свяжутся по номеру телефона: {user["phone"]}',
                keyboard=keyboard
            )
                
            # await loop.run_in_executor(None, create_order, event.object.user_id, products2)
            # await loop.run_in_executor(None, update_uder, event.object.user_id, None)
            # await vk.api.messages.send(
            #     user_id=event.object.user_id,
            #     random_id=0,
            #     peer_id=event.object.peer_id,
            #     message='Ваш заказ принят! Вам перезвонят по указанному в профиле номеру для уточнение дополнительной информации! Спасибо, что выбрали нас:)',
            #     keyboard=keyboard
            # )
        elif 'remove_' in event.object.payload['cmd']:
            keyboard = Keyboard(inline=True)
            keyboard.add(Callback('🚫 Закрыть', payload={'cmd': 'close'}))
            loop = asyncio.get_running_loop()
            product = await loop.run_in_executor(None, get_product, event.object.payload["cmd"].replace("remove_", ""))
            cart = await loop.run_in_executor(None, get_user_cart, event.object.user_id)
            if '' in cart:
                cart.remove('')
            # print(event.object.user_id in all_users)
            cart = [str(i) for i in cart]
            if len(cart) == 1:
                cart = None
            else:
                cart.remove(event.object.payload["cmd"].replace("remove_", ""))
            await loop.run_in_executor(None, update_uder, event.object.user_id, cart)
            await vk.api.messages.send(
                user_id=event.object.user_id,
                random_id=0,
                peer_id=event.object.peer_id,
                message=f'Товар {product["title"]} удалён из корзины',
                keyboard=keyboard
            )
        elif event.object.payload['cmd'] == 'start1':
            keyboard = Keyboard()
            keyboard.add(Text('🛒 Товары'), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text('📱 Профиль'))
            keyboard.row()
            keyboard.add(Text('🛍️ Корзина'), color=KeyboardButtonColor.POSITIVE)
            await vk.api.messages.send(
                user_id=event.object.user_id,
                random_id=0,
                peer_id=event.object.peer_id,
                message = 'Привет! Добро пожаловать в онлайн магазин',
                keyboard = (
                keyboard
                )
            )
        elif 'category_' in event.object.payload['cmd']:
            loop = asyncio.get_running_loop()
            keyboard, category = await loop.run_in_executor(None, get_keyboard_products, event.object.payload["cmd"].replace("category_", ""))
            await vk.api.messages.send(
                user_id=event.object.user_id,
                random_id=0,
                peer_id=event.object.peer_id,
                message=f'Это товары из категории "{category}"',
                keyboard=keyboard
            )
        elif event.object.payload['cmd'] == 'menu':
            loop = asyncio.get_running_loop()
            keyboard = await loop.run_in_executor(None, get_keyboard_categories)
            await vk.api.messages.send(
                user_id=event.object.user_id,
                random_id=0,
                peer_id=event.object.peer_id,
                message=f'Вот доступные категории:)',
                keyboard=keyboard
            )
        elif 'product_' in event.object.payload['cmd']:
            loop = asyncio.get_running_loop()
            product = await loop.run_in_executor(None, get_product, event.object.payload["cmd"].replace("product_", ""))
            photo = await photo_uploader.upload(
                file_source=product['image'],
                peer_id=event.object.peer_id,
            )
            keyboard = Keyboard(one_time = False, inline = True)
            keyboard.add(Callback('Добавить в корзину 🛍️', payload={'cmd': f'add_to_cart_{product["id"]}'}), color=KeyboardButtonColor.POSITIVE)
            keyboard.row()
            keyboard.add(Callback("Назад к категории 🔙", payload={'cmd': f'category_{product["category"]}'}))
            await vk.api.messages.send(
                user_id=event.object.user_id,
                random_id=0,
                peer_id=event.object.peer_id,
                message=f"Название: {product['title']}\nОписание: {product['description']}\nЦена: {product['price']} руб",
                attachment=photo,
                keyboard=keyboard
            )
        elif 'add_to_cart_' in event.object.payload['cmd']:
            loop = asyncio.get_running_loop()
            product = await loop.run_in_executor(None, get_product, event.object.payload["cmd"].replace("add_to_cart_", ""))
            cart = await loop.run_in_executor(None, get_user_cart, event.object.user_id)
            if '' in cart:
                cart.remove('')
            # print(event.object.user_id in all_users)
            # print(cart)
            cart = [str(i) for i in cart]
            cart.append(str(event.object.payload["cmd"].replace("add_to_cart_", "")))
            await loop.run_in_executor(None, update_uder, event.object.user_id, cart)
            keyboard = Keyboard(one_time = False, inline = True)
            keyboard.add(Callback("Назад к категории 🔙", payload={'cmd': f'category_{product["category"]}'}))
            await vk.api.messages.send(
                user_id=event.object.user_id,
                random_id=0,
                peer_id=event.object.peer_id,
                message=f'Товар {product["title"]} добавлен в корзину',
                keyboard=keyboard
            )
        elif event.object.payload['cmd'] == 'orders':
            loop = asyncio.get_running_loop()
            orders = await loop.run_in_executor(None, get_user_orders, event.object.user_id)
            keyboard = Keyboard(one_time = False, inline = True)
            keyboard.add(Callback('🚫 Закрыть', payload={'cmd': 'close'}))
            otv = []
            if orders:
                for num, i in enumerate(orders, start=1):
                    products = ';\n\n'.join([f'Название: {j["name"]},\n      Цена: {j["price"]} руб.' for j in i['products']])
                    text = f"{num}. Статус: {i['status']},\nКол-во товаров: {len(i['products'])},\n   Товары:\n      {products}"
                    otv.append(text)
                await vk.api.messages.send(
                    user_id=event.object.user_id,
                    random_id=0,
                    peer_id=event.object.peer_id,
                    message='\n'.join(otv),
                    keyboard=keyboard
                )
            else:
                await vk.api.messages.send(
                    user_id=event.object.user_id,
                    random_id=0,
                    peer_id=event.object.peer_id,
                    message=f'Вы ничего не заказывали',
                    keyboard=keyboard
                )

    @vk.on.private_message()
    async def update(message: Message):
        global need_register
        if message.from_id in need_register:
            parsed_number = phonenumbers.parse(message.text, 'RU')
            if phonenumbers.is_valid_number(parsed_number):
                loop = asyncio.get_running_loop()
                users_info = await vk.api.users.get(message.from_id)
                loop.run_in_executor(None, update_phone, message.from_id, message.text)
                keyboard = Keyboard(inline=True)
                keyboard.add(Callback('🏚️ На главную', payload={'cmd': 'start1'}), color=KeyboardButtonColor.POSITIVE)
                need_register.remove(message.from_id)
                await message.answer(
                    message = 'Спасибо:) Теперь можете спокойно оплачивать:)',
                    keyboard = (
                    keyboard
                    )
                )
                return
            else:
                await message.answer(
                    message = 'Проверьте правильность ввода номера телефона'
                )
            
    # # Толик видиорегистратор система мене
    vk.run_forever()