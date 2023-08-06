import time
from threading import Thread
from python_helper import Constant as c
from python_helper import log, ObjectHelper
import globals
from ouvidoria_unidombosco.api.src.UnidomboscoNightmare import UnidomboscoNightmare
from ouvidoria_unidombosco.api.src.UnidomboscoHell import UnidomboscoHell
from ouvidoria_unidombosco import OuvidoriaBasePath


URL = "https://www.unidombosco.edu.br/ouvidoria/"

HEADERS = {
  'authority': 'www.unidombosco.edu.br',
  'content-type': 'application/x-www-form-urlencoded',
  'referer': 'Sorry, this is the only way for me to be heard'
}


class Unidombosco:

    def __init__(self, *args, filePath=OuvidoriaBasePath.MODULE_FILE, globalsInstance=None, headless=True, logDebug=False, logInfo=False, **kwargs):
        self.unidomboscoNightmareArgs = args
        self.unidomboscoNightmareKwargs = kwargs
        self.globalsInstance = globalsInstance if ObjectHelper.isNotNone(globalsInstance) else globals.newGlobalsInstance(filePath
            , successStatus = True
            , infoStatus = logInfo
            , settingStatus = True
            , debugStatus = logDebug
            , warningStatus = True
            , failureStatus = True if logDebug else False
            , errorStatus = True
            , logStatus = False
        )
        self.headless = headless
        # processes = []
        # for instance in range(instances):

    def runNightmare(self, message: str, studentRegistry: str, name: str, email: str, phoneNumber: str, cpf: str, url: str = URL, instances: int = 4):
        for instanceIndex in range(instances if self.headless else 1):
            nightmare = Thread(
                target = UnidomboscoNightmare(
                    self.globalsInstance,
                    instanceIndex,
                    *self.unidomboscoNightmareArgs,
                    headless = self.headless,
                    **self.unidomboscoNightmareKwargs
                ).run,
                args = (
                    str(message), str(studentRegistry), str(name), str(email), str(phoneNumber), str(cpf).replace(c.DOT, c.BLANK), str(url)
                )
            )
            nightmare.start()
            time.sleep(10)

    def runHell(self, message: str, studentRegistry: str, name: str, email: str, phoneNumber: str, cpf: str, url: str = URL, headers: str = HEADERS, instances: int = 10):
        for instanceIndex in range(instances):
            hell = Thread(
                target = UnidomboscoHell(
                    instanceIndex,
                    *self.unidomboscoNightmareArgs,
                    **self.unidomboscoNightmareKwargs
                ).run,
                args = (
                    str(message), str(studentRegistry), str(name), str(email), str(phoneNumber), str(cpf).replace(c.DOT, c.BLANK), str(url), headers
                )
            )
            hell.start()
            time.sleep(0.250)
