import os.path
from configobj import ConfigObj


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


class ConfigurationManager(object):

    __ConfigurationSections = ()

    def __init__(self, appname):

        self.__configFilePath = os.path.expanduser("~/.config/.%s.ini" % appname)
        
        if not os.path.exists(self.__configFilePath):
            self.__CreateConfigurationFile()
        else:
            self.__Config = ConfigObj(self.__configFilePath)

    def __CreateConfigurationFile(self):

        configDir = os.path.dirname(self.__configFilePath)
        if not os.path.exists(configDir):
            os.mkdirs(configDir)

        with open(self.__configFilePath,'w'): pass
        self.__Config = ConfigObj(self.__configFilePath)
        
        self.__InitializeConfigurationFile()

    def __InitializeConfigurationFile(self):
        for section in self.__ConfigurationSections:
            self.__Config[section] = {}

    def GetSection(self, section):
        return self.__Config[section]

    def GetSections(self):
        return ( k for k in self.__Config.keys() )

    def GetValue(self, section, key):
        return self.__Config[section][key]

    def SetValue(self, section, key, value):
        if not self.__Config.has_key(section):
            self.__Config[section] = {}
            
        self.__Config[section][key] = str(value)

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.__Config.write()
