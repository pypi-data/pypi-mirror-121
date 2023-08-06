# Copyright The Jackson Laboratory, 2021
# authors: Jim Peterson, Abed Ghanbari
import os

class message_log:
    cumulative_message = ""
    verbose = True

    def __init__(self, verbose):
        self.verbose = verbose
        return

    def add_msg(self, msg, is_error_msg=False):
        self.cumulative_message += msg
        self.cumulative_message += os.linesep
        if self.verbose or is_error_msg:
            print(msg)
        return


    def save_log(self, file_path):
        with open(file_path, 'w') as f:
            f.write(self.cumulative_message)
        return
