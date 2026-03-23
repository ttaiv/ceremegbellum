#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Core computational functions for cerebellum data processing."""
# ---------------------------------------------------------------------------
# Authors: John G Samuelson <johnsam@mit.edu>
#          Christoph Dinh <christoph.dinh@brain-link.de>
# Created: May, 2020
# License: MIT
# ---------------------------------------------------------------------------

import os
import shutil


def get_cerebellum_data(cmb_path=None):
    """
    Checks if the required cerebellum data are available and download if not.

    Parameters
    ----------
    cmb_path : str, optional
        Path to the ceremegbellum data folder. If None, defaults to the
        package installation directory.
    """
    if cmb_path is None:
        from . import CMB_DATA_DIR
        cmb_path = CMB_DATA_DIR
    if os.path.exists(os.path.join(cmb_path, 'data', 'cerebellum_geo')) and \
        os.path.isdir(os.path.join(cmb_path, 'nnUNet', 'RESULTS_FOLDER', 'nnUNet', '3d_fullres', 'Task001_mask')) and \
        os.path.isdir(os.path.join(cmb_path, 'nnUNet', 'RESULTS_FOLDER', 'nnUNet', '3d_fullres', 'Task002_lh')) and \
        os.path.isdir(os.path.join(cmb_path, 'nnUNet', 'RESULTS_FOLDER', 'nnUNet', '3d_fullres', 'Task003_rh')) and \
        os.path.isdir(os.path.join(cmb_path, 'nnUNet', 'RESULTS_FOLDER', 'nnUNet', '3d_fullres', 'Task004_refine_lobsI_IV')) and \
        os.path.exists(os.path.join(cmb_path, 'data', 'brain.nii'))    :
            print('The required atlas data and segmentation models seem to be downloaded.')
    else:
        from pooch import retrieve
        import zipfile
        print('Seems like some data are missing. No problem, fetching...')
        os.makedirs(os.path.join(cmb_path, 'tmp'), exist_ok=True)
        os.makedirs(os.path.join(cmb_path, 'data'), exist_ok=True)
        os.makedirs(os.path.join(cmb_path, 'nnUNet', 'RESULTS_FOLDER', 'nnUNet', '3d_fullres'), exist_ok=True)
        os.makedirs(os.path.join(cmb_path, 'nnUNet', 'nnUNet_preprocessed'), exist_ok=True)
        os.makedirs(os.path.join(cmb_path, 'nnUNet', 'nnUNet_raw_data_base'), exist_ok=True)
        retrieve(url='https://osf.io/sdn9h/download',
                 known_hash='sha256:1d07115e5d9d04c5b6b4e681f881a7c87a4b06fca07837226dcaf6746e286d54',
                 fname='ceremegbellum.zip',
                 path=os.path.join(cmb_path, 'tmp'))
        with zipfile.ZipFile(os.path.join(cmb_path, 'tmp', 'ceremegbellum.zip'), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(cmb_path, 'tmp'))
        shutil.move(os.path.join(cmb_path, 'tmp', 'osf_data', 'cerebellum_geo'),
                    os.path.join(cmb_path, 'data', 'cerebellum_geo'))
        shutil.move(os.path.join(cmb_path, 'tmp', 'osf_data', 'brain.nii'),
                    os.path.join(cmb_path, 'data', 'brain.nii'))
        # Move all Task* directories
        tmp_osf = os.path.join(cmb_path, 'tmp', 'osf_data')
        dest = os.path.join(cmb_path, 'nnUNet', 'RESULTS_FOLDER', 'nnUNet', '3d_fullres')
        for item in os.listdir(tmp_osf):
            if item.startswith('Task'):
                shutil.move(os.path.join(tmp_osf, item), os.path.join(dest, item))
        shutil.rmtree(os.path.join(cmb_path, 'tmp'), ignore_errors=True)  # clean up
        print('Done.')
    return
