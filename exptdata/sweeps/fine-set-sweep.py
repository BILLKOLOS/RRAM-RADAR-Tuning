import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'blv', 'wlv', 'ri', 'rf']
stepsize = 0.1
data = pd.read_csv('data/set-sweep-bl-200ns-perlev-7-30-20.csv', delimiter='\t', names=names)
data = data[np.abs(data['blv']*10 % 1) <= 1e-9] # select points more sparsely
print data


# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times', size=13)


# Remove outliers
def is_outlier(s):
    lower_limit = s.mean() - (s.std() * 3)
    upper_limit = s.mean() + (s.std() * 3)
    return ~s.between(lower_limit, upper_limit)
data = data[~data.groupby(['blv','wlv'])['rf'].apply(is_outlier)]

# Set up variables
grouped = data.groupby(['blv', pd.cut(data['wlv'], np.arange(1.5, 3, 0.01))])

# Means of final resistance
rf = grouped['rf']
means = rf.mean()/1000.
stds = rf.std()/1000.

# Derivative and smoothing
pts = means.unstack().values[:,0]
x1, x2 = (1.4, 1.6)
xsi = (int(round((x1-0)/stepsize)), int(round((x2-0)/stepsize)))
y1, y2 = pts[xsi[0]], pts[xsi[1]]
print y1, y2
gradpw = (y2-y1)/(x2-x1)


# Plot
#title='SET BL Voltage Sweep', 
ax = means.unstack().plot(logy=False, xlim=(0, 3), ylim=(0, 15), linewidth=2, figsize=(4,3), yerr=stds.unstack()/2, elinewidth=0.75, zorder=0)
plt.annotate('Slope: %.1f k$\\Omega$/V' % gradpw, xy=(x1, y1), xytext=(x1+0.05, 13.5), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='center')
plt.xlabel('BL Voltage (V)')
plt.ylabel('Mean Resistance (k$\\Omega$)')
leg = plt.legend(["Range %i" % r for r in reversed(range(1,7))], ncol=1, columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 9})
plt.plot([5*x1-4*x2, 5*x2-4*x1], [y1-4*gradpw*(x2-x1), y2+4*gradpw*(x2-x1)], 'r:', zorder=10)
plt.text(1.3, 2, 'PW=200ns; VWL=varied', fontsize=11, horizontalalignment='center')
plt.tight_layout()
plt.savefig('figs/fine-set-sweep.eps')
plt.savefig('figs/fine-set-sweep.pdf')
plt.show()
