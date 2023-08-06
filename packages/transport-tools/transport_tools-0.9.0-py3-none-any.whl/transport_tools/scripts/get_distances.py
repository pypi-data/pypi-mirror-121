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

import argparse

parser = argparse.ArgumentParser(description='Print distance between the two CAVER clusters clustered with TransportTools.')
parser.add_argument('clusterID1', type=int, help='ID of CAVER cluster 1')
parser.add_argument('mdlabel1', type=str, help='part of label of MD simulation with cluster 1')
parser.add_argument('clusterID2', type=int, help='ID of CAVER cluster 2')
parser.add_argument('mdlabel2', type=str, help='part of label of MD simulation with cluster 2')
parser.add_argument('matrixfile', type=str, help='file with pairwise cluster-cluster distances from transport_tools')
args = parser.parse_args()

with open(args.matrixfile , "r") as in_stream:
    header = list()
    for item in in_stream.readline().strip().split(",")[1:-1]:
        header.append((item.split(":")[0].strip(), item.split(":")[1].strip()))

    matrix = dict()
    line = in_stream.readline()
    while line:
        tmp_list = line.strip().split(",")
        tmp_label = tmp_list[0].split(":")
        label1 =  (tmp_label[0].strip(), tmp_label[1].strip())
        matrix[label1] = dict()
        for distance, label2 in zip(tmp_list[1:-1], header):
            matrix[label1][label2] = float(distance)
        line = in_stream.readline()

    full_mdlabel1 = None
    full_mdlabel2 = None
    cls1 = "cls{}".format(args.clusterID1)
    cls2 = "cls{}".format(args.clusterID2)

    for item in header:
        if args.mdlabel1 in item[0]:
            full_mdlabel1 = item[0]
        if args.mdlabel2 in item[0]:
            full_mdlabel2 = item[0]
    key1 = (full_mdlabel1, cls1)
    key2 = (full_mdlabel2, cls2)

    print("Distance between {} from {} and {} from {} = {}".format(cls1, full_mdlabel1, cls2, full_mdlabel2, matrix[key1][key2]))

