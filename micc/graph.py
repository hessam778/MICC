import numpy as np
from copy import deepcopy
import curves as c
import itertools as it
import sys
from numba import autojit,jit

import logging

import numba.codegen.debug
#def disableNumbaLogging():

llvmlogger = logging.getLogger('numba.codegen.debug')
llvmlogger.setLevel(logging.INFO)


def shift(path):
	'''
	init

	'''
	temp = path.index(min(path))
	return path[temp:] + path[:temp]

def invert(path):
	'''
	init

	'''
	return shift(path[::-1])


rep_num = 1 #for beta only, fix for general distance

def loopDFS(current_node,start_node,graph,current_path,all_loops,nodes_to_faces):
	'''
	Recursively finds all closed cycles in a given graph that begin and end at start_node.
	As one would guess, it employs a standard depth-first search algorithm on the graph, 
	appending current_path to all_loops when it returns to start_node.

	In the overall distance computation, this function is computationally dominating with 
	exponential complexity, so take care with its use.

	:param self: 
	:type self: Graph
	:param current_node: the current alpha edge in the recursion
	:type current_node: int
	:param start_node: the source node of the current recursive search
	:type start_node: int
	:param graph: graph of the overall graph mid-recursion
	:type graph: dict<int,list<int> >
	:param current_path: list of nodes in the current path
	:type current_path: list<int>
	:param all_loops: list of all current paths
	:type all_loops: list< list<int> >
	:returns: set of all closeds cycles in the graph starting and ending at start_node

	'''
	#print 'path:',current_path
	if len(current_path) >= 3:
		path_head_3 = current_path[-3:]
		#path_head_2 = current_path[-2:]
		previous_three_faces =  [set(nodes_to_faces[edge]) for edge in path_head_3]
		#previous_two_faces =  [set(self.nodes_to_faces[edge]) for edge in path_head_2]
		#print 'ptf:',previous_three_faces[0],previous_three_faces[1],previous_three_faces[2]
		intersection_all = previous_three_faces[0]
		intersection_all = intersection_all.intersection(previous_three_faces[1])
		intersection_all = intersection_all.intersection(previous_three_faces[2])
		#intersection_all = set.intersection(*previous_three_faces) #old non numba
		if len(intersection_all) == 2:
			#print 'finished loop!',intersection_all
			return
	if current_node == start_node:
		all_loops.append(shift(list(current_path)))
		return

	else:
		for adjacent_node in set(graph[current_node]):
			if Graph.count(adjacent_node, current_path) < rep_num: #BETA ONLY, FIX FOR GENERAL DISTANCE
				current_path.append(adjacent_node)
				graph[current_node].remove(adjacent_node)
				graph[adjacent_node].remove(current_node)
				loopDFS(adjacent_node, start_node,deepcopy(graph), current_path, all_loops, nodes_to_faces)
				graph[current_node].append(adjacent_node)
				graph[adjacent_node].append(current_node)
				current_path.pop()


