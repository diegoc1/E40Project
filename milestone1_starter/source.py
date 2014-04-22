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
        print '----- Source: -----'

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

        if self.compress:
            encoding_response = self.huffman_encode(srcbits)
            header_bits = self.get_header(srcbits.size, srctype, encoding_response[0])
            payload = encoding_response[1]
            databits = np.concatenate((header_bits, payload))
            return srcbits, payload, databits
        
        return srcbits, srcbits, srcbits 

        

        # Perform Huffman coding if the compression option is on
        # compress will be to be False if you send monotone
        # (handled in sendrecv.py)

        print '\tSource type: ', # fill in here
        print '\tPayload Length: ', # fill in here
        print '\tHeader: ', # fill in here (exclude the extension)

        # srcbits is the bit sequence representing source data
        # payload is the data part that is sent over the channel
        # databits is the bit sequence that is sent over the channel (including header)
        

    def text2bits(self, filename):
        # Given a text file, convert to bits
        with open(filename, 'r') as f:
            lines = f.read().split('\n')
        bit_array = np.array([], bool)
        for i, line in enumerate(lines):
            for ch in line:
                int_val = ord(ch)
                char_bits = np.unpackbits(np.array([int_val], dtype=np.uint8))
                bit_array = np.append(bit_array, char_bits) 
            if i != (len(lines) - 1):
                n_int_val = ord('\n')
                n_char_bits = np.unpackbits(np.array([n_int_val], dtype=np.uint8))
                bit_array = np.append(bit_array, n_char_bits)
        return bit_array            


    def bits_from_image(self, filename):
        # Given an image, convert to bits
        img = Image.open(filename)
        bit_array = np.array([], bool)

        img_arr = np.array(img.getdata(), numpy.uint8)

        #We decided to encode the length of each row to be more robust
        #Works for even non 32x32 files
        row_length = img.size[1]
        row_length_bits = np.unpackbits(np.array([row_length], dtype=np.uint8))
        bit_array = np.append(bit_array, row_length_bits)
        print bit_array

        for pix_tup in img_arr:
            pix_val = pix_tup[0]
            pix_bits = np.unpackbits(np.array([pix_val], dtype=np.uint8))
            bit_array = np.append(bit_array, pix_bits)

        return bit_array            

    def get_header(self, payload_length, srctype, stat):
        # Given the payload length and the type of source 
        # (image, text, monotone), form the header
        # Add header-extension if needed 

        #Add payload bits to header
        payload_bits = np.binary_repr(payload_length)
        header_bits = [int(char) for char in payload_bits]
        if len(header_bits) < 16:
            for i in range(16 - len(header_bits)):
                header_bits.insert(0, 0)

        #Add source type bits to header
        type_bits = np.binary_repr(srctype)
        if (len(type_bits) == 1):
            header_bits.insert(0, int(type_bits[0]))
            header_bits.insert(0, 0)
        elif (len(type_bits) == 2):
            header_bits.insert(0, int(type_bits[1]))
            header_bits.insert(0, int(type_bits[0]))
        else:
            print "Header Error: src_type is not valid"

        #Add stat size bits to header
        imgSize = 0
        statSize = len(stat)
        stat_size_bit_string = np.binary_repr(statSize)
        stat_size_bits = [int(char) for char in stat_size_bit_string]
        if len(stat_size_bits) < 16:
            for i in range(16 - len(stat_size_bits)):
                stat_size_bits.insert(0, 0)
        header_bits = np.array(header_bits, np.uint8)
        header_bits = np.concatenate((header_bits, stat_size_bits))

        #Add stat data bits
        header_bits = np.concatenate((header_bits, stat))

        return header_bits

    def huffman_encode(self, srcbits):
        # Given the source bits, get the statistics of the symbols
        # Compress using huffman coding
        # Return statistics and the source-coded bits

         #Get probs on each symbol
        encoder = HuffmanEncoder()
        symbol_counts, unencoded_count = encoder.huffman_counts(srcbits)
        encoding_map = encoder.huffman_encoding_map(symbol_counts)

        encoded_bits = encoder.build_bit_string_with_encoding_map(encoding_map, srcbits)

        print "Compression statistics from encoding..."
        print "\tSource bit length: ", len(srcbits)
        print "\tSource-coded bit length: ", len(encoded_bits)
        print "\tCompression rate: ", 1.0 * len(encoded_bits) / len(srcbits)
        print

        return encoder.create_symbol_count_bit_array(symbol_counts, unencoded_count), encoded_bits


    

        

         