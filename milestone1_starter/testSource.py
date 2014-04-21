from source import Source
import numpy as np


s = Source(10, "testfiles/Truth.txt", True)
srcbits, payload, databits =  s.process()
print "srcbits: ", srcbits
print
print
print "payload: ", payload
print
print
print "databits", databits

