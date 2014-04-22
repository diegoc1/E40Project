from sink import Sink
from source import Source
import numpy as np

sou = Source(1)
sink = Sink(1)

#testArr = np.array([1, 0, 0, 0, 1])
testArr = sou.bits_from_image("testfiles/32pix.png")

statistics_bits, encoded_bits  = sou.huffman_encode(testArr)

srcbits = sink.huffman_decode(encoded_bits.astype(np.uint), statistics_bits)

final_arr = sink.image_from_bits(srcbits, "testfiles/test_img.png")

print 
print
print "Final result", srcbits

