print("Bot was started!")
def start(message):
    return (f"""Привет, {message.from_user.first_name}! Я помогу тебе найти тиммейта на одну катку или друзей для любой игры. Выбери интересующий тебя пункт.""")

help = """Все команды с их описанием приведены ниже.

/start - начало работы с ботом.

/createanc - создание анкеты для поиска тиммейтов
/editanc - редактирование Вашей анкеты.
/myanc - просмотреть Вашу анкету.

/rules - правила данного бота. Обязательно к прочтению!!!
/search - начать поиск тиммейтов. 
/help - помощь.

/donate - поддержка меня.
"""

rules = """
1. Указывайте только корректные данные! 
2. Старайтесь уважительно относиться к каждому из тиммейтов.
3. Если с вами связались, отвечайте в максимально короткий срок.
4. Старайтесь не употреблять ненорматиыные слова и фразы, которые могут обидеть других пользователей.
5. Не портьте игру другим игрокам, которые вас пригласили играть.
6. Запрещено оставлять ссылки на другие сайты, в описании или в "связь" для исключения фишинговых ссылок. 
7. Запрещено спамить жалобами! Отправляйте жалобы только в случае нарушения! 

В случае нарушения правил, в лучшем случае, ваша анкета будет удаленна, в худшем - получите бан навсегда без возможности разблокировки!

Также, не стоит забывать про мошенников, которые могут попробоавть развести вас на деньги или аккаунт. Если вы заметили подозрительную анкету, отправьте жалобу на этот аккаунт и, в случае обнаружения нарушений, анкета будет удалена!"""

donate = """Если вы хотите меня поддержать копейкой, вы можете сделать это по следующим ссылкам:
1. https://www.donationalerts.com/r/zemph1x - DonationAlerts

2. 40817810606001216169 - СберБанк"""