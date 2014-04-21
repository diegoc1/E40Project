# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import binascii
import random

import numpy as np

from huffman_encoder import HuffmanEncoder




class Source:
    def __init__(self, monotone, filename=None, compress=False):
        self.monotone = monotone
        self.fname = filename
        self.compress = compress
        #print 'Source: '

    def process(self):
        # Form the databits, from the filename
        srctype = 0
        if self.fname is not None:
            if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
                # Its an image
                srctype = 1
                srcbits = self.bits_from_image(self.fname)
            else:           
                # assume it's text
                srctype = 2
                srcbits = self.text2bits(self.fname)

        else:  
            # Send monotone (the bits are all 1s for monotone bits)
            srcbits = np.ones(self.monotone)      

        encoding_response = self.huffman_encode(srcbits)

        header_bits = self.get_header(srcbits.size, srctype, encoding_response[0])
        payload = encoding_response[1]
        databits = np.concatenate((header_bits, payload))

        # Perform Huffman coding if the compression option is on
        # compress will be to be False if you send monotone
        # (handled in sendrecv.py)

        print '\tSource type: ', # fill in here
        print '\tPayload Length: ', # fill in here
        print '\tHeader: ', # fill in here (exclude the extension)

        # srcbits is the bit sequence representing source data
        # payload is the data part that is sent over the channel
        # databits is the bit sequence that is sent over the channel (including header)
        return srcbits, payload, databits

    def text2bits(self, filename):
        # Given a text file, convert to bits
        with open(filename, 'r') as f:
            lines = f.read().split('\n')
        bit_array = np.array([], bool)
        for line in lines:
            for ch in line:
                int_val = ord(ch)
                char_bits = np.unpackbits(np.array([int_val], dtype=np.uint8))
                bit_array = np.append(bit_array, char_bits)
        return bit_array            


    def bits_from_image(self, filename):
        # Given an image, convert to bits
        img = Image.open(filename)
        bit_array = np.array([], bool)

        img_arr = np.array(img.getdata(), numpy.uint8)
        for pix_tup in img_arr:
            pix_val = pix_tup[0]
            pix_bits = np.unpackbits(np.array([pix_val], dtype=np.uint8))
            bit_array = np.append(bit_array, pix_bits)
        return bit_array            

    def get_header(self, payload_length, srctype, stat):
        # Given the payload length and the type of source 
        # (image, text, monotone), form the header
        # Add header-extension if needed 
        data = np.array([[payload_length], [srctype]], dtype=np.uint8)
        header_bits = np.unpackbits([data])
        header_bits = np.concatenate((header_bits, stat))

        # header_bits = np.append(header_bits, stat)

        return header_bits


    

    def huffman_encode(self, srcbits):
        # Given the source bits, get the statistics of the symbols
        # Compress using huffman coding
        # Return statistics and the source-coded bits
        symbol_length = 4

         #Get probs on each symbol
        encoder = HuffmanEncoder()
        symbol_counts = encoder.huffman_counts(srcbits, symbol_length)
        encoding_map = encoder.huffman_encoding_map(symbol_counts)

        encoded_bits = self.rebuild_bit_string(encoding_map, srcbits, symbol_length)


        print "\tSource bit length: ", len(srcbits)
        print "\tSource-coded bit length: ", len(encoded_bits)
        print "\tCompression rate: ", 1.0 * len(encoded_bits) / len(srcbits)

        return self.symbol_count_bit_array(symbol_counts), encoded_bits

        


    def symbol_count_bit_array(self, symbol_counts):
        bit_array = np.array([], dtype=np.bool)
        for symbol in symbol_counts.keys():
            symbol_bits = np.unpackbits(np.array([symbol], dtype=np.uint8))
            count = symbol_counts[symbol]
            count_bits = np.unpackbits(np.array([count], dtype=np.uint8))

            #Append symbol and then count
            bit_array = np.append(bit_array, symbol_bits)
            bit_array = np.append(bit_array, count_bits)

        return bit_array.astype(np.bool)


    def rebuild_bit_string(self, huffman_map, srcbits, symbol_length):
        new_bit_string = np.array([])

        i = 0
        while i <= len(srcbits) - symbol_length:

            #Retrieve the number associated with bit pattern
            symbol = np.packbits(srcbits[i: i+symbol_length])[0]
            huffman_encoded_bits = huffman_map[symbol]
            new_bit_string = np.append(new_bit_string, huffman_encoded_bits)
            print "Converting", srcbits[i: i+symbol_length], "to", huffman_encoded_bits
            i += symbol_length
        
        left_over_bits = srcbits[i:]
        new_bit_string = np.append(new_bit_string, left_over_bits)
        

        return new_bit_string

        

         