#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TransportTools, a library for massive analyses of internal voids in biomolecules and ligand transport through them
# Copyright (C) 2021  Jan Brezovsky, Aravind Selvaram Thirunavukarasu, Carlos Eduardo Sequeiros-Borja, Bartlomiej
# Surpeta, Nishita Mandal, Cedrix Jurgal Dongmo Foumthuim, Dheeraj Kumar Sarkar, Nikhil Agrawal  <janbre@amu.edu.pl>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__version__ = '0.9.0'
__author__ = 'Jan Brezovsky, Aravind Selvaram Thirunavukarasu, Carlos Eduardo Sequeiros-Borja, Bartlomiej Surpeta, ' \
             'Nishita Mandal, Cedrix Jurgal Dongmo Foumthuim, Dheeraj Kumar Sarkar, Nikhil Agrawal'
__mail__ = 'janbre@amu.edu.pl'


# this file contains an example of common custom analyses using outputs from the standard tt_engine workflow run
from transport_tools.libs import tools
from transport_tools.libs.config import AnalysisConfig
import numpy as np
import os
from logging import getLogger

logger = getLogger(__name__)

config = AnalysisConfig("config.ini")

# load outcomes from tt_engine run
mol_system = tools.load_checkpoint(os.path.join(config.get_parameter("output_path"), "_internal", "checkpoints",
                                                "stage010.dump"))

# how many open tunnels (radius > 1.4 A)  with minimal length of 10 A
os.makedirs(os.path.join("custom_analysis", "time_evolution_data"), exist_ok=True)
filters = tools.define_filters(min_length=10)
super_cluster_id = None  # analyze all superclusters
parameter = "bottleneck_radius"
dataset = mol_system.get_property_time_evolution_data(parameter, active_filters=filters,
                                                      sc_id=super_cluster_id)
for sc_id, sc_data in dataset.items():
    sc_overall_num_frames = len(sc_data.keys()) * config.get_parameter("snapshots_per_simulation")
    sc_overall_data = None
    for md_label, md_data in sc_data.items():  # per source MD simulation data
        if sc_overall_data is None:
            sc_overall_data = md_data
        else:
            sc_overall_data = np.concatenate((sc_overall_data, md_data))
        # saving data separately per MD simulation, can be later concatenated if a single set is desired
        with open(os.path.join("custom_analysis", "time_evolution_data",
                               "{}_{}_sc{}.txt".format(parameter, md_label, sc_id)), "w") as out_stream:
            for i, radii in enumerate(md_data):
                out_stream.write("{:6d} {:6.2f}\n".format(i + 1, radii))

    open_tunnels = (sc_overall_data >= 1.4)  # tunnels with min radius of 1.4 A
    max_value = np.max(sc_overall_data)
    how_many_open_tunnels = np.count_nonzero(open_tunnels)
    percent_open = how_many_open_tunnels * 100 / sc_overall_num_frames
    if how_many_open_tunnels > 0:
        logger.info("In supercluster {}:".format(sc_id))
        logger.info("{} of open tunnels {:.3f}%".format(how_many_open_tunnels, percent_open))
        logger.info("{:.3f} max radius".format(max_value))
        logger.info("-----------------------------------")

# visualizing open tunnels (radius > 1.4 A)  with minimal length of 10 A from supercluster 1, snapshots 100-200,
# with single reference pdb structure
visualization_output_folder = os.path.join("custom_analysis", "vis_details", "static")
filters = tools.define_filters(min_length=10, min_bottleneck_radius=1.4)
super_cluster_id = 1
md_labels = None  # all trajectories
start_snapshot = 100
end_snapshot = 200
mol_system.show_tunnels_passing_filter(super_cluster_id, filters, visualization_output_folder, md_labels=md_labels,
                                       start_snapshot=start_snapshot, end_snapshot=end_snapshot, trajectory=False)

# visualizing open tunnels (radius > 1.4 A)  with minimal length of 10 A from supercluster 1,  MD simulation
# md1 snapshots 100-200, including corresponding protein ensembles in pdb files
visualization_output_folder = os.path.join("custom_analysis", "vis_details", "dynamics")
filters = tools.define_filters(min_length=10, min_bottleneck_radius=1.4)
super_cluster_id = 1
md_labels = ["md1"]
start_snapshot = 100
end_snapshot = 200
mol_system.show_tunnels_passing_filter(super_cluster_id, filters, visualization_output_folder, md_labels=md_labels,
                                       start_snapshot=start_snapshot, end_snapshot=end_snapshot, trajectory=True)

# visualize particular tunnel from supercluster 1, MD simulation md1, snapshot 120
visualization_output_folder = os.path.join("custom_analysis", "vis_details", "1snapshot")
filters = tools.define_filters(min_length=10, min_bottleneck_radius=1.4)
super_cluster_id = 1
md_labels = ["md1"]
start_snapshot = end_snapshot = 120
mol_system.show_tunnels_passing_filter(super_cluster_id, filters, visualization_output_folder, md_labels=md_labels,
                                       start_snapshot=start_snapshot, end_snapshot=end_snapshot, trajectory=True)

