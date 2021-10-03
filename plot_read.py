"""


"""
# Authors:
#
#
# License: BSD (3-clause)

import os


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