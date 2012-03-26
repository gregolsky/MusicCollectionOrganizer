# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-08-28 09:30:32$"

import shutil
import os

class FileMover(object):

    def __init__(self):
        pass

    @staticmethod
    def MoveFile(file=None, destination=None):
        if not file and not destination:
            return;
        else:
            shutil.move(file, destination)

