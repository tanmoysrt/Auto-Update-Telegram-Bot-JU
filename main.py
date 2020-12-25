import os

try:
    os.system('start cmd /k "python telegram_bot.py"')
    os.system('python continuous_checking.py')
except ImportError as e:
    print(f'All Required Libraries Not Found\n {e}')
