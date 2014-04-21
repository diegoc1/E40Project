import numpy as np
import numpy as np
from collections import Counter
from Queue import PriorityQueue

class TreeNode:
	def __init__(self, symbol = None, left_child = None, right_child = None, parent = None):
		self.symbol = symbol
		self.left_child = left_child
		self.right_child = right_child
		self.parent = parent


class HuffmanEncoder:
	def __init__(self):
		return

	def huffman_encoding_map(self, symbol_counts):
        # Given the source bits, get the statistics of the symbols
        # Compress using huffman coding
        # Return statistics and the source-coded bits
		symbol_probs = self.huffman_probabilities(symbol_counts)

		#Use priority queue to keep track of least likely
		priority_queue = PriorityQueue()
		for tup in symbol_probs:
			priority_queue.put((tup[1], TreeNode(symbol=tup[0])))

        #Start building the tree
		while not priority_queue.empty():

			#Combine two smallest prob into a super node
			if priority_queue.qsize() >= 2:

				dq1 = priority_queue.get()
				dq2 = priority_queue.get()

				node1 = dq1[1]
				node2 = dq2[1]

				parent_node = TreeNode(left_child=node1, right_child=node2)
				node1.parent = parent_node
				node2.parent = parent_node

				#Insert parent into the priority queue
				new_prob = dq1[0] + dq2[0]
				priority_queue.put((new_prob, parent_node))

				root = parent_node

			else:
				dq = priority_queue.get()
				root = dq[1]


		encodings = {}
		self.search_huffman_node(root, np.array([], dtype=np.bool), encodings)
		return encodings

        # print "\tSource bit length: ", len(srcbits)
        # print "\tSource-coded bit length: ", # fill in here
        # print "\tCompression rate: ", # fill in here

	def search_huffman_node(self, node, curr_bits, encodings):
		if not node.left_child and not node.right_child:
			if node.parent:
			    encodings[node.symbol] = curr_bits
			else:
			    encodings[node.symbol] = np.array([0], dtype=np.bool)
		else:
			if node.left_child:
			    new_bits = np.append(curr_bits, 0)
			    self.search_huffman_node(node.left_child, new_bits, encodings)
			if node.right_child:
			    new_bits = np.append(curr_bits, 1)
			    self.search_huffman_node(node.right_child, new_bits, encodings)

	def bits_from_int(self, number, symbol_length):
		return np.unpackbits([number])[0:symbol_length]

	def huffman_counts(self, arr, symbol_length):
		if symbol_length > 8:
			print "Error: symbol length must be less than 8 bits"
			return Counter()

        #Track counts for each bit
		symbol_counts = Counter()

		i = 0
		while i <= len(arr) - symbol_length:

            #Retrieve the number associated with bit pattern
			symbol = np.packbits(arr[i: i+symbol_length])[0]
			if symbol_counts[symbol]:
				symbol_counts[symbol] += 1
			else: symbol_counts[symbol] = 1

			i += symbol_length

		return symbol_counts


	def huffman_probabilities(self, symbol_counts):
		symbol_probs = []
		total = 0
		for symbol in symbol_counts.keys():
			total += symbol_counts[symbol]

		for symbol in symbol_counts.keys():
			symbol_prob_tuple = (symbol, 1.0 * symbol_counts[symbol] / total)
			symbol_probs.append(symbol_prob_tuple)
		return symbol_probs