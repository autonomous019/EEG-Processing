"""


"""
# Authors:
#
#
# License: BSD (3-clause)

import os
import numpy as np

import mne

from mne.datasets import sample

print(__doc__)

data_path = sample.data_path()

###############################################################################
# Set parameters

#.1/25th of second is 40ms anything smaller then this goes unnoticed by consciousness in working memory. this works
#subliminally because the eyes can see it but it does not invoke reflection at deeper levels of the brain.
#at the higher levels beyond visible sight recognition is that of the fps of the human mind say for safety
#it is 240Hz max then 4ms is optimal for hidden things, subliminals, etc that is a very long time for a computer
###############################################################################
# Show result

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_filt-0-40_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file)

print(raw)
print(raw.info)

raw.plot_psd(fmax=50)
raw.plot(duration=5, n_channels=30)

ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
ica.fit(raw)
ica.exclude = [1, 2]  # details on how we picked these are omitted here
ica.plot_properties(raw, picks=ica.exclude)

orig_raw = raw.copy()
raw.load_data()
ica.apply(raw)

# show some frontal channels to clearly illustrate the artifact removal
chs = ['MEG 0111', 'MEG 0121', 'MEG 0131', 'MEG 0211', 'MEG 0221', 'MEG 0231',
       'MEG 0311', 'MEG 0321', 'MEG 0331', 'MEG 1511', 'MEG 1521', 'MEG 1531',
       'EEG 001', 'EEG 002', 'EEG 003', 'EEG 004', 'EEG 005', 'EEG 006',
       'EEG 007', 'EEG 008']

chan_idxs = [raw.ch_names.index(ch) for ch in chs]
orig_raw.plot(order=chan_idxs, start=12, duration=4)
raw.plot(order=chan_idxs, start=12, duration=4)

events = mne.find_events(raw, stim_channel='STI 014')
print(events[:5])  # show the first 5
event_dict = {'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3,
              'visual/right': 4, 'smiley': 5, 'buttonpress': 32}

fig = mne.viz.plot_events(events, event_id=event_dict, sfreq=raw.info['sfreq'],
                          first_samp=raw.first_samp)



reject_criteria = dict(mag=4000e-15,     # 4000 fT
                       grad=4000e-13,    # 4000 fT/cm
                       eeg=150e-6,       # 150 µV
                       eog=250e-6)       # 250 µV

epochs = mne.Epochs(raw, events, event_id=event_dict, tmin=-0.2, tmax=0.5,
                    reject=reject_criteria, preload=True)

conds_we_care_about = ['auditory/left', 'auditory/right',
                       'visual/left', 'visual/right']
epochs.equalize_event_counts(conds_we_care_about)  # this operates in-place
aud_epochs = epochs['auditory']
vis_epochs = epochs['visual']
del raw, epochs  # free up memory

aud_epochs.plot_image(picks=['MEG 1332', 'EEG 021'])

frequencies = np.arange(7, 30, 3)
power = mne.time_frequency.tfr_morlet(aud_epochs, n_cycles=2, return_itc=False,
                                      freqs=frequencies, decim=3)
power.plot(['MEG 1332'])

aud_evoked = aud_epochs.average()
vis_evoked = vis_epochs.average()

mne.viz.plot_compare_evokeds(dict(auditory=aud_evoked, visual=vis_evoked),
                             legend='upper left', show_sensors='upper right')

aud_evoked.plot_joint(picks='eeg')
aud_evoked.plot_topomap(times=[0., 0.08, 0.1, 0.12, 0.2], ch_type='eeg')



evoked_diff = mne.combine_evoked([aud_evoked, vis_evoked], weights=[1, -1])
evoked_diff.pick_types(meg='mag').plot_topo(color='r', legend=False)


'''

source space- A source space (abbr. src) specifies where in the brain one wants to estimate the source amplitudes. 
It corresponds to locations of a set of candidate equivalent current dipoles. MNE mostly works with 
source spaces defined on the cortical surfaces estimated by FreeSurfer from a T1-weighted MRI image. 
See Head model and forward computation to read about how to compute a forward operator on a source space. 
See SourceSpaces for the API of the corresponding object class.

inverse operator¶
The inverse operator is an  matrix ( source locations by  sensors) that, when applied to the sensor signals, 
yields estimates of the brain activity that gave rise to the observed sensor signals. Inverse operators are available 
for the linear inverse methods MNE, dSPM, sLORETA and eLORETA. See minimum_norm.apply_inverse().

Because this “inverse problem” is underdetermined (there is no unique solution), here we further constrain the solution 
by providing a regularization parameter specifying the relative smoothness of the current estimates in terms of a 
signal-to-noise ratio (where “noise” here is akin to baseline activity level across all of cortex).

'''

# load inverse operator
inverse_operator_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                     'sample_audvis-meg-oct-6-meg-inv.fif')
inv_operator = mne.minimum_norm.read_inverse_operator(inverse_operator_file)
# set signal-to-noise ratio (SNR) to compute regularization parameter (λ²)
snr = 3.
lambda2 = 1. / snr ** 2
# generate the source time course (STC)
stc = mne.minimum_norm.apply_inverse(vis_evoked, inv_operator,
                                     lambda2=lambda2,
                                     method='MNE')  # or dSPM, sLORETA, eLORETA

# path to subjects' MRI files
subjects_dir = os.path.join(sample_data_folder, 'subjects')
# plot the STC
stc.plot(initial_time=0.1, hemi='split', views=['lat', 'med'],
         subjects_dir=subjects_dir)



