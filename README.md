# EEG Processing
 various code files for processing EEG/MEG Data

The files in this repository are working files I use to parse EEG data which can then be used for identifying brain waves of interest to a Brain Computer Interface.  The files are mostly in Python for EEG processing of raw data, then javascript/html5 for display of that data.  I use Python-MNE for eeg related parsing and collection.

MNE: a basic example of parsing FIF files of EEG data is in <a href="https://github.com/autonomous019/EEG-Processing/blob/main/plot_read.py">plot_read.py</a>, plot_read_epoch.py is similiar but deals with identifying EEG epochs. To run the basic example you may also need to install, using pip (<code> >pip install mne</code>), such addons as  numpy, scikit-learn, mne, os may be needed. 



