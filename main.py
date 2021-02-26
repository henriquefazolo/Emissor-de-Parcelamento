# coding: utf-8
# version : 0.1
# author : Henrique UM Fazolo
# e-mail : henriquefazolo@gmail.com

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

class Robo_Emissor:
    def __init__(self, site_login, ie_driver, data_base):
        self.__site_login = site_login
        self.__ie_driver = ie_driver
        self.__data_base = data_base

    def navegador(self, ie_driver):
        self.navegador = webdriver.Ie(ie_driver)
        self.navegador.implicitly_wait(20)
        self.espera = WebDriverWait(self.navegador, 10)      
        return self.navegador

    def localizar_elemento(self, xpath, ByTipe=By.XPATH):
        self.elemento = self.espera.until(EC.presence_of_element_located((ByTipe, xpath)))
        return self.elemento

    def realizar_login(self):
        self.navegador.get(self.__site_login)      

        sleep(2)
        botao_entrar = self.localizar_elemento('//*[@id="login-dados-certificado"]/p[2]/a/img')  
        botao_entrar.click()

        sleep(2)
        botao_certificado_digital = self.localizar_elemento('//*[@id="cert-digital"]')
        botao_certificado_digital.click()
        sleep(5)
       
    def alterar_perfil_acesso(self, cnpj):
        sleep(2)

        botao_alterar_acesso = self.localizar_elemento('//*[@id="btnPerfil"]')
        botao_alterar_acesso.click()

        campo_procurador_cnpj = self.localizar_elemento('//*[@id="txtNIPapel2"]')
        campo_procurador_cnpj.click()
        campo_procurador_cnpj.send_keys(cnpj)

        botao_alterar = self.localizar_elemento('//*[@id="formPJ"]/input[4]').click()
        sleep(2)

    def emitir_guia_simples_nacional(self):
        tempo = 3
        sleep(tempo)

        self.navegador.get('https://sinac.cav.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/snparc.app/Default.aspx')
        sleep(tempo)

        botao_emissao_parcela = self.localizar_elemento('//*[@id="ctl00_contentPlaceH_linkButtonEmitirDAS"]')
        botao_emissao_parcela.click()
        sleep(tempo)

        self.localizar_elemento('//*[@id="ctl00_contentPlaceH_btnContinuar"]').click()
        sleep(tempo)

        self.localizar_elemento('//*[@id="ctl00_contentPlaceH_gdvParcela_ctl02_LinkButtonEmitirDas"]').click()
        sleep(tempo)


    def lista_execução(self, lista_empresas):
        for empresa in lista_empresas:
            cnpj_empresa = empresa[0]
            tipos_parcelamento = empresa[[1][0]]
            self.alterar_perfil_acesso(cnpj_empresa)    

            for tipo_parcelamento in tipos_parcelamento:                
                if tipo_parcelamento == 1:
                    print(tipo_parcelamento)
                    self.emitir_guia_simples_nacional()

    def executar(self):
        self.navegador(self.__ie_driver)
        self.realizar_login()
        self.lista_execução(self.__data_base)
        self.navegador.quit()

site_ecac = 'https://cav.receita.fazenda.gov.br/autenticacao/login'
ie_driver = 'C:\\IEDriverServer\\IEDriverServer.exe'

# tipos de parcelamento
# 1 - simples nacional

data_base_cnpj = [
    ['13827404000103', [1]]
    ]

robo_emissor = Robo_Emissor(site_ecac, ie_driver, data_base_cnpj)
robo_emissor.executar()