"""Cere-MEG-Bellum (CMB)"""

import os as _os

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
#   X.Y
#   X.Y.Z   # For bugfix releases
#
# Admissible pre-release markers:
#   X.YaN   # Alpha release
#   X.YbN   # Beta release
#   X.YrcN  # Release Candidate
#   X.Y     # Final release
#
# Dev branch marker is: 'X.Y.devN' where N is an integer.
#

from ._version import __version__

# Default data directory: <package_dir>/ (atlas data goes into data/, nnUNet/, etc.)
CMB_DATA_DIR = _os.path.join(_os.path.dirname(__file__), '')

from .functions import (get_cerebellum_data)
from .source_space import (setup_full_source_space)
from .visualization import (plot_cerebellum_data)

from .utils import is_float