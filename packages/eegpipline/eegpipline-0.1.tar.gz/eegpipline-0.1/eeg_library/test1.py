#%%
#import libraries that are usually used 
import mne
from mne.connectivity import spectral_connectivity
from mne.connectivity import envelope_correlation
import numpy as np


#%%

# import pandas as pd
# import glob
# #import seaborn as sns



# raw_list=[]
# folder = 'EEG_Preprocessing_code\\'
# EEG_files = glob.glob('..\\..\\semestr2\\Special_course\\EEG_Preprocessing_code\\Preprocessed_data\\good_subjects\\ica_rem_ano_mixed\\*.fif') # List of all preprocessed files

# raw_filt = [mne.io.read_raw_fif(EEG_files[0], preload = True).interpolate_bads().pick_types(eeg = True).resample(500) for rec in range(len(EEG_files))]
# raw=raw_filt[0]

#%%


class Epoch:
    def __init__(self,raw) :
        self.raw=raw
        #self.y=y
       
    def extract_epochs(self,baseline=False):
        annotations = mne.Annotations(onset=self.raw.annotations.onset-self.raw.first_time,duration=self.raw.annotations.duration,description=[x.split(',')[0] for x in self.raw.annotations.description])
        self.raw.set_annotations(annotations)
        events, event_id = mne.events_from_annotations(self.raw)
        if baseline == False:
            if 'Baseline' in event_id:
                event_id.pop('Baseline')
            if 'Baseline_post' in event_id:
                event_id.pop('Baseline_post')

        epochs = mne.Epochs(self.raw, events, event_id,tmin=1, tmax=round(self.raw.annotations.duration[1])-1, baseline=None, preload=True,verbose=False, reject_by_annotation=True,detrend=0)
        return epochs

class PSD(Epoch):
    '''Calculate Power Spectral Density in dB or V for epoch data (epochs)
    return psds[epochs_numbers,channels,PSD], freq[len(PSD)]'''   

    def __init__(self,raw) :
        super().__init__(raw)
        self.epochs = super().extract_epochs()
        self.tmin=self.epochs.tmin
        self.tmax=self.epochs.tmax


    def welch(self,win_size,dB):

        tmin = self.tmin                                         #min time for experiment (so far exclude first and last second)
        tmax = self.tmax                                         #max time for experiment
        fmin = 0                                                 #min frequency of interest
        fmax = 60.                                               #max frequency of interest
        nfft = int(self.epochs.info['sfreq'] * (tmax - tmin))    #number of point in fft
        win=int(self.epochs.info['sfreq'] * win_size)            #window size in seconds

        psds, freqs = mne.time_frequency.psd_welch(
            self.epochs,
            n_fft=nfft,
            n_overlap=0.5*win, 
            n_per_seg=win,
            tmin=tmin,
            fmin=fmin,
            fmax=fmax,
            window='hann',
            average='mean', 
            verbose='WARNING')
        if dB==True:
            psds = 10 * np.log10(psds)
        
        return psds, freqs

    def bartlett(self,dB=False):
        nfft = int(self.epochs.info['sfreq'] * (self.tmax - self.tmin))
        fmin = 0                                               
        fmax = 60.  
        psds, freqs = mne.time_frequency.psd_welch(
            self.epochs,
            n_fft=nfft,
            n_overlap=0, 
            n_per_seg=None,
            tmin=self.tmin, 
            tmax=self.tmax,
            fmin=fmin, 
            fmax=fmax,
            window='hann', 
            average = 'mean',
            verbose = 'WARNING')
        if dB == True:
            psds = 10 * np.log10(psds)

        return psds, freqs
   


class connectivity:
    def __init__(self,epochs,fmin,fmax) :

        '''Calculate connectivity measurments for epoch data (epochs)
        fmin = min frequency of interesed
        fmax=max frequency of intered '''

        self.epochs=epochs
        self.fmin=fmin
        self.fmax=fmax

    def wpli(self):

        '''Calculate wheighted phase lag index based on: 
        Martin Vinck, Robert Oostenveld, Marijn van Wingerden, Franscesco Battaglia, and Cyriel M.A. Pennartz. 
        An improved index of phase-synchronization for electrophysiological data in the presence of volume-conduction, noise and sample-size bias. NeuroImage, 55(4):1548–1565, 2011.
        doi:10.1016/j.neuroimage.2011.01.055.'''

        sfreq=self.epochs.info['sfreq']
        con= spectral_connectivity(self.epochs, method='wpli', mode='fourier', sfreq=sfreq, fmin=self.fmin , fmax=self.fmax ,faverage=True, mt_adaptive=False, n_jobs=1)
        return con

    def plv(self):

        '''Calculate wheighted phase lacking value based on: 
        Jean-Philippe Lachaux, Eugenio Rodriguez, Jacques Martinerie, and Francisco J. Varela. 
        Measuring phase synchrony in brain signals. Human Brain Mapping, 8(4):194–208, 1999. 
        doi:10.1002/(SICI)1097-0193(1999)8:4<194::AID-HBM4>3.0.CO;2-C.'''

        sfreq=self.epochs.info['sfreq']
        con= spectral_connectivity(self.epochs, method='plv', mode='fourier', sfreq=sfreq, fmin=self.fmin , fmax=self.fmax ,faverage=True, mt_adaptive=False, n_jobs=1)
        return con
    
    def envelope_correlation(self):
        '''Calculate envelope correlation (with band pass filter) based on: 
        Joerg F Hipp, David J Hawellek, Maurizio Corbetta, Markus Siegel, and Andreas K Engel. 
        Large-scale cortical correlation structure of spontaneous oscillatory activity. Nature Neuroscience, 15(6):884–890, 2012. 
        doi:10.1038/nn.3101.
        
        Sheraz Khan, Javeria A. Hashmi, Fahimeh Mamashli, Konstantinos Michmizos, Manfred G. Kitzbichler, Hari Bharadwaj, Yousra Bekhti, Santosh Ganesan, Keri-Lee A. Garel,
        Susan Whitfield-Gabrieli, Randy L. Gollub, Jian Kong, Lucia M. Vaina, Kunjan D. Rana, Steven M. Stufflebeam, Matti S. Hämäläinen, and Tal Kenet. 
        Maturation trajectories of cortical resting-state networks depend on the mediating frequency band.
        NeuroImage, 174:57–68, 2018.'''

        epochs_band_pass_filtered=self.epochs.filter(l_freq=1,h_freq=3,method='fir',fir_window='hamming')
        con=envelope_correlation(epochs_band_pass_filtered,combine='mean',orthogonalize=False)
        return con



#%%
# data=Epoch(raw)
# epochs=data.extract_epochs(baseline=False)

# con=connectivity(epochs,38,42)

# env=con.envelope_correlation()

#psd=PSD(raw)

#psd1,freq=psd.welch(10,dB=True)


# %%
