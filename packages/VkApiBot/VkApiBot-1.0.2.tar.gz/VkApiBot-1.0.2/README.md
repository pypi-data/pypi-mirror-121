# VkApiBot
____

**VkApiBot** - библиотека для легкого использования модуля vk_api

[https://vk.com/id559935246](Мой ВК)
___
## Существует три вида хендлеров:
___

#### message_handler_from_chat - возвращает данные полученные из бесед
    @bot.message_handler_from_chat()
    def on_message(data):
        peer_id = data.peer_id
        bot.api.messages.send(peer_id=peer_id, message="Вы написали мне из беседы", random_id=0)


#### message_handler_from_private - возвращает данные, полученные из ЛС сообщества
    @bot.message_handler_from_chat()
    def on_message(data):
        peer_id = data.peer_id
        bot.api.messages.send(peer_id=peer_id, message="Вы написали мне из ЛС сообщества", random_id=0)

#### message_event_handler - возвращает данные при взаимодействии с сообщением
    @bot.message_handler_from_chat()
    def on_message(data):
        bot.api.messages.sendMessageEventAnswer(
            event_id=data.event_id,
            user_id=event.user_id,
            peer_id=event.peer_id,
            event_data=json.dumps(event.payload),
        )
