from sink import Sink
from source import Source
import numpy as np

sou = Source(1)

#testArr = np.array([1, 1, 1, 0, 0, 0, 0, 0])
testArr = sou.text2bits("testfiles/Time.txt")

statistics_bits, encoded_bits  = sou.huffman_encode(testArr)
print "Encoded bits", encoded_bits
print


sink = Sink(1)

srcbits = sink.huffman_decode(encoded_bits, statistics_bits)

text = sink.bits2text(srcbits)

print 
print
print text

