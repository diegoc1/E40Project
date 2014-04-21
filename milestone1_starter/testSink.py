from sink import Sink
from source import Source
import numpy as np

testArr = np.array([1, 0, 0, 0, 1, 1 ,0, 0, 0, 0])

sou = Source(1)
statistics_bits, encoded_bits  = sou.huffman_encode(testArr)

print statistics_bits, encoded_bits


