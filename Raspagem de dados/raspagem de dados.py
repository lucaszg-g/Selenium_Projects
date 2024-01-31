from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from time import sleep
import pandas as pd

# Inicializa o WebDriver
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

# Navega até a página inicial
navegador.get("https://www.kabum.com.br/celular-smartphone")

# Aguarda até que pelo menos uma página esteja disponível
wait = WebDriverWait(navegador, 10)

# Lista para armazenar as informações coletadas
lista_final_celulares = []

# Itera através das páginas
contador = 1
while contador <= 5:  # Modifique este valor conforme necessário
    sleep(1.5)

    try:
        # Coleta informações sobre celulares na página atual
        celulares_nome = navegador.find_elements(By.CLASS_NAME, "sc-d79c9c3f-0")
        celulares_valores = navegador.find_elements(By.CLASS_NAME, "sc-620f2d27-2")

        # Adiciona as informações à lista final
        for nome, valor in zip(celulares_nome, celulares_valores):
            celular_info = {
                'Nome': nome.text,
                'Valor': valor.text,
            }
            lista_final_celulares.append(celular_info)

        # Clique na próxima página
        navegador.find_element(By.CLASS_NAME, 'nextLink').click()
        print(f"Página {contador} coletada")
        contador += 1

    except TimeoutException:
        print(f"Tempo de espera excedido na página {contador}")

print(lista_final_celulares)
print(f"Total de celulares coletados: {len(lista_final_celulares)}")

# Fecha o navegador
navegador.quit()

# Cria um DataFrame a partir da lista
df = pd.DataFrame(lista_final_celulares)

# Salva o DataFrame em um arquivo Excel
nome_arquivo_excel = 'dados_celulares.xlsx'
df.to_excel(nome_arquivo_excel, index=False)

print(f'Dados salvos em {nome_arquivo_excel}')
