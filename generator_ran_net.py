#!/usr/bin/python
#generator_ran_net.py

import sys

import random as ran
from math import log

import numpy as np
import networkx as nx

import input_net as inet
import updating_rule as ur
import time_evol as tev
import info_dyn as info


################# begin : global_random_network (ER net) ########################
def global_random_network(net): #generate a random network with the global constraint from the input network(net)#
   
   #### 0. obtain global constraint from the input network(net) ####
    nbrInhibition = 0 # the total number of inhibition links except self inhibition
    nbrActivation = 0 # the total number of activitaion links except self activation
    selfInhibition = set() # a set of nodes which have a self inhibition link
    selfActivation = set() # a set of nodes which have a self activation link
    for u,v in net.edges_iter():
        if u == v:
            if net[u][v]['weight'] >= 1:
                selfActivation.add(u)
            if net[u][v]['weight'] <= -1:
                selfInhibition.add(u)
        elif net[u][v]['weight'] >= 1:
            nbrActivation += 1
        else:
            nbrInhibition += 1
    #*inhibit 15 activation 8*#

    #### 1. generate a random network ####
    gr_net = nx.DiGraph() #empty network object for a new global random net == > ER network
    gr_net.add_nodes_from(net.nodes(data=True)) #add nodes labelled as same as ones in the biological network
 
    #edge link weights for activation and inhibition
    inhibit = [-2,-2,-3,-2,-3,-2,-2,-2,-2,-3,-4,-1,-1,-2,-3,-1,-3,-1,-3,-1,-2,-1,-1,-2,-1,-1,-1,-1]
    activate = [1,2,1,1,2,1,1,2,1,2,2,2,3,1,2,1,1,1,2,2,3,1]

    ran.shuffle(activate)
    ran.shuffle(inhibit)
 

    ## 1-1) select a random pair of nodes to connect and repeat until the same number of activation and inhibition links are connected in gr_net
    i = 0
    while ( i < nbrActivation):
        u,v = ran.sample(net.nodes(), 2)
        if not gr_net.has_edge(u,v) and u != v:
            wa = activate[i]
            gr_net.add_edge(u,v,weight=wa)
            i += 1

    i = 0
    while ( i < nbrInhibition):
        u,v = ran.sample(net.nodes(), 2)
        if not gr_net.has_edge(u,v) and u != v:
            wi = inhibit[i]
            gr_net.add_edge(u,v,weight=wi)
            i += 1

    
    ## 1-2) add self activition or self inhibition links in gr_net to the same nodes as in biological network

    for u in selfActivation:
        gr_net.add_edge(u,u,weight=1.0)
    for u in selfInhibition:
        gr_net.add_edge(u,u,weight=-1.0)

    return gr_net
################# end : global_random_network ########################


