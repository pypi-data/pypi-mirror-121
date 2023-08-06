from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from retry import retry
from .utils.WorkerThread import WorkerThread

class VkApiBot:
	
	def __init__(self, token, group_id):
		self.token = token
		self.group_id = group_id
		self.handler_messages_from_private = []
		self.handler_messages_from_chat = []
		self.handler_message_events = []	
		
	def message_handler_from_chat(self):
		def decorator(handler):
			self.handler_messages_from_chat.append(handler)
			return handler
		return decorator
	
	def message_handler_from_private(self):
		def decorator(handler):
			self.handler_messages_from_private.append(handler)
			return handler
		return decorator
		
	def message_event_handler(self):
		def decorator(handler):
			self.handler_message_events.append(handler)
			return handler
		return decorator
	
	def login(self):
		self.group = VkApi(token=self.token)
		self.api = self.group.get_api()
		self.longpoll = VkBotLongPoll(self.group, self.group_id)
	
	@retry(delay=20)	
	def __get_updates(self):
		for event in self.longpoll.listen():
			self.__process_new_update(event)
	
	def __process_new_update(self, event):
		if event.type == VkBotEventType.MESSAGE_NEW:
			if event.message.peer_id > 2000000000:
				self.__process_new_message_from_chat(event.message)
			else:
				self.__process_new_message_from_private(event.message)
		if event.type == VkBotEventType.MESSAGE_EVENT:
			self.__process_new_message_event(event.object)

	def __process_new_message_from_chat(self, message):
		for handler in self.handler_messages_from_chat:
			self.__exec_task(handler, message)

		
	def __process_new_message_from_private(self, message):
		for handler in self.handler_messages_from_private:
			print(1)
			self.__exec_task(handler, message)


	def __process_new_message_event(self, message_event):
		for handler in self.handler_message_events:
			self.__exec_task(handler, message_event)
			
	def __exec_task(self, task, *args):
		WorkerThread(task, *args)
	
	def execute(arr):
		pass
	
	def polling(self):
		print(self.handler_message_events, self.handler_messages_from_private, self.handler_messages_from_chat)
		self.login()
		WorkerThread(self.__get_updates)