#!/usr/bin/python
#bioinfo.py

__author__ = '''Hyunju Kim'''

#import os
import sys
import numpy as np
import networkx as nx
from collections import OrderedDict

import input_net as inet
import updating_rule as ur


################# BEGIN: decimal_to_binary(nodes_list, decState, Nbr_States=2) ########################
def decimal_to_binary(nodes_list, decState, Nbr_States=2): # more left in the nodes list means higher order of 2 in binary
    biStates = {}
    x = len(nodes_list) -1
    for u in nodes_list:
        biStates[u] = decState / np.power(Nbr_States, x)
        decState = decState % np.power(Nbr_States, x)
        x = x - 1
    return biStates
################# END: decimal_to_binary(nodes_list, decState, Nbr_States=2) ########################


################# BEGIN: binary_to_decimal(nodes_list, biStates, Nbr_States=2) ########################
def binary_to_decimal(nodes_list, biStates, Nbr_States=2):  # more left in the nodes list means higher order of 2 in binary
    decState = 0
    x = len(nodes_list) -1
    for u in nodes_list:
        decState = decState + biStates[u]  * np.power(Nbr_States, x)
        x = x - 1
    return decState
################# END: binary_to_decimal(nodes_list, biStates, Nbr_States=2) ########################


################# BEGIN: biological_sequence(net, nodes_list, bio_initStates, fileName, damage, Nbr_States=2) ########################
def biological_sequence(net, nodes_list, bio_initStates, fileName, damage, Nbr_States=2):
    bioSeq = []
    currBiStates = bio_initStates
    finished = False
    while(not finished):
        oneDiff = 0
        prevBiStates = currBiStates.copy()
        bioSeq.append(prevBiStates)
        currBiStates = ur.sigmoid_updating(net, prevBiStates, damage)
        for u in nodes_list:
            if abs(prevBiStates[u] - currBiStates[u]) > 0:
                oneDiff = 1
                break
        finished = (oneDiff < 1)

    OUTPUT_FILE  = open(fileName, 'w')
    OUTPUT_FILE.write('time step')
    for u in nodes_list:
        OUTPUT_FILE.write('\t%s'%(u))
    OUTPUT_FILE.write('\n')

    for i in range(len(bioSeq)):
        OUTPUT_FILE.write('%d'%i)
        for u in nodes_list:
            OUTPUT_FILE.write('\t%d'%(bioSeq[i][u]))
        OUTPUT_FILE.write('\n')
    #return bioSeq
################# END: biological_sequence(net, nodes_list, bio_initStates, fileName, damage, Nbr_States=2) ########################


################# BEGIN: time_series_all(net, nodes_list, damage, Nbr_Initial States, Nbr_States=2, MAX_TimeStep=20, Transition_Step=0) ########################
def time_series_all(net, nodes_list, Nbr_Initial_States, Nbr_States, MAX_TimeStep=20):
    
    '''
        Description:
        -- compute TE for every pair of nodes using distribution from all possible initial conditions or an arbitrary set of initial conditions
        
        Arguments:
        -- 1. net
        -- 2. nodes_list
        -- 3. Initial_States_List
        -- 4. Nbr_States
        -- 5. MAX_TimeStep
        
        Return:
        -- 1. timeSeriesData
    '''
    
    #Nbr_Nodes = len(net.nodes())
    #Nbr_All_Initial_States = np.power(Nbr_States, Nbr_Nodes)
    
    timeSeriesData = {}
    for n in net.nodes():
        timeSeriesData[n] = {}
        for initState in range(Nbr_Initial_States):
            timeSeriesData[n][initState] = []
    
    for initDecState in range(Nbr_Initial_States):
        currBiState = decimal_to_binary(nodes_list, initDecState, Nbr_States)
        for step in range(MAX_TimeStep):
            prevBiState = currBiState.copy()
            for n in nodes_list:
                timeSeriesData[n][initDecState].append(prevBiState[n])
            currBiState = ur.sigmoid_updating(net, prevBiState)

    return timeSeriesData
################# END: time_series_all(net, nodes_list, Nbr_States=2, MAX_TimeStep=20) ########################


