"""
Central place to store the config info

"""
import numpy as np

# default values
default_out_dir_name = 'visualqc'
annot_vis_dir_name = 'annot_visualizations'
default_mri_name = 'orig.mgz' # brainmask would not help check expansion of surfaces into skull
default_seg_name = 'aparc+aseg.mgz'
required_files = (default_mri_name, default_seg_name)

freesurfer_features_outlier_detection = ('cortical', 'subcortical')
outlier_list_prefix = 'possible_outliers'
alert_background_color = 'xkcd:coral'
alert_colors_outlier = dict(cortical='xkcd:hot pink', subcortical='xkcd:periwinkle')

position_annot_text = (0.990, 0.98)
annot_text_props = dict(ha='right', va='top', multialignment='left',
                        wrap=True, fontsize='large', color='#c65102')

alert_text_props = dict(horizontalalignment='center', fontsize='medium',
                        color='white', backgroundcolor=alert_background_color)

default_outlier_detection_method = 'isolation_forest'
default_outlier_fraction = 0.2
avail_outlier_detection_methods = ('isolation_forest',)
# OLD -> OutLier Detection
avail_OLD_source_of_features = ('freesurfer', 't1_mri')

default_freesurfer_dir = None
cortical_types = ('cortical_volumetric', 'cortical_contour')
label_types = ('labels_volumetric', 'labels_contour')
freesurfer_vis_types = cortical_types
visualization_combination_choices = cortical_types + label_types
default_vis_type = 'cortical_contour'

# these vis types would need to be identified by more than one label
vis_types_with_multiple_ROIs = ('labels_volumetric', 'labels_contour')

surface_view_angles = ['lateral', 'medial', 'transverse']

freesurfer_vis_cmd = 'tksurfer'

default_label_set = None

default_user_dir = None

default_alpha_mri = 1.0
default_alpha_seg = 0.7
default_alpha_set = (default_alpha_mri, default_alpha_seg)

default_views = (0, 1, 2)
default_num_slices = 12
default_num_rows = 2
default_padding = 5  # pixels/voxels

default_review_figsize = [13, 9]

default_navigation_options = ("Next", "Quit")
# shortcuts L, F, S have actions on matplotlib interface, so choosing other words
default_rating_list = ('Good', 'Doubtful', 'Bad', 'Error', 'Review later')
map_short_rating = dict(g='Good', d='Doubtful', b='Bad', e='Error', r='Review later')
default_rating_list_shortform = map_short_rating.keys()
ratings_not_to_be_recorded = [None, '']

# for serialization
delimiter = ','
# when ratings or notes contain the above delimiter, it will be replaced by this
delimiter_replacement = ';'
# when ratings are multiple (in some use cases), how to concat them into a single string without a delimiter
rating_joiner = '+'

textbox_title = ''
textbox_initial_text = 'Notes: '  # Text(text='Your Notes:', )

color_rating_axis = 'xkcd:slate'
color_textbox_input = '#009b8c'
color_quit_axis = '#009b8c'
color_slider_axis = '#fa8072'
text_box_color = 'xkcd:grey'
text_box_text_color = 'black'
text_option_color = 'white'
color_navig_text = 'black'

position_outlier_alert = (0.950, 0.92)
position_outlier_alert_box = [0.902, 0.87, 0.097, 0.07]
position_rating_axis = [0.905, 0.65, 0.09, 0.2]
position_checkbox = [0.905, 0.42, 0.09, 0.25]
position_text_input = [0.900, 0.20, 0.095, 0.2]
position_slider_seg_alpha = [0.905, 0.35, 0.07, 0.02]
position_next_button = [0.905, 0.13, 0.07, 0.04]
position_quit_button = [0.905, 0.07, 0.07, 0.04]
position_navig_options = [0.905, 0.21, 0.07, 0.12]

review_area = dict(left  =0.08, right=0.88,
                   bottom=0.06, top=0.98,
                   wspace=0.05, hspace=0.02)
no_blank_area = dict(left=0.01, right=0.99,
                     bottom=0.01, top=0.99,
                     wspace=0.05, hspace=0.02)

suffix_ratings_dir = 'ratings'
file_name_ratings = 'ratings.all.csv'
prefix_backup = 'backup'

# visualization layout
zoomed_position = [0.15, 0.15, 0.7, 0.7]
default_contour_face_color = 'yellow'  # '#cccc00' # 'yellow'
contour_line_width = 1
binary_pixel_value = 1
contour_level = 0.5
line_break = [np.NaN, np.NaN]

## ----------------------------------------------------------------------------
# T1 mri specific
## ----------------------------------------------------------------------------

t1_mri_pass_indicator = 'Pass' # TODO Tired and Review Later must also be handled separately??
t1_mri_default_issue_list = (t1_mri_pass_indicator, 'Motion', 'Ringing', 'Ghosting',
                             'Contrast', 'blurrY', 'Bright', 'Dark', 'Orient/FOV',
                             'Weird', 'Other', "i'm Tired", 'reView later')
abbreviation_t1_mri_default_issue_list = {'p': t1_mri_pass_indicator, 'm': 'Motion', 'r': 'Ringing', 'g': 'Ghosting',
                                          'c': 'Contrast', 'y': 'blurrY', 'b': 'Bright', 'd': 'Dark', 'o' : 'Orient/FOV',
                                          'w': 'Weird', 's': 'Something else', 't': "i'm Tired", 'v': 'reView later'}

t1_mri_default_rating_list_shortform = abbreviation_t1_mri_default_issue_list.keys()

num_bins_histogram_intensity_distribution = 100

# outlier detection (OLD)
t1_mri_features_OLD = ('histogram_whole_scan', )
checkbox_rect_width  = 0.05
checkbox_rect_height = 0.05
checkbox_cross_color = 'xkcd:goldenrod'

position_histogram_t1_mri = [0.905, 0.7, 0.09, 0.1]
title_histogram_t1_mri = 'nonzero intensities'
num_bins_histogram_display = 30
xticks_histogram_t1_mri = np.arange(0.1, 1.01, 0.2)
color_histogram_t1_mri = ('#c9ae74') #sandstone

## ----------------------------------------------------------------------------
# Functional mri specific
## ----------------------------------------------------------------------------

func_mri_pass_indicator = 'Pass' # TODO Tired and Review Later must also be handled separately??
func_mri_default_issue_list = (func_mri_pass_indicator, 'Motion', 'Ringing', 'Ghosting',
                               'Orient/FOV', 'Weird', 'Other', "i'm Tired", 'reView later')

abbreviation_func_mri_default_issue_list = {'p': func_mri_pass_indicator, 'm': 'Motion', 'r': 'Ringing',
                                            'g': 'Ghosting', 'o' : 'Orient/FOV', 'w': 'Weird',
                                            's': 'Something else', 't': "i'm Tired", 'v': 'reView later'}

func_mri_default_rating_list_shortform = abbreviation_func_mri_default_issue_list.keys()

func_outlier_features = None

func_mri_BIDS_filters = dict(modalities='func', types='bold')
# usually done in analyses to try keep the numbers in numerical calculations away from small values
# not important here, just for display, doing it anyways.
scale_factor_BOLD = 1000

alpha_stats_overlay = 0.5
linewidth_stats_fmri = 2
linestyle_stats_fmri = '-'

default_views_fmri = (0, )
default_num_slices_fmri = 30
default_num_rows_fmri = 5

## ----------------------------------------------------------------------------

features_outlier_detection = freesurfer_features_outlier_detection + t1_mri_features_OLD
