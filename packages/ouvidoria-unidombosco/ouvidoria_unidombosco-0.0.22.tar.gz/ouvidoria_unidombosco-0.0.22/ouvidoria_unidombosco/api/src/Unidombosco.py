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
  'Content-Type': 'application/x-www-form-urlencoded',
  'referer': 'Sorry, this is the only way for me to be heard'
}

DEFAULT_SUBJECT: str =  '3'
DEFAULT_PLACE: str =  '13'
DEFAULT_AREA: str =  'Administrativo'
DEFAULT_DEPARTMENT: str =  'Direção'
DEFAULT_REASON: str =  '62'
DEFAULT_IS_STUDENT: str = '1'
DEFAULT_DESTINY: str = '8'


def toString(thing):
    return None if ObjectHelper.isNone(thing) else str(thing)


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

    def runNightmare(self,
        message: str,
        studentRegistry: str,
        name: str,
        email: str,
        phoneNumber: str,
        cpf: str,
        subject: str =  DEFAULT_SUBJECT,
        place: str =  DEFAULT_PLACE,
        area: str =  DEFAULT_AREA,
        department: str =  DEFAULT_DEPARTMENT,
        reason: str =  DEFAULT_REASON,
        isStudent: str = DEFAULT_IS_STUDENT,
        destiny: str = DEFAULT_DESTINY,
        url: str = URL,
        instances: int = 1
    ):
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
                    str(message),
                    str(studentRegistry),
                    str(name),
                    str(email),
                    str(phoneNumber),
                    c.BLANK if ObjectHelper.isNone(cpf) else str(cpf).replace(c.DOT, c.BLANK),
                    str(subject,
                    str(area),
                    str(department),
                    str(reason),
                    str(url)
                )
            )
            nightmare.start()
            time.sleep(10)

    def runHell(self,
        message: str,
        studentRegistry: str,
        name: str,
        email: str,
        phoneNumber: str,
        cpf: str,
        subject: str =  DEFAULT_SUBJECT,
        place: str =  DEFAULT_PLACE,
        area: str =  DEFAULT_AREA,
        department: str =  DEFAULT_DEPARTMENT,
        reason: str =  DEFAULT_REASON,
        isStudent: str = DEFAULT_IS_STUDENT,
        destiny: str = DEFAULT_DESTINY,
        url: str = URL,
        headers: str = HEADERS,
        instances: int = 1,
        interval: float = 60,
        threadsInterval: float = 0.250
    ):
        for instanceIndex in range(instances):
            hell = Thread(
                target = UnidomboscoHell(
                    instanceIndex,
                    *self.unidomboscoNightmareArgs,
                    **self.unidomboscoNightmareKwargs
                ).run,
                args = (
                    toString(message),
                    toString(studentRegistry),
                    toString(name),
                    toString(email),
                    toString(phoneNumber),
                    toString(cpf),
                    toString(subject),
                    toString(place),
                    toString(area),
                    toString(department),
                    toString(reason),
                    toString(isStudent),
                    toString(destiny),
                    toString(url),
                    headers
                ),
                kwargs = {
                    'interval': interval
                }
            )
            hell.start()
            time.sleep(threadsInterval)
