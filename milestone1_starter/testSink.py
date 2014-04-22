from sink import Sink
from source import Source
import numpy as np

testArr = np.array([1, 0, 0, 0, 1])

sou = Source(1)
statistics_bits, encoded_bits  = sou.huffman_encode(testArr)
sink = Sink(1)
srcbits = sink.huffman_decode(encoded_bits.astype(np.uint), statistics_bits)

print 
print
print "Final result", srcbits

