# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import binascii
import random

import numpy as np
from collections import Counter
from Queue import PriorityQueue

class TreeNode:
    def __init__(self, symbol = None, left_child = None, right_child = None, parent = None):
        self.symbol = symbol
        self.left_child = left_child
        self.right_child = right_child
        self.parent = parent


class Sink:
    def __init__(self, compression):
        self.compression = compression
        print 'Sink:'

    def process(self, recd_bits):
        # Process the recd_bits to form the original transmitted
        # file. 
        # Here recd_bits is the array of bits that was 
        # passed on from the receiver. You can assume, that this 
        # array starts with the header bits (the preamble has 
        # been detected and removed). However, the length of 
        # this array could be arbitrary. Make sure you truncate 
        # it (based on the payload length as mentioned in 
        # header) before converting into a file.
        
        # If its an image, save it as "rcd-image.png"
        # If its a text, just print out the text
        
        #print '\tRecd', , 'source bits' # fill in here

        # Return the received source bits for comparison purposes
        return srcbits

    def bits2text(self, bits):
        # Convert the received payload to text (string)
        return  text

    def image_from_bits(self, bits,filename):
        # Convert the received payload to an image and save it
        # No return value required .
        pass

    def read_header(self, header_bits): 
        # Given the header bits, compute the payload length
        # and source type (compatible with get_header on source)
        # Get information for decompression if needed
 
        print '\tRecd header: ', # fill in here (exclude the extension)
        print '\tLength from header: ', # fill in here (length of the payload)
        print '\tSource type: ', # fill in here
        return srctype, payload_length, stat


    def search_huffman_node(self, node, curr_bits, decodings):
        if not node.left_child and not node.right_child:
            if node.parent:
                decodings[curr_bits] = node.symbol
            else:
                decodings[np.array([0], dtype=np.bool)] = node.symbol
        else:
            if node.left_child:
                new_bits = np.append(curr_bits, 0)
                self.search_huffman_node(node.left_child, new_bits, decodings)
            if node.right_child:
                new_bits = np.append(curr_bits, 1)
                self.search_huffman_node(node.right_child, new_bits, decodings)

    def create_huffman_decoding_map(self, root):
        decodings = {}
        self.search_huffman_node(root, np.array([], dtype=np.bool), decodings)
        return decodings

    def bits_from_int(self, number, symbol_length):
        return np.unpackbits([number])[0:symbol_length]

    def huffman_statistics(self, symbol_counts):
        symbol_probs = []
        total = 0
        for symbol in symbol_counts.keys():
            total += symbol_counts[symbol]

        for symbol in symbol_counts.keys():
            symbol_prob_tuple = (symbol, 1.0 * symbol_counts[symbol] / total)
            symbol_probs.append(symbol_prob_tuple)

        #Need to randomly shuffle for tie breaks

        return symbol_probs

    def huffman_decode(self, codedbits, stat):
        # Given the source-coded bits and the statistics of symbols,
        # decompress the huffman code and return the decoded source bits
        symbol_length = 4

         #Get probs on each symbol
        symbol_probs = self.huffman_statistics(stat)

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

        srcbits = self.rebuild_bit_string(self.create_huffman_deccoding_map(root), symbol_length)
        return srcbits
