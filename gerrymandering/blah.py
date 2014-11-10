#Python 2.7 
#Gerrymandering AI Assignment
#Heather Dykstra and Michael Aaron
#This must have networkx installed to run

'''THINGS TO WRITE!
- take in a file  CHECK
- put the file into matrix CHECK
- ask user for max CHECK
- create An array of all contiguous regions for an n x n grid CHECK
- pick regions 
	- COMPLICATED
	- min /max  (Your rules need to follow the Minimax pseudocode found on page 166 of your textbook.)
	- check for contiguous solution possibility
	- don't forget to weigh each option...
	- threshold values
- return each district with each region's coordinate
- return district winners
- return overall winner
'''

import sys
import copy
import networkx as nx
import collections

def main():
	filename = sys.argv[1]
	infile = open(filename, "r")
	
	board = []
	
	#Input functions
	#Please do not adjust!
	maxi = raw_input('Who is max(r or d): ')
	newmax = str(maxi).upper()
	if newmax == 'R':
	    max_player = True #not sure this is right
	    #print("OKAY!")
	elif newmax == 'D':
	    max_player = False #not sure this is right
	    #print("OKAY!")
	else:
	    print("error")
	   
	#Read in the board   
	for line in infile:
		board.append(line.split())
	#Get a permutation of all "legal" moves
	allRegions = possibleRegions(board)
	#We need a set of sets to throw out the duplicates
	legalSet = set()
	for line in allRegions:
		#print line
		legalSet.add(frozenset(line))
	# print the sets
	#for x in legalSet:
	#	print x
	#print len(legalSet)
	#returns region and district winner?
	#PRINT IT ALL.
	gametree = nx.DiGraph()
	gametree.add_node(frozenset([]))
	build_gametree((frozenset([]),),legalSet, gametree, len(board[0])-1, board)
	print gametree.__len__()
	min_max(gametree, len(board[0]), max_player, (frozenset([]),))
	#for node in gametree.successors((frozenset([]),)):
	#   print("----")
	#   print(gametree.node[node])
	#   print(gametree.node[node]['weight'])
	   #print(min_max(node, 0, max_player))
	print ("-------------------")
	if max_player == True:
		print("MAX = R")
		print("MIN = D")
	else:
		print("MAX = D")
		print("MIN = R")
	i = 0
	results = min_max(gametree, len(board[0]), max_player, (frozenset([]),))
	results = list(results)
	for partition in results:
		print ("District "+str(i)+": "+ str(list(partition)))
		i+=1
	i = 0
	winner = 0
	for partition in results:
		if find_score_end(partition, board) > 0:
			print ("District "+str(i)+": D")
			winner+=1
		elif find_score_end(partition,board)< 0:
			print ("District "+str(i)+": R")
			winner-=1
		else:
			print ("District "+str(i)+": Tie")
		i+=1
	if winner > 0:
		print ("D wins!")
	elif winner <0:
		print ("R wins!")
	else:
		print ("Tie!")

def possibleRegions(board):
	#Seems like we want to built up a set, and covert it to a list to return
	matrix_length = len(board)
	#set of all possible partitions
	part_set = set()
	#Alright, we doin' this recursively, first we need to define in possibleRegions for access
	#possibleRegions variables
	def build_adj(cell, n):
		#basecase
		if n==0:
			part_set.add(tuple(adj_list))
		#UP, DOWN, LEFT, RIGHT
		transformed_cells = [(cell[0]-1,cell[1]), (cell[0]+1,cell[1]), (cell[0],cell[1]-1), (cell[0],cell[1]+1)]
		for tc in transformed_cells:
			if ((tc[0] >= 0) and (tc[1] >=0)): 
				if tc not in adj_list:
					try:
						board[tc[0]][tc[1]]
						adj_list[matrix_length-n] = tc
						build_adj(tc, n-1)
					except IndexError: 
						x = "out of bounds"
	#call build_adj for all cells in region
	i = 0
	while i<matrix_length:
		j = 0
		while j<matrix_length:
			#Weird python hack for recursion
			adj_list = range(matrix_length)
			adj_list[0] = (i,j)
			#Recursive call
			build_adj((i,j),matrix_length-1)
			j+=1
		i+=1
	return part_set


def min_max(gametree, depth, max_player, results):
	if depth==0:
		#print results
		return results
	if max_player:
		bestPick = -10000 #arbitrary, large neg num
		for node in gametree.successors(results):
			#pick = min_max(child, depth-1, False)
			if (gametree.node[node]['weight']>bestPick):
				bestPick = gametree.node[node]['weight']
				results = node
		#print "MAX "+str(bestPick)
		#print results
		results = min_max(gametree, depth-1, False, results)
			#bestValue = max(pick, bestValue)
	else:
		bestPick = 10000
		for node in gametree.successors(results):
			#pick = min_max(child, depth-1, False)
			if (gametree.node[node]['weight']<bestPick):
				bestPick = gametree.node[node]['weight']
				results = node
		#print "MIN "+str(bestPick)
		#print results
		results = min_max(gametree, depth-1, True, results)
	return results

def build_gametree(current_region, legal_set, tree,depth, board):
	#convert to list to allow for hashing shenanigans

	#master_legalList = list(legal_set)
	#def recursive_build():
	#i = 0
	#for move in legal_set:
	#	move_list.append(move)
	#	if depth!=0 and len(legal_set)!=0:
	#		build_gametree(region,legal_set,tree[i],depth-1)
	#Initalize the first level of the tree
	#create the new legal set of moves
	i = 0
	for move in legal_set:
		if depth==7:
			print str((float(i)/float(len(legal_set)))*100)+" percent done(ish)"
		region = current_region + (move,)
		tree.add_edge(current_region,region)
		new_legal_set = legal_set.copy()
		for partition in region:
			for cell in partition:
				for move in legal_set:
					if cell in move:
						try: 
							new_legal_set.remove(move)
						except KeyError:
							pass
		if (len(new_legal_set)!=0 and depth!=0):
			build_gametree(region,new_legal_set,tree, depth-1, board)
		if (depth==0):
			tree.node[region]['weight']=find_score(region, board)
		else:
			if len(tree.successors(region))==0:
				tree.remove_node(region)
			else:
				tree.node[region]['weight']=0
				for successor in tree.successors(region):
						tree.node[region]['weight']+=tree.node[successor]['weight']
		i+=1
	return


	#Alright, this might be so slow to be unusable, but we will
	#give it a shot.

#Finds the score of a region given 
def find_score(region, board):
	D_count = 0
	D_win = 0
	R_count = 0
	R_win = 0
	for partition in region:
		for cell in partition:
			if board[cell[0]][cell[1]] == "D":
				D_count = D_count+1
			else:
				R_count = R_count+1
		if R_count > D_count:
			R_win+=1
		elif D_count > R_count:
			D_win+=1
	return D_win-R_win

def find_score_end(partition, board):
	R_count = 0
	D_count = 0
	for cell in partition:
		if board[cell[0]][cell[1]] == "D":
			D_count += 1
		else:
			R_count += 1
	return D_count-R_count

main()