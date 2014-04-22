# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import binascii
import random

import numpy as np
from huffman_encoder import HuffmanEncoder


class Sink:
    def __init__(self, compression):
        self.compression = compression
        print '----- Sink: -----'

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

        
        srctype, payload_length, stat = self.read_header(recd_bits)
        payload_bits = recd_bits[-payload_length:]

        if self.compression:
            srcbits = self.huffman_decode(payload_bits, stat)
        else:
            srcbits = payload_bits

        if (srctype == 0):
            print "Monotone"
        elif (srctype == 1):
            self.image_from_bits(srcbits, "rcd-image.png")
        elif (srctype == 2):
            print self.bits2text(srcbits)

        return srcbits

    def bits2text(self, bits):
        # Convert the received payload to text (string)
        text = ''

        i = 0
        while i < len(bits):
            char_bits = bits[i:i+8]
            ord_val = np.packbits(char_bits)
            ch = chr(ord_val)
            text += ch
            i += 8
        return text

    def image_from_bits(self, bits, filename):
        # Convert the received payload to an image and save it
        # No return value required .
        pixel_values = np.array([], dtype=np.uint)

        #Retrieve length of each row
        row_length_bits = bits[0:8]
        row_length = np.packbits(row_length_bits)[0]

        print "Forming image from bits..."
        print "Row length bits: " + str(row_length_bits)
        print "\tFound row length of " + str(row_length)
        print

        pixel_idx = 8
        while pixel_idx < len(bits):

            pixel_bits = bits[pixel_idx:pixel_idx+8]
            pixel_value = np.packbits(pixel_bits)[0]
            pixel_values = np.append(pixel_values, pixel_value)

            pixel_idx += 8 #int

        img = Image.new('L', (len(pixel_values) / row_length, row_length)) 
        img.putdata(pixel_values)
        img.save(filename)

        print pixel_values


    def getIntFromBinaryArr(self, numpyArr):
        numpyArr = numpyArr.astype(int)
        bit_array = numpyArr.tolist()
        bit_string = ''.join(str(bin_num) for bin_num in bit_array)
        return int(bit_string, 2)

    def read_header(self, header_bits): 
        # Given the header bits, compute the payload length
        # and source type (compatible with get_header on source)
        # Get information for decompression if needed
        srctype = self.getIntFromBinaryArr(header_bits[0:2])
        payload_length = self.getIntFromBinaryArr(header_bits[2:18])
        if self.compression:
            stat_length = self.getIntFromBinaryArr(header_bits[18:34])
            stat = header_bits[34:34+stat_length]
        else:
            stat = None

        print '\tRecd header: ', # fill in here (exclude the extension)
        print '\tLength from header: ', # fill in here (length of the payload)
        print '\tSource type: ', # fill in here


        return srctype, payload_length, stat



    
    

    def huffman_decode(self, codedbits, stat):
        # Given the source-coded bits and the statistics of symbols,
        # decompress the huffman code and return the decoded source bits

        decoder = HuffmanEncoder()

        #Build statistics
        symbol_counts, unencoded_count = decoder.symbol_counts_from_statistics_bits(stat)

        #Get decoding map
        decoding_map = decoder.huffman_decoding_map(symbol_counts)

        #Decode using map
        srcbits = decoder.build_bit_string_from_decoding_map(decoding_map, codedbits, unencoded_count)

        return srcbits







