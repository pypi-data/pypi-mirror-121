# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hsf', 'hsf.conf']

package_data = \
{'': ['*'],
 'hsf.conf': ['augmentation/*',
              'files/*',
              'hydra/help/*',
              'roiloc/*',
              'segmentation/*']}

install_requires = \
['antspyx>=0.2.9,<0.3.0',
 'hydra-core>=1.1.1,<2.0.0',
 'icecream>=2.1.1,<3.0.0',
 'onnxruntime>=1.8.1,<2.0.0',
 'roiloc>=0.2.3,<0.3.0',
 'torchio>=0.18.56,<0.19.0',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['hsf = hsf.factory:start']}

setup_kwargs = {
    'name': 'hsf',
    'version': '0.1.1',
    'description': 'Simple yet exhaustive segmentation tool of the Hippocampal Subfields in T1w and T2w MRIs.',
    'long_description': '======================================\nHippocampal Segmentation Factory (HSF)\n======================================\n\n.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.5527122.svg\n   :target: https://doi.org/10.5281/zenodo.5527122\n\nThe Hippocampal Segmentation Factory (HSF) is a Python package for\nthe segmentation of the hippocampal subfields in raw MRI volumes.\n\n.. image:: https://raw.githubusercontent.com/clementpoiret/HSF/0537a69c6390d497157e0e6c95398610b6447ace/res/header.svg\n\nThe main idea is to have a click-button tool that allows the user to\nsegment the hippocampal subfields in a given raw image (T1w or T2w), while keeping\nas much modularity and customization options as possible.\n\nHSF will be able to segment the following subfields:\n\n- Dentate gyrus (DG),\n- Cornu Ammonis (CA1, CA2 & CA3) in a flexible way (e.g. you can ask to combine CA2 and CA3),\n- Subiculum (SUB).\n\nHSF will segment the hippocampus from head to tail: it will produce\nan homogeneous segmentation from the anterior hippocampus (head), to\nthe posterior hippocampus (tail), without assigning a specific head\nor tail class.\n\nPlease note that the tool is still under development and is not yet\nready for production use. It uses multiple expert deep learning models\ntrained on 600+ manually segmented hippocampi (see `Which MRI modalities are usable in HSF?`_)\nwhich are not yet fully trained.\n\nHSF uses inference sessions provided by `ONNXRuntime <https://onnxruntime.ai>`_,\nwhich means that it can be used *theoretically* on Windows, MacOS and Linux,\nand the following hardware accelerations: CPU, CUDA, DirectML, OneDNN,\nOpenVINO, TensorRT, NUPHAR, Vitis AI, ACL, ArmNN, MIGraphX, and Rockchip NPU.\nPlease be aware that we do not tested all possible configurations, as HSF\nhas been tested only on CPU and CUDA on Linux (Debian-based and Arch-based distros).\n\n\nInstallation\n************\n\nTo install the package, first setup an environment suitable for `ONNX Runtime <https://onnxruntime.ai>`_.\n\nIf the ONNX Runtime isn\'t properly configured, you might be stuck running inference sessions on CPU, which is not optimal.\n\nThen, simply run:\n\n``pip install hsf``.\n\nQuick start\n***********\n\nOnce installed, HSF can be used simply by running the ``hsf`` command.\n\nFor example, to segment a set of T2w MRIs of 0.3*0.3*1.2, run:\n\n``hsf files.path="~/Dataset/MRIs/" files.pattern="*T2w.nii" roiloc.contrast="t2" roiloc.margin=\\[10,2,10\\] segmentation=bagging_accurate segmentation.ca_mode="1/2/3"``\n\nNow, let\'s dive into the details.\n\n``files.path`` and ``files.pattern`` are mandatory parameters.\nThey specify the path to the dataset (or MRI) and the pattern to find the files.\n\nAll parameters starting with ``roiloc.`` are directly linked to our home-made ROI location algorithm.\nYou can find more information about it in the `related GitHub repository <https://github.com/clementpoiret/ROILoc>`_.\n\nTo date, we propose 4 different segmentation algorithms (from the fastest to the most accurate):\n\n- ``single_fast``: a segmentation is performed on the whole volume by only one model,\n- ``single_accurate``: a single model segments the same volume that has been augmented 20 times through TTA,\n- ``bagging_fast``: a bagging ensemble of 5 models is used to segment the volume without TTA,\n- ``bagging_accurate``: a bagging ensemble of 5 models is used to segment the volume with TTA.\n\nFinally, ``segmentation.ca_mode`` is a parameter that allows to combine CA1, CA2 and CA3 subfields.\nIt is particularly useful when you want to segment low-resolution images where it makes no sense to\ndistinguish between CA\'s subfields.\n\nConfiguration\n*************\n\nAs HSF is pretty modular, you can easily configure it to your needs thanks to Hydra.\n\nCompose your configuration from those groups (group=option)\n\n* augmentation: default\n* files: default\n* roiloc: default_t2iso\n* segmentation: bagging_accurate, bagging_fast, single_accurate, single_fast\n\nOverride anything in the config (e.g. hsf roiloc.margin=[16, 2, 16])\nYou can also add specific configs absent from the default yaml files (e.g. hsf +augmentation.elastic.image_interpolation=sitkBSpline)\nFields set with ??? are mandatory.\n\nfiles:\n\n* path: ???\n* pattern: ???\n* mask_pattern: ``*mask.nii.gz``\n* output_dir: hsf_outputs\n\nroiloc:\n\n* contrast: t2\n* roi: hippocampus\n* bet: false\n* transform_type: AffineFast\n* margin: [8, 8, 8]\n\nsegmentation:\n\n* ca_mode: 1/2/3\n* models_path: ~/.hsf/models\n* models:\n   *  arunet_bag_0.onnx:\n   *  url: https://zenodo.org/record/5524594/files/arunet_bag0.onnx?download=1\n   *  md5: 10026a4ef697871b7d49c08a4f16b6ae\n   * segmentation:\n      * test_time_augmentation: true\n      * test_time_num_aug: 20\n\naugmentation:\n\n* flip:\n   * axes:\n      * LR\n   * flip_probability: 0.5\n   * affine_probability: 0.75\n   * affine:\n      * scales: 0.2\n      * degrees: 15\n      * translation: 3\n      * isotropic: false\n   * elastic_probability: 0.25\n   * elastic:\n      * num_control_points: 4\n      * max_displacement: 4\n      * locked_borders: 0\n\n\nHow to improve segmentation quality?\n************************************\n\nIf the segmentation is not good enough, you can try to improve it with the following steps:\n- Try to augment the number of TTAs,\n- Try to use a different ONNX model (by adding its ONNX to ``~/.hsf/models``),\n\nIf the segmentation is clearly absent or outside the hippocampus, it is because ROILoc failed.\nThis is caused by ANTs having troubles to perform registration, leading to a wrong bounding box.\n\nGenerally, performing a brain extraction step, our using another ``transform_type`` (e.g. ``SyN``)\nsolves this problem.\n\nAlso check that the margins are high engough, otherwise you might be missing some subfields\n(crop effect).\n\n\nWhich MRI modalities are usable in HSF?\n***************************************\n\nWe trained HSF using T1 (MPRAGE & MP2RAGE) and T2 (mostly TSE) modalities.\n\nHSF should work with isotropic and non-isotropic images, but we do not encourage the segmentation\non 1mm iso images as the resolution is too low to distinguish between subfields.\n\nWe trained on CoroT2 with resolutions as low as 0.125*0.125*1.2mm.\n\nYou can of course try with other settings, feel free to report your results :)\n\n\nCustom models\n*************\n\nYou can use your own ONNX models by placing them in ``~/.hsf/models``, and providing the correct configuration (path & md5).\n\nYou can also just place your models there, and use our ``bagging*`` presets, they will be included in the plurality votes.\n\n\nPerformance tunning\n*******************\n\nPlease refer to ONNXRuntime\'s documentation for setting-up the correct environment,\nto benefit from the performance and scalability of hardware accelerations.\n\n\nAuthorship, Affiliations and Citations\n**************************************\n\nAuthorship:\n\n* C Poiret, UNIACT-NeuroSpin, CEA, Saclay University, France,\n* A Bouyeure, UNIACT-NeuroSpin, CEA, Saclay University, France,\n* S Patil, UNIACT-NeuroSpin, CEA, Saclay University, France,\n* C Boniteau, UNIACT-NeuroSpin, CEA, Saclay University, France,\n* M Noulhiane, UNIACT-NeuroSpin, CEA, Saclay University, France.\n\nIf you use this work, please cite it as follows:\n\n``C. Poiret, et al. (2021). clementpoiret/HSF. Zenodo. https://doi.org/10.5281/zenodo.5527122``\n\nThis work licensed under MIT license was supported in part by the Fondation de France and the IDRIS/GENCI for the HPE Supercomputer Jean Zay.\n',
    'author': 'Clément POIRET',
    'author_email': 'poiret.clement@outlook.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hippomnesis.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
