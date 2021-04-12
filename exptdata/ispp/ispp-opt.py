import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Load data
bpc = 3
stepsize = 0.01 if bpc == 2 else 0.005
datas = []
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
for step in np.arange(stepsize, 0.091, stepsize):
    step = round(step, 3)
    data = pd.read_csv('data/3bpc/ispp-wl%.3f-bl0.80-sl0.30-0.30-7-13-20.csv' % step, delimiter='\t', names=names, index_col=False)
    data['npulses'] = data['nsets'] + data['nresets'] - 1
    data['stepsize'] = step
    rlos = data['rlo'].unique()
    data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
    data = data[data['bin'] != (2**bpc - 1)]
    datas.append(data)
data = pd.concat(datas)

# Cells to ignore
ignore = [3879, 3860, 4023]
ignore = []
data = data[~data['addr'].isin(ignore)]
data = data[((data['stepsize'] * 1000 % 10) < 4) | (np.abs(data['stepsize']-0.05) < 1e-10)]

# Get maxpulses where > 99%
maxpulses = {}
for maxpulse in range(2000,0, -1):
    clipped = data.copy()
    clipped['npulses'] = data['npulses'].clip(upper=maxpulse)
    clipped['success'] = clipped['success'].astype(bool) & (clipped['npulses'] < maxpulse)
    grouped = clipped.groupby(['stepsize'])
    success = grouped['success'].mean()
    for stepsize in data['stepsize'].unique():
        if success[stepsize] < 0.99 and stepsize not in maxpulses:
            maxpulses[stepsize] = maxpulse
print(maxpulses)
for stepsize in data['stepsize'].unique():
   data.loc[data.stepsize == stepsize, 'npulses'] = data[data.stepsize == stepsize].npulses.clip(upper=maxpulses[stepsize])
print(data.groupby(['stepsize']).mean())


# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    #'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times', size=13)


# ISPP Mean Step
grouped = data.groupby(['stepsize'])
npulses = grouped['npulses']
npulses_mean = npulses.mean()
print(npulses_mean)
npulses_std = npulses.std()
print(npulses_std)
npulses_mean.plot.bar(title='ISPP Tuning', figsize=(3,3), color=['r' if s < 0.99 else 'c' for s in grouped['success'].mean()]) #, yerr=npulses_std)
#plt.legend(['$\geq$99\% success rate'])
#plt.ylim(20, 60)
plt.ylim(50, 150)
plt.xlabel('WL Voltage Step (V)')
plt.ylabel('Mean Pulses Required')
if bpc == 2:
    plt.annotate('Optimal Step Size: 0.1V', xy=(9, 20), xytext=(8, 40), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='bottom')
if bpc == 3:
    plt.annotate('Optimal Step Size: 0.07V', xy=(6, 80), xytext=(5, 120), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='bottom')
plt.tight_layout()
plt.savefig('figs/ispp-mean-pulses-step.eps')
plt.savefig('figs/ispp-mean-pulses-step.pdf')
plt.show()
exit()

# ISPP Mean Resets
grouped = data.groupby(['stepsize'])
nresets = grouped['nresets']
nresets_mean = nresets.mean()
print(nresets_mean)
nresets_std = nresets.std()
print(nresets_std)
nresets_mean.plot.bar(title='ISPP: Mean Resets vs. Step Size', figsize=(5,3), yerr=nresets_std)
plt.xlabel('Step Size (V)')
plt.ylabel('Mean Resets Required')
plt.tight_layout()
plt.savefig('figs/ispp-mean-resets-step.eps')
plt.show()

# ISPP Mean Success Rate
grouped = data.groupby(['stepsize'])
success = grouped['success']
success_mean = success.mean()
print(success_mean)
success_mean.plot.bar(title='ISPP: Success Rate vs. Step Size', figsize=(5,3))
plt.xlabel('Step Size (V)')
plt.ylabel('Success Rate')
plt.tight_layout()
plt.savefig('figs/ispp-mean-success-step.eps')
plt.show()


# ISPP Mean Step
grouped = data[np.abs(data['stepsize'] - 0.07) <= 1e-9].groupby(['bin'])
npulses = grouped['npulses']
npulses_mean = npulses.mean()
npulses_std = npulses.std()
npulses_mean.plot.bar(title='ISPP: Mean Pulses per Level', figsize=(5,3), yerr=npulses_std)
plt.xlabel('Level Number')
plt.ylabel('Mean Pulses Required')
plt.tight_layout()
plt.savefig('figs/ispp-mean-pulses-beststep-bin.eps')
plt.show()

# ISPP Mean Resets
grouped = data[np.abs(data['stepsize'] - 0.07) <= 1e-9].groupby(['bin'])
nresets = grouped['nresets']
nresets_mean = nresets.mean()
nresets_std = nresets.std()
nresets_mean.plot.bar(title='ISPP: Mean Resets per Level', figsize=(5,3), yerr=nresets_std)
plt.xlabel('Level Number')
plt.ylabel('Mean Resets Required')
plt.tight_layout()
plt.savefig('figs/ispp-mean-resets-beststep-bin.eps')
plt.show()

# ISPP Mean Success Rate
grouped = data[np.abs(data['stepsize'] - 0.07) <= 1e-9].groupby(['bin'])
success = grouped['success']
success_mean = success.mean()
print(success_mean)
success_mean.plot.bar(title='ISPP: Success Rate per Level', figsize=(5,3))
plt.xlabel('Level Number')
plt.ylabel('Success Rate')
plt.tight_layout()
plt.savefig('figs/ispp-mean-success-beststep-bin.eps')
plt.show()