import numpy as np
import math
import operator

# Methods common to both the transmitter and receiver.
def hamming(arr1,arr2):
    # Given two binary vectors s1 and s2 (possibly of different 
    # lengths), first truncate the longer vector (to equalize 
    # the vector lengths) and then find the hamming distance
    # between the two. Also compute the bit error rate  .
    # BER = (# bits in error)/(# total bits )
    #Truncate longer of the two arrays
	if len(arr1) != len(arr2):
		shorter_len = min(len(arr1), len(arr2))
		arr1 = arr1[0:shorter_len]
		arr2 = arr2[0:shorter_len]
	dist = 0
	for i in xrange(len(arr1)):
		if arr1[i] != arr2[i]:
			dist = dist + 1
	return dist, (1.0 * dist) / len(arr1)