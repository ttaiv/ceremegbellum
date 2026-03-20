# Cere-MEG-Bellum (CMB)

[![PyPI](https://badge.fury.io/py/cmb.svg?label=PyPI%20downloads)](https://pypi.org/project/cmb/)
[![CI](https://github.com/johnsam7/ceremegbellum/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/johnsam7/ceremegbellum/actions/workflows/ci.yml)

CMB is a Python package for **automatic cerebellar cortical surface reconstruction from standard MRI** and **MEG/EEG source space computation including the cerebellum**.

For more information about the method, please see:

> Samuelsson, J. G., J. D.Schmahmann, M. I.Sereno, B.Rosen, and M. S.Hämäläinen. 2026. “A Digital Anatomical Atlas of the Human Cerebellum at Subfolial Resolution.” Human Brain Mapping47, no. 4: e70497. https://doi.org/10.1002/hbm.70497.

## Features

- Automatic segmentation of cerebellar lobules using a trained nnU-Net model
- Diffeomorphic registration (ANTs SyNCC) of a high-resolution cerebellar template to subject anatomy
- Construction of cerebellar cortical source spaces compatible with MNE-Python
- Visualization of cerebellar data in normal, inflated, and flatmap views

## Requirements

- Python >= 3.10
- [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/) (for MRI conversion and recon-all)
- [nnU-Net](https://github.com/MIC-DKFZ/nnUNet) (installed automatically as a dependency)

## Installation

### Standard Installation

On most systems with a modern toolchain (GCC >= 9.3), install the latest stable version from PyPI:

```bash
pip install -U cmb
```

Or install from source for development:

```bash
git clone https://github.com/johnsam7/ceremegbellum.git
cd ceremegbellum
pip install -e .
```

### Installation on Systems with Older Toolchains

Some institutional clusters (e.g., CentOS 7 / RHEL 7) ship with GCC < 9.3 and cannot compile packages like NumPy or SciPy from source. If `pip install` fails with **"NumPy requires GCC >= 9.3"**, use the following approach:

1. **Get a supported Python version.** If conda is available, create a new environment. Otherwise, download a standalone build from [python-build-standalone](https://github.com/astral-sh/python-build-standalone/releases) and create a venv:

   ```bash
   # Example: extract standalone Python 3.12
   tar xzf cpython-3.12*-x86_64-unknown-linux-gnu-install_only.tar.gz
   /path/to/python/bin/python3.12 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   ```

2. **Install compiled dependencies as pre-built wheels:**

   ```bash
   pip install --only-binary :all: \
       numpy scipy pandas matplotlib torch antspyx statsmodels \
       scikit-image scikit-learn imagecodecs numexpr blosc2 \
       pyyaml Pillow
   ```

3. **Install source-only packages (pure Python, no compiler needed):**

   ```bash
   pip install --no-deps nnunetv2 acvl-utils dynamic-network-architectures \
       batchgenerators batchgeneratorsv2 ndindex
   ```

4. **Install CMB and remaining dependencies:**

   ```bash
   pip install --only-binary :all: mne nibabel plyfile pooch webcolors
   pip install --no-deps -e .
   ```

5. **Verify the installation:**

   ```bash
   python -c "import cmb; print(cmb.__version__)"
   ```

## Quick Start

```python
import mne
import pickle
import os.path as op
from cmb import get_cerebellum_data, setup_full_source_space, plot_cerebellum_data, CMB_DATA_DIR

subjects_dir = '/path/to/freesurfer/subjects/'
subject = 'your_subject'

# Download atlas data and trained segmentation models (first time only)
get_cerebellum_data()

# Load cerebellum geometry
cb_data = pickle.load(open(op.join(CMB_DATA_DIR, 'data', 'cerebellum_geo'), 'rb'))

# Set up combined cortical + cerebellar source space
src_whole = setup_full_source_space(subject, subjects_dir,
                                    cerb_subsampling='dense', spacing='oct6')

# ... compute forward/inverse solutions with MNE as usual ...

# Visualize cerebellar data on a flatmap
plot_cerebellum_data(data, fwd['src'], src_whole, cb_data,
                     view='flatmap', sub_sampling='dense')
```

See [`examples/example_script.py`](examples/example_script.py) for a complete end-to-end example using the MNE sample dataset.

## Docker

A Docker image is provided with FreeSurfer 7.4.1 and GPU support (NVIDIA PyTorch base image).

**Prerequisites:** Place a FreeSurfer `license.txt` file in the repository root.

```bash
# Build the image
docker build -t mne-tools/cmb:v0.1.0 .

# Run with mounted data directories
docker run -ti \
  -v /path/to/subjects:/workspace/subjects \
  -v /path/to/nnUNet:/workspace/nnUNet \
  --name CMB mne-tools/cmb:v0.1.0
```

For development inside the container, mount the repo and install in editable mode:

```bash
docker run -ti \
  -v /path/to/ceremegbellum:/workspace/ceremegbellum \
  -v /path/to/subjects:/workspace/subjects \
  --name CMB mne-tools/cmb:v0.1.0

# Inside the container:
cd /workspace/ceremegbellum
pip install -e .
```

## License

CMB is licensed under the [MIT License](LICENSE).

Copyright (c) 2021-2026, authors of CMB. All rights reserved.