################# begin : local_random_network ########################
def local_random_network(net): #generate a random network with the local constraint from the input network(net)#

    lr_net = net.copy() # lr_net == > local constraint random network ==> scale-free network
    
    inhibition_edges = set() # a set of inhibition edges for lr_net
    activation_edges = set() # a set of activation edges for lr_net
    self_edges = set() # a set of self edges for lr_net

    #### 1. initialize the sets for different type of edges same as ones for biological network ####
    for u, v in net.edges_iter():
        if u == v:
            self_edges.add((u,v))
        elif net[u][v]['weight'] >= 1:
            activation_edges.add((u,v))
        else:
            inhibition_edges.add((u,v))


    nbrInhibition = len(inhibition_edges) # the total number of inhibition links except self inhibition
    nbrActivation = len(activation_edges) # the total number of activitaion links except self activation
    nbrSumEdges = nbrInhibition + nbrActivation # the total number of edges except self links

    #print nbrInhibition, nbrActivation, nbrSumEdges
    #print inhibition_edges
    #print activation_edges
    #### 2. decide how many edges swap will be made to generate one scale-free network or lr_net ####
    exchangingEdgeNbr = int( 1.0 * nbrSumEdges * nbrSumEdges / 2.0 ) #number of attempts for exchaning edges to make one local random graph.

    #print exchangingEdgeNbr    

    inhibit = [-2,-2,-3,-2,-3,-2,-2,-2,-2,-3,-4,-1,-1,-2,-3,-1,-3,-1,-3,-1,-2,-1,-1,-2,-1,-1,-1,-1]
    activate = [1,2,1,1,2,1,1,2,1,2,2,2,3,1,2,1,1,1,2,2,3,1]

    ran.shuffle(activate)
    ran.shuffle(inhibit)

    #### 3. LOOP for different attempt of exchanging edges for one local random network
    exchanged = 0
    for i in range(0, exchangingEdgeNbr):
        ## 3-1) Select type of edges between inhibition and activation
        ranNbr = ran.choice(range(nbrActivation + nbrInhibition))

        #print ranNbr

        if ranNbr < nbrInhibition:
            selected_weight = inhibit[ranNbr]
            #print selected_weight
        else:
            selected_weight = activate[ranNbr-nbrInhibition]
            #print selected_weight

        ## 3-2) Choose two different edges with the selected type.
        if selected_weight <= -1:
            e1, e2 = ran.sample(inhibition_edges,2)
        if selected_weight >= 1:
            e1, e2 = ran.sample(activation_edges,2)


        ## 3-3) Check if (u,z) not in edges and (w,v) not in edges
        #  if True : exchange two edges from (u,v)  and (w,z) to (u,z) and (w,v)
        #               ==> remove (u,v)  and (w,z) from lr_net and the set of correponding edges and add (u,z) and (w,v) to the network and the set
        #  if False : don't change anything
        
        u = e1[0]
        v = e1[1]
        w = e2[0]
        z = e2[1]


        #print 'u',u,'v',v,'w',w,'z',z
        if not lr_net.has_edge(u, z) and not lr_net.has_edge(w,v) and v!= w  and u!= z:
            
            exchanged += 1

            lr_net.remove_edges_from([(u,v),(w,z)])
            lr_net.add_weighted_edges_from([(u,z, selected_weight),(w,v,selected_weight)])
            if selected_weight >= 1:
                activation_edges.remove((u,v))
                activation_edges.remove((w,z))
                activation_edges.add((u,z))
                activation_edges.add((w,v))

            if selected_weight <= -1:
                inhibition_edges.remove((u,v))
                inhibition_edges.remove((w,z))
                inhibition_edges.add((u,z))
                inhibition_edges.add((w,v))

    return lr_net
################# end : local_random_network ########################


def main(argv):
    cmdargs = str(sys.argv)
    #print cmdargs
    # EDGE_FILE
    EDGE_FILE = str(sys.argv[1])
    # NODE_FILE
    NODE_FILE = str(sys.argv[2])
    # Damage True or False
    damage = int(sys.argv[3])
    
    net = inet.read_network_from_file(EDGE_FILE, NODE_FILE)
    nodes_list = inet.build_nodes_list(NODE_FILE)
    
    nbrRanNet = 100 # the number of random networks
    
    #generate global random networks (ER nets)#
    for i in range(0, nbrRanNet):
        result_file = open('results/random/global_%d/p53_%d-gr%03d.dat'%(damage,damage,i), 'w')
        gr_net = global_random_network(net)
        for u, v in gr_net.edges_iter():
            result_file.write('%s\t%s\t%d\n'%(u, v, gr_net[u][v]['weight']))
    
    #generate local random networks (SF nets)#
    for i in range(0, nbrRanNet):
        result_file = open('results/random/local_%d/p53_%d-lr%03d.dat'%(damage,damage,i), 'w')
        lr_net = local_random_network(net)
        for u, v in lr_net.edges_iter():
            result_file.write('%s\t%s\t%d\n'%(u, v, lr_net[u][v]['weight']))
    
if __name__=='__main__':
    main(sys.argv[1:])

