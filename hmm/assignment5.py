#assignment5.py
#Heather Dykstra and Michael Aaron

import getopt, sys, pdb, math, string, copy

def main():
    try:
        optlist, remainder = getopt.getopt(sys.argv[1:],'p:o:')
        if len(optlist) == 0:
            print "***Options required***"
            usage()
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in optlist:
        if o == "-p":
            problemNumber = int(a)
        elif o == "-o":
	        hmmOrder = int(a)
    
    runHmm(problemNumber,hmmOrder)

def runHmm(problemNumber, hmmOrder):
    if problemNumber == 1:
        toyRobot(hmmOrder)
    elif problemNumber == 2:
        typoCorrection(hmmOrder)
    elif problemNumber == 3:
        topicChange(hmmOrder)
    else:
        print "No problem associated with number", problemNumber

def toyRobot(hmmOrder):
    #parse(robot_no_momentum.data)
    if hmmOrder == 1:
        #call first order hmm
        print("Functionality not implemented") 
    elif hmmOrder == 2:
	    #call first order hmm
        print("Functionality not implemented")
    else:
        print "No HMM with order", hmmOrder

def typoCorrection(hmmOrder): #the one I wrote
    #parse(typos10.data)
    if hmmOrder == 1:
        #call first order hmm
        print("Functionality not implemented") 
    elif hmmOrder == 2:
	    #call first order hmm
        print("Functionality not implemented")
    else:
        print "No HMM with order", hmmOrder

def topicChange(hmmOrder):
    if hmmOrder == 1:
        #call first order hmm
        print("Functionality not implemented") 
    elif hmmOrder == 2:
	    #call first order hmm
        print("Functionality not implemented")
    else:
        print "No HMM with order", hmmOrder



def parse(filename):
    f = open(filename, "r")
    testing = False
    traincorrect=[]
    trainincorrect=[]
    testcorrect=[]
    testincorrect=[]
    
    for line in f:
        l = line.split()
        if  l[0] == ".." :
            testing = True
            continue
        if not testing:
            traincorrect.append(l[0]) 
            trainincorrect.append(l[1])
        else:
            testcorrect.append(l[0]) 
            testincorrect.append(l[1])
            
    f.close()
    return traincorrect, trainincorrect, testcorrect, testincorrect



if __name__ == "__main__":
    main()
        
