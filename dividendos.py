import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd

def setup_driver():
    """Configura o driver do Selenium com opções para evitar detecção"""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    
    # Descomente a linha abaixo se quiser rodar em modo headless
    # options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_ticker_data(driver, ticker):
    """Raspa os dados de proventos para um ticker específico"""
    base_url = f"https://statusinvest.com.br/acoes/{ticker.lower()}"
    driver.get(base_url)
    
    # Aguarda o carregamento da página
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.list table"))
        )
    except TimeoutException:
        print(f"Timeout ao carregar a página para {ticker}")
        return []
    
    # Fecha popups se existirem
    close_popups(driver)
    
    all_data = []
    page = 1
    
    while True:
        print(f"Processando página {page} para {ticker}")
        
        try:
            # Extrai os dados da tabela
            table = driver.find_element(By.CSS_SELECTOR, "div.list table")
            rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Pula o cabeçalho
            
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) == 4:
                    data = {
                        'Ticker': ticker,
                        'Tipo': cols[0].text.strip(),
                        'Data COM': cols[1].text.strip(),
                        'Pagamento': cols[2].text.strip(),
                        'Valor': cols[3].text.strip()
                    }
                    all_data.append(data)
            
            # Verifica se há próxima página
            next_button = driver.find_element(By.CSS_SELECTOR, "li[data-next='1']")
            if 'disabled' in next_button.get_attribute('class'):
                break
                
            # Clica na próxima página
            next_button.click()
            time.sleep(3)  # Aguarda o carregamento
            
            # Fecha popups novamente se aparecerem
            close_popups(driver)
            
            page += 1
            
        except NoSuchElementException:
            break
        except Exception as e:
            print(f"Erro ao processar {ticker} página {page}: {str(e)}")
            break
    
    return all_data

def close_popups(driver):
    """Tenta fechar qualquer popup que apareça"""
    try:
        # Fecha popup de cookies se existir
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cookie-button")))
        cookie_button.click()
        time.sleep(1)
    except:
        pass
    
    try:
        # Fecha popup de newsletter se existir
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.wisepops-popup-close")))
        close_button.click()
        time.sleep(1)
    except:
        pass

def main():
    # Lista de tickers para raspar
    tickers = ["ITUB3", "PETR4", "VALE3"]  # Adicione aqui todos os tickers que deseja
    
    driver = setup_driver()
    all_data = []
    
    try:
        for ticker in tickers:
            print(f"Iniciando raspagem para {ticker}")
            ticker_data = scrape_ticker_data(driver, ticker)
            all_data.extend(ticker_data)
            time.sleep(2)  # Pausa entre tickers para evitar bloqueio
    finally:
        driver.quit()
    
    # Cria DataFrame e exporta para CSV
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv("proventos_acoes.csv", index=False, encoding='utf-8-sig')
        print("Dados salvos em proventos_acoes.csv")
    else:
        print("Nenhum dado foi coletado.")

if __name__ == "__main__":
    main()