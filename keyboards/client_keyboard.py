from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

markup.add(('Show all passwords 📋'), 'Add new password 🔏')