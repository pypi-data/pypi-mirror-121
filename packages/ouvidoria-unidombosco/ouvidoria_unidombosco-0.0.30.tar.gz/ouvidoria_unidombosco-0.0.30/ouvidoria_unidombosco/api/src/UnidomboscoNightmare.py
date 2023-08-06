import requests, time
from python_helper import Constant as c
from python_helper import log, ObjectHelper


DAY_TOKEN = '__DAY_TOKEN__'


class UnidomboscoNightmare:

    def __init__(self, instanceIndex: int):
        self.instanceIndex = instanceIndex

    def getInstanceIndex(self):
        return self.getIteration(self.instanceIndex) if ObjectHelper.isNotNone(self.instanceIndex) else 1

    def getIteration(self, iteration: int):
        return iteration + 1

    def run(self,
        message: str,
        studentRegistry: str,
        name: str,
        email: str,
        phoneNumber: str,
        cpf: str,
        subject: str,
        place: str,
        area: str,
        department: str,
        reason: str,
        isStudent: str,
        destiny: str,
        url: str,
        headers: str,
        successMessage: str,
        interval: float = 60.0,
        logResponse: bool = False
    ) :
        iteration = 0
        log.info(self.run, f'{self.getInstanceIndex()}° instance running')
        while True :
            log.debug(self.run, f'{self.getInstanceIndex()}° instance running {self.getIteration(iteration)}° iteration')
            parsedMessage = message.replace(DAY_TOKEN, str(self.getIteration(iteration)))
            payload = {
                'txtAssunto': subject,
                'txtSede': place,
                'txtArea': area,
                'txtDepartamento': department,
                'txtMotivo': reason,
                'rdAluno': isStudent,
                'txtCodigoAluno': studentRegistry,
                'txtNome': name,
                'txtEmail': email,
                'txtTelefone': phoneNumber,
                'txtCpf': cpf,
                'txtMensagem': parsedMessage,
                'txtDestino': destiny
            }
            response = requests.post(url, headers=headers, data=payload)
            if ObjectHelper.isNotNone(response):
                log.prettyPython(self.run, f'Response headers', dict(response.headers), logLevel=log.DEBUG)
                log.debug(self.run, f'Response status: {response.status_code}')
                if logResponse:
                    log.prettyPython(self.run, f'Response content', response.content, logLevel=log.DEBUG)
                    log.prettyPython(self.run, f'Response text', response.text, logLevel=log.DEBUG)
                if ObjectHelper.isNotNone(successMessage) and not ObjectHelper.equals(not c.BLANK, successMessage) and successMessage in str(response.text):
                    log.success(self.run, f'{self.getInstanceIndex()}° instance message, at the {self.getIteration(iteration)}° iteration, submited')
                else:
                    exception = Exception(f'The success message "{successMessage}" wasnt found in response text')
                    log.error(self.run, f'{self.getInstanceIndex()}° instance message, at the {self.getIteration(iteration)}° iteration, submited. Unfortnately, not successfuly', exception)
            else:
                exception = Exception(f'Response can not be none')
                log.error(self.run, f'{self.getInstanceIndex()}° instance message, at the {self.getIteration(iteration)}° iteration, submited. Unfortnately, none response was returned', exception)
            time.sleep(interval)
            iteration += 1
