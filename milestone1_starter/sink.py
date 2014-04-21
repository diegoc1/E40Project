# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import binascii
import random

import numpy as np


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


    

    def huffman_decode(self, codedbits, stat):
        # Given the source-coded bits and the statistics of symbols,
        # decompress the huffman code and return the decoded source bits
        srcbits = np.array([0, 0, 1])
        return srcbits
