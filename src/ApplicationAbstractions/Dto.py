# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-09-01 18:11:14$"

class DataTransferObject(object):

    def __init__(self, **kwargs):
        self.__dict__ = kwargs