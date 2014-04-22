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
		self.symbol_length = 4

	################################################
	#Methods shared by encoding and decoding
	################################################

	def format_bit_array(self, array):
		return array.astype(bool).astype(int)

	def huffman_encoding_tree(self, symbol_counts):
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
		return root

	def bits_from_int(self, number):
		return np.unpackbits([number])[0:self.symbol_length]

	def huffman_probabilities(self, symbol_counts):
		symbol_probs = []
		total = 0
		for symbol in symbol_counts.keys():
			total += symbol_counts[symbol]

		for symbol in symbol_counts.keys():
			symbol_prob_tuple = (symbol, 1.0 * symbol_counts[symbol] / total)
			symbol_probs.append(symbol_prob_tuple)
		return symbol_probs

	################################################
	#Methods for encoding only
	################################################

	def huffman_encoding_map(self, symbol_counts):

		encodings = {}
		if len(symbol_counts.keys()):
			root = self.huffman_encoding_tree(symbol_counts)		
			self.search_huffman_node_encoding(root, np.array([], dtype=np.uint), encodings)

		print "Building encoding map..."
		for key in encodings.keys():
			print "\t--> Mapped " + str(key) + " (" + str(self.bits_from_int(key)) + ") to " + str(encodings[key])
		print

		return encodings

	def search_huffman_node_encoding(self, node, curr_bits, encodings):
		if not node.left_child and not node.right_child:
			if node.parent:
			    encodings[node.symbol] = curr_bits
			else:
			    encodings[node.symbol] = np.array([0], dtype=np.uint)
		else:
			if node.left_child:
			    new_bits = np.append(curr_bits, 0)
			    self.search_huffman_node_encoding(node.left_child, new_bits, encodings)
			if node.right_child:
			    new_bits = np.append(curr_bits, 1)
			    self.search_huffman_node_encoding(node.right_child, new_bits, encodings)


	def huffman_counts(self, arr):
		if self.symbol_length > 8:
			print "Error: symbol length must be less than 8 bits"
			return Counter()

        #Track counts for each bit
		symbol_counts = Counter()

		i = 0
		while i <= len(arr) - self.symbol_length:

            #Retrieve the number associated with bit pattern
			symbol = np.packbits(arr[i: i+self.symbol_length])[0]
			if symbol_counts[symbol]:
				symbol_counts[symbol] += 1
			else: symbol_counts[symbol] = 1

			i += self.symbol_length

		return symbol_counts, len(arr) % self.symbol_length

	def build_bit_string_with_encoding_map(self, huffman_map, srcbits):
		new_bit_string = np.array([])
		print "Building bit string from encoding map..."
		i = 0
		while i <= len(srcbits) - self.symbol_length:

			#Retrieve the number associated with bit pattern
			symbol = np.packbits(srcbits[i: i+self.symbol_length])[0]
			huffman_encoded_bits = huffman_map[symbol]
			new_bit_string = np.append(new_bit_string, huffman_encoded_bits)
			#print "\t--> Converting", srcbits[i: i+self.symbol_length], "to", huffman_encoded_bits
			i += self.symbol_length

		left_over_bits = srcbits[i:]
		new_bit_string = np.append(new_bit_string, left_over_bits)

		print
		return new_bit_string

	def create_symbol_count_bit_array(self, symbol_counts, unencoded_count):
		bit_array = np.array([], dtype=np.uint)

		#Append number of non-encoded bits at front
		unencoded_count_bits = np.unpackbits(np.array(unencoded_count, dtype=np.uint8))
		bit_array = np.append(bit_array, unencoded_count_bits)

		for symbol in symbol_counts.keys():
			symbol_bits = np.unpackbits(np.array([symbol], dtype=np.uint8))
			count = symbol_counts[symbol]
			count_bits = np.unpackbits(np.array([count], dtype=np.uint8))

			#Append symbol and then count
			bit_array = np.append(bit_array, symbol_bits)
			bit_array = np.append(bit_array, count_bits)

		return bit_array.astype(np.uint)

	################################################
	#Methods for decoding only
	################################################

	def symbol_counts_from_statistics_bits(self, statistics_bits):

		symbol_counts = {}

		unencoded_count_bits = statistics_bits[0:8].astype(np.uint8)
		unencoded_count = np.packbits(unencoded_count_bits)[0]
		
		print"Retrieving statistics..."
		print "\tFound " + str(unencoded_count) + " unencoded bits"
		print

		i = 8;

		while i < len(statistics_bits):
			symbol_bits = statistics_bits[i:i+8].astype(np.uint8)
			symbol_int = np.packbits(symbol_bits)[0]

			count_int_bits = statistics_bits[i+8:i+16].astype(np.uint8)
			count = np.packbits(count_int_bits)[0]

			symbol_counts[symbol_int] = count

			i += 16 #jump 2 ints
		return symbol_counts, unencoded_count

	def huffman_decoding_map(self, symbol_counts):
		decodings = {}

		if len(symbol_counts.keys()):
			root = self.huffman_encoding_tree(symbol_counts)
			self.search_huffman_node_decoding(root, np.array([], dtype=np.uint), decodings)

		print "Building encoding map..."
		for key in decodings.keys():
			#print "\t--> Mapped " + key + " to " + str(decodings[key])
			pass
		print

		return decodings

	def search_huffman_node_decoding(self, node, curr_bits, decodings):
		if not node.left_child and not node.right_child:
			if node.parent:
				decodings[str(self.format_bit_array(curr_bits))] = self.bits_from_int(node.symbol)
			else:
			    decodings[str(self.format_bit_array(np.array([0], dtype=np.uint)))] =  self.bits_from_int(node.symbol)
		else:
			if node.left_child:
			    new_bits = np.append(curr_bits, 0)
			    self.search_huffman_node_decoding(node.left_child, new_bits, decodings)
			if node.right_child:
			    new_bits = np.append(curr_bits, 1)
			    self.search_huffman_node_decoding(node.right_child, new_bits, decodings)

	def build_bit_string_from_decoding_map(self, decoding_map, codedbits, unencoded_count):
		#Decode bit by bit
		srcbits = np.array([], dtype=np.uint)

		i = 0
		curr_bits = np.array([], dtype=np.uint)

		print "Mapping encoded bits..."
		print "Coded bits: " + str(codedbits)

		while i < len(codedbits) - unencoded_count:
			curr_bits = self.format_bit_array(np.append(curr_bits, codedbits[i]))
			curr_bits_key = str(curr_bits)

			if curr_bits_key not in decoding_map:
				pass
				#print "\t--> No match for " + curr_bits_key

			else:
				#Decode and append to srcbits
				srcbits = np.concatenate((srcbits, decoding_map[curr_bits_key]))

				#print "\t--> Matched " + curr_bits_key + " to " + str(decoding_map[curr_bits_key])

				#Reset curr_bits
				curr_bits = np.array([])

			i += 1
				

		#Append whatever's left over (unencoded bits)
		srcbits = np.concatenate((srcbits, curr_bits, codedbits[i:]))
		print
		return self.format_bit_array(srcbits)


	