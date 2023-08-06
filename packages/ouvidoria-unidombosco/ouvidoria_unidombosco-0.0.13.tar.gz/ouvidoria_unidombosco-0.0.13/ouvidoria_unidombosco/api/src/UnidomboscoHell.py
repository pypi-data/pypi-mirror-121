import requests
from python_helper import log, ObjectHelper


class UnidomboscoHell:

    def __init__(self, instanceIndex: int):
        self.instanceIndex = instanceIndex

    def getInstanceIndex(self):
        return self.getIteration(self.instanceIndex) if ObjectHelper.isNotNone(self.instanceIndex) else 1

    def getIteration(self, iteration: int):
        return iteration + 1
        
    def run(self, message: str, studentRegistry: str, name: str, email: str, phoneNumber: str, cpf: str, url: str, headers: str) :
        iteration = 0
        log.info(self.run, f'{self.getInstanceIndex()}° instance creating driver')
        while True :
            log.debug(self.run, f'{self.getInstanceIndex()}° instance running {self.getIteration(iteration)}° iteration')
            parsedMessage = message.replace(DAY_TOKEN, str(self.getIteration(iteration)))
            payload = {
                'txtAssunto': '3',
                'txtSede': '13',
                'txtArea': 'Administrativo',
                'txtDepartamento': 'Direção',
                'txtMotivo': '62',
                'rdAluno': '1',
                'txtCodigoAluno': studentRegistry,
                'txtNome': name,
                'txtEmail': email,
                'txtTelefone': phoneNumber,
                'txtCpf': cpf,
                'txtMensagem': parsedMessage
            }
            response = requests.post(url, headers=headers, data=payload)
            log.success(self.run, f'{self.getInstanceIndex()}° instance message, at the {self.getIteration(iteration)}° iteration, submited with status: {response.status_code}')
            iteration += 1
