import numpy as np
import bokeh
import hvplot.pandas
import param
import os
import sklearn
import requests
import kshape
import pickle

from kshape.core import _sbd as sbd
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
import pandas as pd
import holoviews as hv
import panel as pn

pn.extension()

# Load data dictionary
def load_data():
    url = 'https://storage.googleapis.com/daves-new-bucket/organoid_viz_v2.pkl'

    print('Beginning file download with requests')

    r = requests.get(url)

    with open('/notebooks/organoid_viz_v2.pkl', 'wb') as f:
        f.write(r.content)
    
load_data()
with open('organoid_viz_v2.pkl', 'rb') as fp:
    viz_dict = pickle.load(fp)
    
class OrganoidExplorer(param.Parameterized):
    
    expts = list(viz_dict.keys())
    expt = param.ObjectSelector(default=expts[0], objects=expts)
    folder = param.ObjectSelector(default=list(viz_dict[expts[0]].keys())[0], 
                                  objects=list(viz_dict[expts[0]].keys()))
    color = param.ObjectSelector(default='Reds', objects=['Greys', 'Reds', 'Blues', 'Purples', 'Greens', 'Oranges'])
    
    @param.depends('expt', watch=True)
    def _update_folder(self):
        folders = list(viz_dict[self.expt].keys())
        self.param['folder'].objects = folders
        self.folder = folders[0]
    
    @param.depends('expt', 'folder', 'color')
    def plot(self):

        times_list = []
        counts_list = []
        
        times = viz_dict[self.expt][self.folder]['times']
        cell_counts = viz_dict[self.expt][self.folder]['cell_counts']
        Y = viz_dict[self.expt][self.folder]['linkage']
        
        # Plot dendrogram
        fig = plt.figure()
        
        ax_dendro = fig.add_axes([0.09, 0.1, 0.2, 0.8], frame_on = False)
        Z = sch.dendrogram(Y, orientation = 'left', color_threshold = 0.5*np.amax(Y[:,2]))

        ax_dendro.set_xticks([])
        ax_dendro.set_yticks([])
        
        # Plot growth curves
        ax_heatmap = fig.add_axes([0.3, 0.1, 0.6, 0.8], frame_on=False)
        
        index = Z['leaves']
        gc_ordered = cell_counts[index,:]
        extent = [0,times[0,-1],0,cell_counts.shape[0]-1]
        heatmap = ax_heatmap.matshow(gc_ordered, 
                                     aspect='auto',
                                     origin='lower',
                                     cmap=plt.get_cmap(self.color), 
                                     interpolation='none',
                                     extent=extent)
        ax_heatmap.xaxis.tick_bottom()
        fig.colorbar(heatmap, orientation='vertical')                
        ax_heatmap.set_yticks([])
        ax_heatmap.set_xlabel('Time (hours)')
        ax_heatmap.set_title('Organoid growth curve')
        plt.close(fig)
        return fig
            
explorer = OrganoidExplorer()
pn.Row(explorer.param, explorer.plot).servable()