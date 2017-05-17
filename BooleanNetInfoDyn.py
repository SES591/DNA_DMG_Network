#!/usr/bin/python
#BooleanNetInfoDyn.py

__author__ = '''Hyunju Kim'''

import sys
#import os
#import random as ran
#from math import log
#from optparse import OptionParser, OptionGroup
#from scipy import *
#import matplotlib.pyplot as plt
import numpy as np
#import itertools
from collections import defaultdict
#import operator
from collections import OrderedDict

import input_net as inet
import updating_rule as ur
import time_evol as tev
import info_dyn as info


def Bool_info(EDGE_FILE,NODE_FILE,maxStep,historyLength,network_filename):
   net = inet.read_network_from_file(EDGE_FILE, NODE_FILE)
   nodes_list = inet.build_nodes_list(NODE_FILE)
   Nbr_States = 2 # the number of all possible states of a node
   
   timeSeries_Type = ['all_initial'] # 'all_initial', 'primary_attractor', 'one_trajectory'

   if 'all_initial' in timeSeries_Type:
       Nbr_All_Initial_States = np.power(Nbr_States, len(nodes_list)) # the number of initial states of the network
       timeSeriesAll = tev.time_series_all(net, nodes_list, Nbr_All_Initial_States, Nbr_States, maxStep) # To generate time series data over all possible initial states
        
       result_ai_all = open('ai-all-step%d-h%d-%s.dat'%(maxStep, historyLength,network_filename),'w')

       AI_all = {}
       count_max = len(nodes_list)
       count = 1
       for n in nodes_list:
           AI_all[n] = info.compute_AI(timeSeriesAll[n], historyLength, Nbr_All_Initial_States, Nbr_States)
           result_ai_all.write('%s\t%f\n'%(n, AI_all[n]))
           sys.stdout.write("Computing AI:  %d%% \r"%(100.0*count/count_max))
           sys.stdout.flush()
           count+=1
           #print n, AI_all[n]
           
       result_te_all = open('te-all-step%d-h%d-%s.dat'%(maxStep, historyLength,network_filename),'w')

       count_max = len(nodes_list)**2
       count = 1
       print '\n' 
       TE_all =  defaultdict(float)
       for v in nodes_list:
           for n in nodes_list:
               TE_all[(v, n)] = info.compute_TE(timeSeriesAll[v], timeSeriesAll[n], historyLength, Nbr_All_Initial_States, Nbr_States)
               result_te_all.write('%s\t%s\t%f\n'%(v, n,TE_all[(v, n)] ))
               sys.stdout.write("Computing TE:  %d%% \r"%(100.0*count/count_max))
               sys.stdout.flush()
               count+=1
               #print v, n,TE_all[(v, n)]

def main(argv):
   ## 1. Network Information from Data File ##
   cmdargs = str(sys.argv)
   #print cmdargs
   # EDGE_FILE
   EDGE_FILE = str(sys.argv[1])
   # NODE_FILE
   NODE_FILE = str(sys.argv[2])
   # Number of Steps
   maxStep = int(sys.argv[3])
   # History length
   historyLength = int(sys.argv[4])
   # Output filename
   network_filename = str(sys.argv[5])

   Bool_info(EDGE_FILE,NODE_FILE,maxStep,historyLength,network_filename)

if __name__=='__main__':
    main(sys.argv[1:])
