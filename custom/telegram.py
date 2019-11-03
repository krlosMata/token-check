import telegram
from telegram.ext import Updater, CommandHandler

class Ctelegram:
  def __init__(self, _token, _chatId):
    self.chatId = _chatId  
    self.bot = telegram.Bot(_token) 

  def sendMessage(self, message):
    self.bot.send_message(self.chatId, message)