from python_helper import log, ObjectHelper
from ouvidoria_unidombosco.api.src.SeleniumHelper import SeleniumHelper


DAY_TOKEN = '__DAY_TOKEN__'


class UnidomboscoNightmare:

    def __init__(self, globalsInstance, instanceIndex: int):
        self.selenium = SeleniumHelper(globalsInstance)
        self.instanceIndex = instanceIndex

    def accessField(self, formSelector, choice, processingTime=0, muteLogs=True):
        if processingTime > 0 :
            self.selenium.wait(processingTime=processingTime)
        form = self.selenium.accessSelector(f'//form//div//div//select[@id="txt{formSelector}"]', movingTo=True, muteLogs=True)
        self.selenium.wait(fraction=True)
        self.selenium.accessSelector(f'//option[@value="{choice}"]', muteLogs=True)

    def isThereAny(self, formSelector, choice, processingTime=0, muteLogs=True):
        if processingTime > 0 :
            self.selenium.wait(processingTime=processingTime)
        form = self.selenium.findBySelector(f'//form//div//div//select[@id="txt{formSelector}"]', movingTo=True, muteLogs=True)
        self.selenium.wait(fraction=True)
        choiceElement = self.selenium.findBySelector(f'//option[@value="{choice}"]', muteLogs=True)
        return ObjectHelper.isNotNone(choiceElement)

    def typeForm(self, formSelector, text):
        form = self.selenium.findBySelector(f'//form//div//div//input[@id="txt{formSelector}"]')
        self.selenium.typeIn(text, form)

    def typeMessage(self, formSelector, text):
        form = self.selenium.findBySelector(f'//form//div//textarea[@id="txt{formSelector}"]', movingTo=True)
        self.selenium.typeIn(text, form)

    def dismissCokies(self):
        self.selenium.accessSelector(f'//div//div//a[@aria-label="deny cookies"]')

    def submit(self) :
        self.selenium.accessSelector(f'//form//button[@id="form-submit"]', movingTo=True)

    def getInstanceIndex(self):
        return self.getIteration(self.instanceIndex) if ObjectHelper.isNotNone(self.instanceIndex) else 1

    def getIteration(self, iteration: int):
        return iteration + 1

    def run(self, message: str, studentRegistry: str, name: str, email: str, phoneNumber: str, cpf: str) :
        iteration = 0
        log.info(self.run, 'Creating driver')
        self.body = self.selenium.newDriver()
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
            log.debug(self.run, 'Waiting for fields to appear')
            while True :
                log.debug(self.run, 'Accessing "Assunto"')
                self.accessField('Assunto', '3', muteLogs=True)
                log.debug(self.run, 'Accessing "Area"')
                self.accessField('Area', 'Administrativo', muteLogs=True)
                log.debug(self.run, 'Checking "Departamento"')
                if self.isThereAny('Departamento', 'Financeiro', processingTime=1, muteLogs=True) :
                    break
            ###- financeiro
            # log.debug(self.run, 'Accessing "Departamento"')
            # self.accessField('Departamento', 'Financeiro')
            # log.debug(self.run, 'Accessing "Motivo"')
            # self.accessField('Motivo', '39', processingTime=5)

            ###- direção
            log.debug(self.run, 'Accessing "Departamento"')
            self.accessField('Departamento', 'Direção')
            log.debug(self.run, 'Accessing "Motivo"')
            self.accessField('Motivo', '62', processingTime=5)

            log.debug(self.run, 'Typing user info')
            self.typeForm('CodigoAluno', studentRegistry)
            self.typeForm('Nome', name)
            self.typeForm('Email', email)
            self.typeForm('Telefone', phoneNumber)
            self.typeForm('Cpf', cpf)
            log.debug(self.run, 'Typing message')
            self.typeMessage('Mensagem', parsedMessage)
            log.debug(self.run, 'Submitting')
            self.submit()
            self.selenium.wait(2)
            # self.selenium.closeDriver()
            log.success(self.run, f'{self.getInstanceIndex()}° instance message, at the {self.getIteration(iteration)}° iteration, submited')
            iteration += 1
            self.urlElement = self.selenium.accessUrl('https://www.unidombosco.edu.br/ouvidoria/')
