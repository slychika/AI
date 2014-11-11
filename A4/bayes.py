#python2.7
#Heather Dykstra and Michael Aaron
#Bayes Net

#! /usr/bin/env python2.7

import getopt, sys
from numpy import *
from pbnt.Graph import *
from pbnt.Distribution import *
from pbnt.Node import *
from pbnt.Inference import *

try:
    from IPython import embed
except:
    pass

def main():
    #Import arguments and parse into options.
    try:
        optlist, remainder = getopt.getopt(sys.argv[1:], 'j:g:m:vh')
        #If no arguments profided
        if len(optlist) == 0:
            print "***Options required***"
            usage()
  #if inappropriate argument provided
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in optlist:
        if o == "-h":
            usage()
        elif o == "-m":
            # Return the Marginal probability
            print a
            pass
        elif o == "-g":
            # Return the Conditional probability
            print a
            pass
        elif o == "-j":
            # Return the Joint probability
            print a
            pass

    #Initialize the Cancer Bayes Network
    numberOfNodes = 5
    #name the nodes
    pollution = 0
    smoker = 1
    cancer = 2
    xray = 3
    dysponea = 4

    pNode = BayesNode(0, 2, name="pollution")
    sNode = BayesNode(1, 2, name="smoker")
    cNode = BayesNode(2, 2, name = "cancer")
    xNode = BayesNode(3, 2, name="xray")
    dNode = BayesNode(4, 2, name="dysponea")

    #pollution
    pNode.add_child(cNode)

    #smoker
    sNode.add_child(cNode)

    #cancer
    cNode.add_parent(pNode)
    cNode.add_parent(sNode)
    cNode.add_child(xNode)
    cNode.add_child(dNode)

    #xray
    xNode.add_parent(cNode)

    #dysponea
    dNode.add_parent(cNode)

    nodes = [pNode, sNode, cNode, xNode, dNode]

    #create distributions
  
    #pollution distribution
    pDistribution = DiscreteDistribution(pNode)
    pindex = pDistribution.generate_index([],[])
    pDistribution[pindex] = [0.9, 0.1] #[low, high]
    pNode.set_dist(pDistribution)
    
    #smoker distruibution
    sDistribution = DiscreteDistribution(sNode)
    sindex = sDistribution.generate_index([],[])
    sDistribution[sindex] = [0.3, 0.7] #[true, false]
    sNode.set_dist(sDistribution)

    #cancer distruibution
    #note: high =1, low =0, pos = 1, neg =0
    cdist = zeros([pNode.size(), sNode.size(), cNode.size()], dtype=float32)
    cdist[0,0,] = [0.001,0.999]  #low, false [true,false]
    cdist[0,1,] = [0.03,0.97]    #low, true [true, false]
    cdist[1,0,] = [0.02,0.98]    #high, false [true, false]
    cdist[1,1,] = [0.05,0.95]    #high, true [true, false]
    cDistribution = ConditionalDiscreteDistribution(nodes=[pNode, sNode, cNode], table=cdist)
    cNode.set_dist(cDistribution)
    
    #xray distruibution 
    xdist = zeros([cNode.size(), xNode.size()], dtype = float32)
    xdist[0,] = [0.20, 0.80] #neg [true, false]
    xdist[1,] = [0.90, 0.10] #pos [true, false]
    xDistribution = ConditionalDiscreteDistribution(nodes = [cNode, xNode], table = xdist)
    xNode.set_dist(xDistribution)
    
    #dysponea distruibution
    ddist = zeros([cNode.size(), dNode.size()], dtype = float32)
    ddist[0,] = [0.30, 0.70] #false [true, false]
    ddist[1,] = [0.65, 0.35] #true [true, false]
    dDistribution = ConditionalDiscreteDistribution(nodes = [cNode, dNode], table = ddist)
    dNode.set_dist(dDistribution)
    
    #create bayes net
    isCancer = BayesNet(nodes)
    for node in isCancer.nodes:
        if node.id == 0:
            pollution = node
        if node.id == 1:
            smoker = node
        if node.id == 2:
            cancer = node
        if node.id == 3:
            xray = node
        if node.id == 4:
            dysponea = node


def usage():
  print """
  Usage:
  ---
    Flags
    -g  conditional probablity
    -j  joint probability
    -m  marginal probability
    -h  help
  ---
    Input
    P  Polution   (p = low,  ~p = high)
    S  Smoker     (s = true, ~s = false)
    C  Cancer     (c = true, ~c = false)
    D  Dyspnoea   (d = true, ~d = false)
    X  X-Ray      (x = positive, ~x = negative)
  ---
    Example
    python bayesnet.py -jPSC
    (joint probabilities for Pollution, Smoker, and Cancer)
    python bayesnet.py -j~p~s~c
    (joint probability for pollution = h, smoker = f, cancer = f)
    python bayesnet.py -gc|s
    (conditional probability for cancer given that someone is a smoker)
  """
  sys.exit(2)

if __name__ == "__main__":
    main()
