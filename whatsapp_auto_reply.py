from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep


service = Service(executable_path="C:/chromedriver/chromedriver.exe")
options = Options()


driver = webdriver.Chrome(service=service, options=options)


driver.get("https://web.whatsapp.com/")


print("Please scan Qr code:")
sleep(20)  


group_name = "Lux_Travel"  
message_to_check = "sedan"  

try:
    sleep(2)  

    
    group = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//span[@title="{group_name}"]'))
    )
    group.click()
    print(f'"{group_name}" grubuna girildi.')

    
    while True:
        try:
            sleep(2)  

            
            if len(driver.window_handles) == 0:
                print("Tarayıcı kapanmış! 5 saniye bekleyip tekrar deniyorum...")
                sleep(5)
                continue

            
            messages = driver.find_elements(By.XPATH, '//span[@class="_ao3e selectable-text copyable-text"]')

            if messages:
                last_message = messages[-1].text
                print(f"Son mesaj: {last_message}")

                
                if message_to_check.lower() in last_message.lower():
                    
                    message_box = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Type a message" and @role="textbox"]'))
                    )

                    
                    message_box.click()
                    message_box.send_keys("men")
                    sleep(1)  

                    
                    send_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
                    )
                    send_button.click()
                    print(f"'{message_to_check}' mesajı tespit edildi, yanıt gönderildi.")

            sleep(1)  

        except Exception as e:
            print(f"Döngü içinde hata oluştu: {e}")
            sleep(2)  
except Exception as e:
    print("Hata oluştu:", e)

finally:
    driver.quit()  
