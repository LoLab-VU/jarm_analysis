from tropical.discretize_path import DomPath
from tropical.clustering import ClusterSequences
from tropical.plot_signatures import PlotSequences
from tropical.cluster_analysis import AnalysisCluster
from jnk3_no_ask1 import model
import numpy as np
import pickle

disc = DomPath(model, 'simulations_arrestin_jnk3.h5', target='s27', depth=7, dom_om=0.5)
path_signatures, path_labels = disc.get_path_signatures(cpu_cores=20, verbose=True, sample_simulations=5000)
np.save('dom_path_signatures_arrestin_kpars.npy', path_signatures)

with open('dom_path_labels_arrestin_kpars.pkl', 'wb') as f:
    pickle.dump(path_labels, f, pickle.HIGHEST_PROTOCOL)

# path_signatures = np.load('dom_path_signatures.npy')
cs = ClusterSequences(path_signatures)
cs.diss_matrix(n_jobs=20)
sil_df = cs.silhouette_score_agglomerative_range(cluster_range=20, n_jobs=20)
print(sil_df)
nclusters = sil_df.loc[sil_df['cluster_silhouette'].idxmax()].num_clusters
nclusters = int(nclusters)
cs.spectral_clustering(n_clusters=nclusters, n_jobs=20)
np.save('path_labels_depth7', cs.labels)

ps = PlotSequences(cs)
ps.plot_sequences(type_fig='modal', title='modal_path')
ps.plot_sequences(type_fig='trajectories', title='trajectories_path')
ps.plot_sequences(type_fig='entropy', title='modal_path')
#
# ac =AnalysisCluster(model, sim_results='simulations_ic_jnk3.h5', clusters=cs.labels)
# ac.plot_cluster_dynamics([27])
#
# jnk3 = model.monomers['JNK3']
# mkk4 = model.monomers['MKK4']
# mkk7 = model.monomers['MKK7']
# ac.plot_pattern_sps_distribution(pattern=jnk3, type_fig='bar', fig_name='jnk3_bar')
# ac.plot_pattern_sps_distribution(pattern=jnk3, type_fig='entropy', fig_name='entropy')
# ac.plot_pattern_sps_distribution(pattern=mkk4, type_fig='bar', fig_name='mkk4_bar')
# ac.plot_pattern_sps_distribution(pattern=mkk4, type_fig='entropy', fig_name='mkk4_entropy')
# ac.plot_pattern_sps_distribution(pattern=mkk7, type_fig='bar', fig_name='mkk7_bar')
# ac.plot_pattern_sps_distribution(pattern=mkk7, type_fig='entropy', fig_name='mkk7_entropy')
