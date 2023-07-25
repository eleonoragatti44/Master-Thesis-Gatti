import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def bifurcation_point(df_cen):
    """df_cen needs to be already"""
    repl0 = df_cen[df_cen['cue_reached']==0].replicate
    repl1 = df_cen[df_cen['cue_reached']==1].replicate

    traj0 = df_cen[df_cen.replicate.isin(repl0)]
    traj1 = df_cen[df_cen.replicate.isin(repl1)]

    for i in range(int(traj0.time.max())):
        mean1, sigma1 = stats.norm.fit(traj0[traj0.time==i*50].y.to_numpy())
        mean2, sigma2 = stats.norm.fit(traj1[traj1.time==i*50].y.to_numpy())
        if (abs(mean1 - mean2) > (sigma1+sigma2)):
            x_bif0 = traj0[traj0.time==i*50].x.mean()
            x_bif1 = traj1[traj1.time==i*50].x.mean()
            #print('time:', 50*i)
            break
    return (x_bif0+x_bif1)/2, (sigma1+sigma2)/2

def draw_bifurcation(df_cen, df_tar, ax):
    #fig, ax = plt.subplots(figsize=(6,6))
    for i in range(df_cen.replicate.max()+1):
        ax.plot(df_cen.loc[df_cen.replicate==i,:].x, df_cen.loc[df_cen.replicate==i,:].y, c='black', alpha=0.3)
    ax.scatter(df_tar.loc[df_tar.id==0,:].x, df_tar.loc[df_tar.id==0,:].y, c='r', s=100)
    ax.scatter(df_tar.loc[df_tar.id==1,:].x, df_tar.loc[df_tar.id==1,:].y, c='r', s=100)
    x_bif, s = bifurcation_point(df_cen)
    ax.plot([0,x_bif],[500,500], color='r')
    ax.plot([x_bif, df_tar.loc[df_tar.id==0,:].x],[500, df_tar.loc[df_tar.id==0,:].y], color='r')
    ax.plot([x_bif, df_tar.loc[df_tar.id==1,:].x],[500, df_tar.loc[df_tar.id==1,:].y], color='r')
    