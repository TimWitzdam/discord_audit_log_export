import inspect
from datetime import datetime


def debug(argument):
    cf = inspect.currentframe()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f'{current_time} - {cf.f_back.f_lineno}: {argument}')
