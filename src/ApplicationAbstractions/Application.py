# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-08-20 14:15:51$"

class Application(object):

    def __init__(self):
        self.ConfigurationManager = None
        self._ApplicationConfigurationInitialize()
        self._ApplicationInit()

    def _ApplicationInit(self):
        raise NotImplementedError()

    def _ApplicationStart(self):
        raise NotImplementedError()

    def _ApplicationError(self, error):
        raise NotImplementedError()

    def _ApplicationEnd(self):
        raise NotImplementedError()

    def _ApplicationOnErrorDeinitialize(self):
        raise NotImplementedError()

    def _ApplicationConfigurationInitialize(self):
        pass

    def ApplicationMain(self):

            try:
                self._ApplicationConfigurationInitialize()

                if self.ConfigurationManager:
                    with self.ConfigurationManager:
                        self._ApplicationStart()
                        self._ApplicationEnd()
                else:
                    print "Warning: __ApplicationConfigurationInitialize may need overriding. ConfigurationManager has not been initialized"
                    self._ApplicationStart()
                    self._ApplicationEnd()
                    
            except Exception as exception:
                self._ApplicationError(exception)
                
            finally:
                self._ApplicationOnErrorDeinitialize()