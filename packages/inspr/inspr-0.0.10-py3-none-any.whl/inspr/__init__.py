from .client import *
from .rest import *
from .models import *

from importlib_metadata import version
print(version('inspr'))

from .controller.controller_client import ControllerClient