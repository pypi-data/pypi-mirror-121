import requests, time
from python_helper import log, ObjectHelper


DAY_TOKEN = '__DAY_TOKEN__'


class UnidomboscoHell:

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
        interval: float = 0.0
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
                'txtCpf': cpf if ObjectHelper.isNone(cpf) else cpf.replace(c.DOT, c.BLANK),
                'txtMensagem': parsedMessage,
                'txtDestino': destiny
            }
            response = requests.post(url, headers=headers, data=payload)
            log.success(self.run, f'{self.getInstanceIndex()}° instance message, at the {self.getIteration(iteration)}° iteration, submited with status: {response.status_code}')
            time.sleep(interval)
            iteration += 1
