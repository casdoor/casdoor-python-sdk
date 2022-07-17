try:
    from test_oauth import *

except ModuleNotFoundError or ImportError:
    from .test_oauth import *
