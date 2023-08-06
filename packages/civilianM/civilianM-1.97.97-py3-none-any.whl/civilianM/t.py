from __init__ import *
from  tiger import *
upgrade()
print(getAddress())
a = test()
if a == None:
    raise LibraryError("sb")
