"""
Module with algorithms to extract various features of interest for outlier detection methods.

"""

from visualqc import config as cfg
from visualqc.utils import read_image, scale_0to1
import numpy as np
from os.path import join as pjoin, splitext, exists as pexists
from os import makedirs

def t1_histogram_whole_scan(in_mri_path, num_bins=cfg.num_bins_histogram_intensity_distribution):
    """
    Computes histogram over the intensity distribution over the entire scan, including brain, skull and background.

    Parameters
    ----------

    in_mri_path : str
        Path to an MRI scan readable by Nibabel

    Returns
    -------
    hist : ndarray
        Array of prob. densities for intensity

    """

    img = read_image(in_mri_path)
    # scaled, and reshaped
    arr_0to1 = scale_0to1(img).flatten()
    # compute prob. density
    hist, _ = np.histogram(arr_0to1, bins=num_bins, density=True)

    return hist


def extract_T1_features(wf, feature_type='histogram_whole_scan'):
    """
    Returns a set of features from T1 sMRI scan from each subject.

    Parameters
    ----------
    wf : QCWorkFlow
        Self-contained object describing the details of a particular QC operation.

    feature_type : str
        String the identifying the type of features to read.

    Returns
    -------
    feature_paths : dict
        Dict containing paths to files with extracted features.

    """

    feature_type = feature_type.lower()
    basename = lambda name: splitext(name)[0]
    out_csv_name = '{}_{}_features.csv'.format(basename(wf.mri_name), feature_type)
    path_to_csv = lambda sid: pjoin(wf.out_dir, sid, out_csv_name)
    if feature_type in ['histogram_whole_scan', ]:
        extract_method = t1_histogram_whole_scan
    else:
        raise NotImplementedError('Requested feature type {} not implemented!\n'
                                  '\tAllowed options : {} '.format(feature_type, cfg.t1_mri_features_OLD))

    feature_paths = dict()
    num_subjects = len(wf.id_list)
    for counter, sid in enumerate(wf.id_list):
        print('{} : {}/{}'.format(sid, counter+1, num_subjects))
        makedirs(pjoin(wf.out_dir, sid), exist_ok=True)
        feat_file = path_to_csv(sid)
        if not pexists(feat_file):
            features = extract_method(wf.path_getter_inputs(sid))
            try:
                np.savetxt(feat_file, features, delimiter='\n', header=feature_type)
            except:
                raise IOError('Unable to save extracted features to disk!')
        else:
            feature_paths[sid] = feat_file

    return feature_paths
