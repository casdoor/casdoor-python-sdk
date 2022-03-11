try:
    from main import *
    from user import *

except ModuleNotFoundError or ImportError:
    from .main import *
    from .user import *
