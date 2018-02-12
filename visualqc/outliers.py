"""

Outlier detection module.

"""

import numpy as np
from scipy import stats
import visualqc.config as cfg
from visualqc.readers import read_aparc_stats_wholebrain, read_aseg_stats
from visualqc.utils import read_id_list
from sklearn.ensemble import IsolationForest
from genericpath import exists as pexists
from os import makedirs
from os.path import join as pjoin

def outlier_advisory(fs_dir,
                     id_list_file,
                     feature_list=cfg.freesurfer_feature_types_for_outlier_detection,
                     method='isolation_forest',
                     fraction_of_outliers=.3,
                     out_dir=None):
    """
    Performs outlier detection based on chosen types of data and technique.

    Returns
    -------
    outliers_by_sample : dict
        Keyed in by sample id, each element is a list of features that identified a given ID as a possible outlier.

    outliers_by_feature : dict
        Keyed in by feature, each element is a list of IDs that feature identified as possible outliers.

    """

    if not pexists(out_dir):
        makedirs(out_dir)

    outliers_by_feature = dict()
    id_list = read_id_list(id_list_file)

    for feature_type in feature_list:
        features = gather_freesurfer_data(fs_dir, id_list, feature_type)
        out_file = pjoin(out_dir,'{}_{}_{}.txt'.format(cfg.outlier_list_prefix, method, feature_type))
        outliers_by_feature[feature_type] = detect_outliers(features,
                                                            id_list,
                                                            method=method,
                                                            out_file=out_file,
                                                            fraction_of_outliers=fraction_of_outliers)

    # re-organizing the identified outliers by sample
    outliers_by_sample = dict()
    for id in id_list:
        # each id contains a list of all feature types that flagged it as an outlier
        outliers_by_sample[id] = [ feat for feat in feature_list if id in outliers_by_feature[feat] ]

    # dropping the IDs that were not flagged by any feature
    # so a imple ID in dict would reveal whether it was ever suspected as an outlier
    outliers_by_sample = { id : flag_list for id, flag_list in outliers_by_sample.items() if flag_list }

    return outliers_by_sample, outliers_by_feature


def gather_freesurfer_data(fs_dir,
                           id_list,
                           feature_type='whole_brain'):
    """
    Reads all the relevant features to perform outlier detection on.

    feature_type could be cortical, subcortical, or whole_brain.

    """

    feature_type = feature_type.lower()
    if feature_type in ['cortical', ]:
        features = np.vstack([read_aparc_stats_wholebrain(fs_dir, id) for id in id_list])
    elif feature_type in ['subcortical', ]:
        features = np.vstack([read_aseg_stats(fs_dir, id) for id in id_list])
    elif feature_type in ['whole_brain', 'wholebrain']:
        cortical = np.vstack([read_aparc_stats_wholebrain(fs_dir, id) for id in id_list])
        sub_ctx = np.vstack([read_aseg_stats(fs_dir, id) for id in id_list])
        features = np.hstack((cortical, sub_ctx))
    else:
        raise ValueError('Invalid type of features requested.')

    return features


def detect_outliers(features,
                    id_list,
                    method='isolation_forest',
                    fraction_of_outliers=.3,
                    out_file=None):
    """Performs outlier detection based on chosen types of features and detection technique."""

    method = method.lower()
    if method == 'isolation_forest':
        outlying_ids = run_isolation_forest(features, id_list, fraction_of_outliers=fraction_of_outliers)
    else:
        raise NotImplementedError('Chosen detection method {} not implemented or invalid.'.format(method))

    # printing out info on detected outliers
    print('\nPossible outliers ({} / {}):'.format(len(outlying_ids), len(id_list)))
    print('\n'.join(outlying_ids))

    # writing out to a file, if requested
    if out_file is not None:
        np.savetxt(out_file, outlying_ids, fmt='%s', delimiter='\n')

    return outlying_ids


def run_isolation_forest(features, id_list, fraction_of_outliers=.3):
    """Performs anomaly detection based on Isolation Forest."""

    rng = np.random.RandomState(1984)

    num_samples = features.shape[0]
    iso_f = IsolationForest(max_samples=num_samples,
                            contamination=fraction_of_outliers,
                            random_state=rng)
    iso_f.fit(features)
    pred_scores = iso_f.decision_function(features)

    threshold = stats.scoreatpercentile(pred_scores, [100 * fraction_of_outliers, ])
    outlying_ids = id_list[pred_scores < threshold]

    return outlying_ids