################# BEGIN: net_state_transition_map(net, nodes_list, Nbr_States=2) ########################
def net_state_transition(net, nodes_list, Nbr_States=2):

    '''
    Arguments:
               1. net
               2. nodes_list
               4. Nbr_States
    Return:
               1. decStateTransMap
    '''
    
    Nbr_Nodes = len(net.nodes())
    Nbr_All_Initial_States = np.power(Nbr_States, Nbr_Nodes)
    
    decStateTransMap = nx.DiGraph()
    for prevDecState in range(Nbr_All_Initial_States):
        prevBiState = decimal_to_binary(nodes_list, prevDecState, Nbr_States)
        currBiState = ur.sigmoid_updating(net, prevBiState)
        currDecState = binary_to_decimal(nodes_list, currBiState, Nbr_States)
        decStateTransMap.add_edge(prevDecState, currDecState)
    return decStateTransMap
################# END: net_state_transition_map(net, nodes_list, Nbr_States=2) ########################


################# BEGIN: find_attractor_old(decStateTransMap) ########################
def find_attractor_old(decStateTransMap):
    
    '''
        Arguments:
        1. decStateTransMap
        Return:
        1. attractor
    '''
    attractor_list = nx.simple_cycles(decStateTransMap) #in case of deterministic system, any cycle without considering edge direction will be directed cycle.
    attractors = {}
    attractors['fixed'] = []
    attractors['cycle'] = []

    for u in attractor_list:
        if len(u) == 1:
            attractors['fixed'].append(u)
        else:
            attractors['cycle'].append(u)

    return attractors
################# END: find_attractor_old(decStateTransMap) ########################


################# BEGIN: attractor_analysis(decStateTransMap) ########################
def find_attractor(decStateTransMap):
    
    '''
        Arguments:
            -- 1. decStateTransMap
        Return:
            -- attractor
    '''
    attractor_list = nx.simple_cycles(decStateTransMap) #in case of deterministic system, any cycle without considering edge direction will be directed cycle.
    attractors = {}
    #attractors['fixed'] = []
    #attractors['cycle'] = []
    
    undirectedMap = nx.DiGraph.to_undirected(decStateTransMap)
    
    for u in attractor_list:
        attractors[u[0]] = {}
        if len(u) == 1:
            attractors[u[0]]['type'] = 'fixed'
        else:
            attractors[u[0]]['type'] = 'cycle'

    for v in attractors.iterkeys():
        basin = nx.node_connected_component(undirectedMap, v)
        attractors[v]['basin'] = basin
        attractors[v]['basin-size'] = len(basin)
    
    sorted_attractors = OrderedDict(sorted(attractors.items(), key=lambda kv: kv[1]['basin-size'], reverse=True))
    return sorted_attractors
################# END: attractor_analysis(decStateTransMap) ########################


################# BEGIN: time_series_pa(net, nodes_list, Initial_States_List, Nbr_States=2, MAX_TimeStep=20) ########################
def time_series_pa(net, nodes_list, Initial_States_List, Nbr_States, MAX_TimeStep=20):
    
    '''
        Description:
        -- compute TE for every pair of nodes using distribution from all initial conditions that converge to the primary or biological attractor
        
        Arguments:
        -- 1. net
        -- 2. nodes_list
        -- 3. Initial_States_List
        -- 4. Nbr_States
        -- 5. MAX_TimeStep
        
        Return:
        -- 1. timeSeriesData (only for primary attractor)
    '''
    timeSeriesData = {}
    for n in net.nodes():
        timeSeriesData[n] = {}
        for initState in range(len(Initial_States_List)):
            timeSeriesData[n][initState] = []
    
    for initState in range(len(Initial_States_List)):
        initDecState = Initial_States_List[initState]
        currBiState = decimal_to_binary(nodes_list, initDecState, Nbr_States)
        for step in range(MAX_TimeStep):
            prevBiState = currBiState.copy()
            for n in nodes_list:
                timeSeriesData[n][initState].append(prevBiState[n])
            currBiState = ur.sigmoid_updating(net, prevBiState)

    return timeSeriesData
################# END: time_series_pa(net, nodes_list, Nbr_States=2, MAX_TimeStep=20) ########################