class Graph:

	def addNode(self,node):
		self.nodes[node] = []


	def __init__(self, curvePair, param_edges):
		
		self.nodes = {}
		self.counter = 0
		self.loops = []
		self.gammas = []
		self.nodes_to_faces = {}
		edges, __ =  curvePair.edges
		fourgons = [i[1] for i in edges if i[0] == 4  ]
		non_fourgons = [i[1] for i in edges if i[0] != 4  ]
		keys = self.nodes_to_faces.keys()
		for i,face in enumerate(non_fourgons):
			for node in face:
				if not node in keys:
					self.nodes_to_faces[node] = [i]
				else:
					self.nodes_to_faces[node].append(i)
				keys = self.nodes_to_faces.keys()
		for face in fourgons:
			for node in face:
				if not node in keys:
					self.nodes_to_faces[node] = [None]
				else:
					self.nodes_to_faces[node].append(None)

				keys = self.nodes_to_faces.keys()
		nodes = range(curvePair.n)

		for i in nodes:
			self.addNode(i)
		self.rep_num = 1
		self.findAllEdges(fourgons, non_fourgons, nodes, self.rep_num)
		graph_copy = deepcopy(self.nodes)
		proc_list = []
		for start_node in nodes:
			for adj_node in graph_copy[start_node]:
				loopDFS(start_node,adj_node,graph_copy,[start_node],self.loops, self.nodes_to_faces)

		self.loops = [list(j) for j in set([tuple(i) for i in self.loops])]
		__, edges = param_edges
		for path in list(self.loops):
			removed = False
			if len(path) < 3:
				if not removed:
					self.loops.remove(path)
					removed = True

			elif invert(path) in self.loops:
				if not removed:
					self.loops.remove(path)
					removed = True



			# Trial: remove all duplicates
			else:
				temp_path = list(path)
				temp_path = shift(temp_path)
				for face in non_fourgons:
					for triple in [temp_path[i:i+3] \
							for i in range(len(temp_path)-2)]:
						if set(triple) <= set(face):
							if not removed:
								self.loops.remove(path)
								removed = True

					temp_path = invert(temp_path)

					for triple in [temp_path[i:i+3] \
							for i in range(len(temp_path)-2)]:
						if set(triple) <= set(face):
							if not removed:
								self.loops.remove(path)
								removed = True

					for i in range(len(path)):
						temp_path = temp_path[1:] + temp_path[:1]

						for  triple in [temp_path[i:i+3] \
								for i in range(len(temp_path)-2)]:
							if set(triple) <= set(face) and path in self.loops:
								if not removed:
									self.loops.remove(path)
									removed = True

		for loop in list(self.loops):
			beta = list([list(curvePair.top),list(curvePair.bottom)])
			path = list(loop)
			path2 = list(path)
			path_matrix = c.buildMatrices(deepcopy(edges), [path])
			ladder = [list(path_matrix[0][0,:,1]),list(path_matrix[0][0,:,3])]
			gamma = c.curvePair(ladder[0],ladder[1],0, 0)
			if gamma.genus <= curvePair.genus:
				self.gammas.append(loop)

	def getValue(self,pos_to_insert, ladder, path):
		return	int(path[int(ladder[int(pos_to_insert)])])+1

	def findAllEdges(self, fourgons, non_fourgons, alphaEdgeNodes, rep_num):
		'''
		Determines all edges between boundary componenets and adds adjacencies between
		appropriate edges. 

		'''

		#find all direct connections between non-fourgon regions
		regions = fourgons + non_fourgons
		for alphaEdge in alphaEdgeNodes:
			for region in regions:
				if alphaEdge in region:
					region.remove(alphaEdge)
					for other_edge in region:
						self.addAdjacency(alphaEdge, int(other_edge), rep_num)
					region.add(alphaEdge)


	def addAdjacency(self,node, adjacentNode, rep_num):
		'''
		Adds adjacencies to a graph represented by an adjacency list.
		This is useful when we would like to replicate adjacencies 
		between nodes. 

		:param self:
		:type self: Graph
		:param node: node to add adjacency
		:param type: int
		:param adjacentNode: the adjacent node
		:type adjacentNode: int
		:param rep_num: set to 1
		:type rep_num: int

		'''
		for i in range(rep_num):
			adjacencyList = self.nodes[node]
			if Graph.count(adjacentNode, adjacencyList) < rep_num:
				adjacencyList.append(adjacentNode)

			adjacencyList = self.nodes[adjacentNode]
			if Graph.count(node, adjacencyList) < rep_num:
				adjacencyList.append(node)
	@staticmethod
	def count(adj_node, adj_list):
		'''
		Determines the number of adjacencies between two nodes in a graph, given the
		adjacency list of one of node.

		:param self:
		:type self: Graph
		:param adj_node: Adjacent node
		:type adj_node: int
		:param adj_list: Adjacency list of the node in question
		:type adj_list: list<int>
		:returns: number of edges from the adjacent node to the original node


		'''
		count = 0
		for i in adj_list:
			if i == adj_node:
				count += 1
		return count
	

'''
for i in range(len(path)):
	index = path[i]
	beta[0].insert(index+1,None)
	beta[1].insert(index+1,None)
	beta[0].append('____')
	beta[1].append('____')
	for j,tup in enumerate(zip(beta[0],beta[1])):

		t,b = tup
		if type(t) == str or type(b) == str: continue
		if t > index:
			beta[0][j] +=1
		if b > index:
			beta[1][j] +=1
	beta[0].remove('____')
	beta[1].remove('____')


	for j in range(len(path)):
		if path[j] > index:
			path[j] += 1
path.sort()
for i in range(len(path)):
	index = path[i]
	beta[0][index+1]=int(self.getValue(i,ladder[0],path))
	beta[1][index+1] =int(self.getValue(i,ladder[1],path))
'''
'''
count = {}
count[None] = 0
for i,j in zip(beta[0],beta[1]):
	if i in count.keys():
		count[i] += 1
	else:
		count[i] = 1
	if j in count.keys():
		count[j] += 1
	else:
		count[j] = 1
'''
