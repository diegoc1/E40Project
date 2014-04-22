from sink import Sink
from source import Source
import numpy as np
from common_srcsink import hamming

compress = True
sou = Source(1, "testfiles/columns.png", compress)
sink = Sink(compress)

a, b, c = sou.process()
srcbits = sink.process(c)


# #testArr = np.array([1, 1, 1, 0, 0, 0, 0, 0])
# testArr = sou.text2bits("testfiles/Time.txt")

# statistics_bits, encoded_bits  = sou.huffman_encode(testArr)
# print len(encoded_bits)

# print "Encoded bits", encoded_bits
# print

# sink = Sink(1)

# srcbits = sink.huffman_decode(encoded_bits, statistics_bits)

# text = sink.bits2text(srcbits)


# print 
# print
# print text

# print
# print
print len(srcbits)
print 
print hamming(srcbits, a)