################# BEGIN: time_series_one(net, nodes_list, Initial_State, Nbr_States=2, MAX_TimeStep=20) ########################
def time_series_one(net, nodes_list, Initial_State, Nbr_States, MAX_TimeStep=20):
    
    '''
        Description:
        -- compute TE for every pair of nodes using distribution from all initial conditions that converge to the primary or biological attractor
        
        Arguments:
        -- 1. net
        -- 2. nodes_list
        -- 3. Initial_States_List
        -- 4. Nbr_States
        -- 5. MAX_TimeStep
        
        Return:
        -- 1. timeSeriesData (only for primary attractor)
    '''
    
    
    timeSeriesData = {}
    for n in net.nodes():
        timeSeriesData[n] = {}
        timeSeriesData[n][0] = []
    
 
    currBiState = Initial_State
    for step in range(MAX_TimeStep):
        prevBiState = currBiState.copy()
        for n in nodes_list:
            timeSeriesData[n][0].append(prevBiState[n])
        currBiState = ur.sigmoid_updating(net, prevBiState)

    return timeSeriesData
################# END: time_series_one(net, nodes_list, Initial_State, Nbr_States=2, MAX_TimeStep=20) ########################

def edge_print(EDGE_FILE,NODE_FILE,attractor_filename,ran_type,damage):

    net = inet.read_network_from_file(EDGE_FILE,NODE_FILE)
    nodes_list = inet.build_nodes_list(NODE_FILE)

    initState = 1
    biStates = decimal_to_binary(nodes_list, initState)
    #print 'initial state', biStates

    decStateTransMap = net_state_transition(net, nodes_list,Nbr_States=2)
   
    # Exports network and attractor landscape for use in cytoscape.
    nx.write_graphml(net,"results/random/%s_%d/network-%s.graphml"%(ran_type,damage,attractor_filename))
    nx.write_graphml(decStateTransMap,"results/random/%s_%d/attractors-%s.graphml"%(ran_type,damage,attractor_filename))
    
    attractor_file = 'results/random/%s_%d/attractors-%s.txt'%(ran_type,damage,attractor_filename)
   
    # Prints out all attractors
    attractors = find_attractor_old(decStateTransMap)
    print attractors
    print '\n'
    with open(attractor_file,'a') as f:
        f.write('%s'%(attractors))
        f.write('\n')
        # Prints out the fixed attractors for the network with values in a matrix format.    
        f.write('*** fixed ***\n') 
        for a in attractors['fixed']:
            biState = decimal_to_binary(nodes_list,a)
            b = []
            c = []
            keymaster = []
            for key, values in biState.items():
                b.append(values)
                keymaster.append(key)
                c = np.concatenate(b, axis=0)
            size = len(a)
            d = np.transpose(c.reshape((len(nodes_list),size)))
            print a
            print d, '\n'
            print keymaster, '\n'
            f.write('%s\n'%(a))
            f.write('%s\n'%(keymaster))
            f.write('%s\n'%(d))
            f.write('\n')
        f.write('\n')
            
        # Prints out the cyclic attractors for the network with values in a matrix format.
        f.write('*** cyclic ***\n')
        for a in attractors['cycle']:
            biState = decimal_to_binary(nodes_list,a)
            b = []
            c = []
            keymaster = []
            for key, values in biState.items():
                b.append(values)
                keymaster.append(key)
                c = np.concatenate(b, axis = 0)
            size = len(a)
            d = np.transpose(c.reshape((len(nodes_list),size)))
            print a
            print d, '\n'
            print keymaster, '\n'
            f.write('%s\n'%(a))
            f.write('%s\n'%(keymaster))
            f.write('%s\n\n'%(d))
        f.write('\n')
    return

def main(argv):

    print ("time_evol module is the main code.")
    cmdargs = str(sys.argv)
    print cmdargs
    # EDGE_FILE
    EDGE_FILE = str(sys.argv[1])
    # NODE_FILE
    NODE_FILE = str(sys.argv[2])
    filename = str(sys.argv[3])
    ran_type = str(sys.argv[4])

    edge_print(EDGE_FILE,NODE_FILE,filename,ran_type)
            
if __name__=='__main__':
    main(sys.argv)
