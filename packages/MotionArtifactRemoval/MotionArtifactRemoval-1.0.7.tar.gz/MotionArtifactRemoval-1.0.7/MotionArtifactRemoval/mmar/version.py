# Copyright The Jackson Laboratory, 2021
# authors: Jim Peterson, Abed Ghanbari

class version:
    major = 1
    minor = 0
    str = None
    def __init__(self):
        self.str = str(self.major) + "." + str(self.minor).zfill(3)
