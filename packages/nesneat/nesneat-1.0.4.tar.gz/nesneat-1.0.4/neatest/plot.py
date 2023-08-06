import glob
import argparse
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot(log_paths, smooth=1):
    sns.set(style="darkgrid", font_scale=1.5)
    estimator = getattr(np, 'mean')
    for log_path in log_paths:
        if os.path.isfile(log_path):
            logs = [log_path]
        else:
            logs = glob.glob(os.path.join(log_path, '*.csv'))
        data = [pd.read_csv(f) for f in logs]
        if smooth > 1:
            y = np.ones(smooth)
            for datum in data:
                x = np.asarray(datum['Reward'])
                z = np.ones(len(x))
                smoothed_x = np.convolve(x,y,'same') / np.convolve(z,y,'same')
                datum['Reward'] = smoothed_x

        data = pd.concat(data, ignore_index=True)
        data = data.astype({"Generation": int, "Algorithm": str,
                            'Seed': int, 'Reward': float})
        ax = sns.lineplot(x="Generation", y="Reward", hue="Algorithm",
                         data=data, ci='sd', estimator=estimator)

        plt.legend(loc='best').set_draggable(True)
        plt.tight_layout(pad=0.5)
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('log_paths', type=str, nargs='+', help='Log Path to Plot')
    parser.add_argument('--smooth', required=False, type=int, default=1,
                        help='Smoothing Coefficient')
    args = parser.parse_args()
    plot(args.log_paths, args.smooth)
