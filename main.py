import random
import telebot
from telebot import types


TOKEN = '5658746455:AAGEU7qlSMRUsxHVwZ0YiQ6lz8tiKzGuDaw'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['new_chat_members'])
def new_member(message):
    welcome = {
        1: 'https://static.insales-cdn.com/images/products/1/7126/528366550/%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82__%D1%83%D1%80%D0%BE%D0%B4%D0%B5%D1%86.jpg',
        2: 'https://bonnycards.ru/images/privet/small/s-privet0054.jpg',
        3: 'https://i.yapx.cc/SLIDc.jpg',
        4: 'https://cdn.fotokartinki.ru/storage/posts/thumbs/otkrytka-privet-i-udacnogo-dnya-13203.jpg',
        5: 'https://i.pinimg.com/474x/c7/58/87/c75887b282c5e392e7dd4e52353b3c35.jpg'
    }
    bot.send_message(message.chat.id, f"@{message.new_chat_members[0].username}, приветсвую тебя! Как жизнь молодая?")
    i = random.randint(1, len(welcome))
    bot.send_photo(message.chat.id, welcome[i])


@bot.message_handler(commands=['make_admin'])
def make_admin(message):
    if message.reply_to_message:
        your_role = bot.get_chat_member(message.chat.id, message.from_user.id).status
        if your_role not in ['administrator', 'creator']:
            bot.send_message(message.chat.id, 'Ошибка. У вас недостаточно прав.')
            return
        his_role = bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).status
        if his_role in ['kicked', 'left']:
            bot.send_message(message.chat.id,
                             f'Ошибка. @{message.reply_to_message.from_user.username} вышел из чата или был забанен.')
            return
        elif his_role in ['administrator', 'creator']:
            bot.send_message(message.chat.id,
                             f'Ошибка. @{message.reply_to_message.from_user.username} и так является админиcтратором или владельцем.')
            return
        try:
            bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_delete_messages=True,
                                    can_manage_video_chats=True, can_restrict_members=True, can_promote_members=True,
                                    can_change_info=True, can_invite_users=True)
            bot.send_message(message.chat.id, f'Теперь @{message.reply_to_message.from_user.username} является админом')
            bot.send_photo(message.chat.id, 'https://mem-baza.ru/_ph/1/2/235069664.jpg?1600932446')
        except:
            bot.send_message(message.chat.id, 'Ошибка. У бота недостаточно прав.')
    else:
        bot.send_message(message.chat.id,
                         'Ошибка. Эта команда должна быть ответом на сообщение человека, которого вы хотите сделать админом')


@bot.message_handler(commands=['ban'])
def ban(message):
    if message.reply_to_message:
        your_role = bot.get_chat_member(message.chat.id, message.from_user.id).status
        his_role = bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).status
        if (your_role not in ['administrator', 'creator']) or (
                your_role == 'administrator' and his_role in ['administrator', 'creator']):
            bot.send_message(message.chat.id, 'Ошибка. У вас недостаточно прав.')
            return
        if his_role in ['kicked', 'left']:
            bot.send_message(message.chat.id,
                             f'Ошибка. @{message.reply_to_message.from_user.username} вышел из чата или был забанен.')
            return

        try:
            bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            bot.send_message(message.chat.id, f'@{message.reply_to_message.from_user.username} забанен.')
            bot.send_message(message.chat.id, 'https://www.youtube.com/watch?v=RKYeODIEk1s')
        except:
            bot.send_message(message.chat.id, 'Ошибка. У бота недостаточно прав.')
    else:
        bot.send_message(message.chat.id,
                         'Ошибка. Эта команда должна быть ответом на сообщение человека, которого вы хотите забанить')


