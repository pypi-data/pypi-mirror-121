import requests


class UnidomboscoHell:

    def __init__(self, instanceIndex: int):
        self.instanceIndex = instanceIndex

    def run(self, message: str, studentRegistry: str, name: str, email: str, phoneNumber: str, cpf: str, url: str, headers: str) :
        iteration = 0
        log.info(self.run, f'{self.getInstanceIndex()}° instance creating driver')
        self.body = self.selenium.newDriver(headless=self.headless)
        self.urlElement = self.selenium.accessUrl('https://www.unidombosco.edu.br/ouvidoria/')
        log.debug(self.run, 'Dismissing Cokies')
        try:
            self.dismissCokies()
        except Exception as exception:
            log.error(self.run, 'Not possible to dismiss Cokies', exception)
        log.debug(self.run, 'Going to loop')
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
