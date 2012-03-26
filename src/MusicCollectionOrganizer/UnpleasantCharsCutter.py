'''
Created on 2010-06-26

@author: gregorl
'''



class UnpleasantCharactersCutter(object):

    UnpleasantCharacters = r""",'"~.'`:;\/?][)("""

    def cutUnpleasantCharacters(self, s):
        return "".join([c for c in s.strip() if c not in self.UnpleasantCharacters])