@bot.message_handler(commands=['unban'])
def unban(message):
    if message.reply_to_message:
        your_role = bot.get_chat_member(message.chat.id, message.from_user.id).status
        his_role = bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).status
        if (your_role not in ['administrator', 'creator']) or (
                your_role == 'administrator' and his_role in ['administrator', 'creator']):
            bot.send_message(message.chat.id, 'Ошибка. У вас недостаточно прав.')
            return
        if his_role not in ['kicked', 'left']:
            bot.send_message(message.chat.id,
                             f'Ошибка. @{message.reply_to_message.from_user.username} находится в чате.')
            return

        try:
            bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            bot.send_message(message.chat.id, f'@{message.reply_to_message.from_user.username} разбанен.')
        except:
            bot.send_message(message.chat.id, 'Ошибка. У бота недостаточно прав.')
    else:
        bot.send_message(message.chat.id,
                         'Ошибка. Эта команда должна быть ответом на сообщение человека, которого вы хотите забанить.')


@bot.message_handler(commands=['stat'])
def stat(message):
    members = bot.get_chat_members_count(message.chat.id)
    admins = len(bot.get_chat_administrators(message.chat.id))
    ending1 = ''
    if (1 < members < 5):
        ending1 = 'а'
    elif (members >= 5):
        ending1 = 'ов'
    ending2 = ''
    if (1 < admins < 5):
        ending2 = 'а'
    elif (admins >= 5):
        ending2 = 'ов'
    bot.send_message(message.chat.id, f'{members} участник{ending1}')
    bot.send_message(message.chat.id, f'{admins} администратор{ending2}')


@bot.message_handler(commands=['leave'])
def leave(message):
    bot.leave_chat(message.chat.id)


@bot.message_handler(commands=['delete'])
def delete(message):
    if message.reply_to_message:
        your_role = bot.get_chat_member(message.chat.id, message.from_user.id).status
        his_role = bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).status
        if (your_role not in ['administrator', 'creator']) or (
                your_role == 'administrator' and his_role in ['administrator', 'creator']):
            bot.send_message(message.chat.id, 'Ошибка. У вас недостаточно прав.')
            return
        try:
            bot.delete_message(message.chat.id, message.reply_to_message.id)
        except:
            bot.send_message(message.chat.id, 'Ошибка. У бота недостаточно прав')
    else:
        bot.send_message(message.chat.id,
                         'Ошибка. Эта команда должна быть ответом на сообщение человека, которого вы хотите забанить.')


@bot.message_handler(commands=['all'])
def kek(message):
    bot.send_message(message.chat.id, bot.get_chat_members())


@bot.inline_handler(func=lambda query: True)
def text(query):
    make_admin = types.InlineQueryResultArticle(
        id='1',
        title='make admin',
        input_message_content=types.InputTextMessageContent(
            '/make_admin'
        )
    )
    ban = types.InlineQueryResultArticle(
        id='2',
        title='ban',
        input_message_content=types.InputTextMessageContent(
            '/ban'
        )
    )
    unban = types.InlineQueryResultArticle(
        id='3',
        title='unban',
        input_message_content=types.InputTextMessageContent(
            '/unban'
        )
    )
    stat = types.InlineQueryResultArticle(
        id='4',
        title='statistics',
        input_message_content=types.InputTextMessageContent(
            '/stat'
        )
    )
    leave = types.InlineQueryResultArticle(
        id='5',
        title='kick bot',
        input_message_content=types.InputTextMessageContent(
            '/leave'
        )
    )
    delete = types.InlineQueryResultArticle(
        id='6',
        title='delete message',
        input_message_content=types.InputTextMessageContent(
            '/delete'
        )
    )
    answer = []
    txt = query.query
    if txt in 'make admin':
        answer.append(make_admin)
    if txt in 'ban':
        answer.append(ban)
    if txt in 'unban':
        answer.append(unban)
    if txt in 'statistics':
        answer.append(stat)
    if txt in 'kick bot':
        answer.append(leave)
    if txt in 'delete message':
        answer.append(delete)
    if len(txt) == 0:
        answer = [make_admin, ban, unban, stat, leave, delete]
    bot.answer_inline_query(query.id, answer)


bot.polling(none_stop=True, interval=0)
