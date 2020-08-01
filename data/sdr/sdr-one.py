import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Filter parameters
maxpulses = 150


# Load data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
data = pd.read_csv('data/sdr-wl0.070-bl3.00-3.00-sl3.00-3.00-7-24-20.csv', delimiter='\t', names=names, index_col=False)
data['npulses'] = data['nsets'] + data['nresets'] - 1
rlos = data['rlo'].unique()
data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
data = data[data['bin'] != 7]
print data

data['success'] = data['success'].astype(bool) & (data['npulses'] <= maxpulses)
data['npulses'] = data['npulses'].clip(upper=maxpulses)

# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times', size=13)


# SDR Statistics
print 'Mean pulses:', data['npulses'].mean()
print 'Stdev pulses:', data['npulses'].std()
print 'Mean resets:', data['nresets'].mean()
print 'Stdev resets:', data['nresets'].std()
print 'Mean coarse attempts:', data['attempts1'].mean()
print 'Stdev coarse attempts:', data['attempts1'].std()
print 'Mean fine attempts:', data['attempts2'].mean()
print 'Stdev fine attempts:', data['attempts2'].std()
print 'Mean success rate:', data['success'].mean()

# SDR Mean Pulses
grouped = data.groupby(['bin'])
npulses = grouped['npulses']
npulses_mean = npulses.mean()
npulses_std = npulses.std()
npulses_mean.plot.bar(title='SDR: Mean Pulses per Level', figsize=(4,3), yerr=npulses_std)
plt.xlabel('Level Number')
plt.ylabel('Mean Pulses Required')
plt.tight_layout()
plt.savefig('figs/sdr-mean-pulses-bin.eps')
plt.show()

# SDR Mean Coarse Attempts
grouped = data.groupby(['bin'])
nresets = grouped['attempts1']
nresets_mean = nresets.mean()
nresets_std = nresets.std()
nresets_mean.plot.bar(title='SDR: Mean Coarse Attempts per Level', figsize=(4,3), yerr=nresets_std)
plt.xlabel('Level Number')
plt.ylabel('Mean Coarse Attempts Required')
plt.tight_layout()
plt.savefig('figs/sdr-mean-coarse-attempts-bin.eps')
plt.show()

# SDR Fine Coarse Attempts
grouped = data.groupby(['bin'])
nresets = grouped['attempts2']
nresets_mean = nresets.mean()
nresets_std = nresets.std()
nresets_mean.plot.bar(title='SDR: Mean Fine Attempts per Level', figsize=(4,3), yerr=nresets_std)
plt.xlabel('Level Number')
plt.ylabel('Mean Fine Attempts Required')
plt.tight_layout()
plt.savefig('figs/sdr-mean-fine-attempts-bin.eps')
plt.show()

# SDR Mean Success Rate
grouped = data.groupby(['bin'])
success = grouped['success']
success_mean = success.mean()
success_mean.plot.bar(title='SDR: Success Rate per Level', figsize=(4,3))
plt.xlabel('Level Number')
plt.ylabel('Success Rate')
plt.tight_layout()
plt.savefig('figs/sdr-mean-success-bin.eps')
plt.show()