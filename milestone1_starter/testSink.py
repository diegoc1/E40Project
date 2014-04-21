from sink import Sink
from source import Source
import numpy as np

testArr = np.array([1, 0, 0, 0, 1, 1 ,0, 0, 0, 0])

sou = Source(1)
counts = sou.huffman_counts(testArr, 4)
bit_string = sou.huffman_encode(testArr)[1]
print 
s = Sink(1)
print s.huffman_decode(bit_string, counts)

