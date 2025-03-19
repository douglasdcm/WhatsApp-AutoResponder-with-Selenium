from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
from guara.transaction import Application, AbstractTransaction


class OpenWhatsApp(AbstractTransaction):
    def do(self, **kwargs):
        self._driver.get("https://web.whatsapp.com/")
        print("Please scan the QR code:")
        sleep(20)  # Wait for user to scan QR code
        return self._driver


class SelectGroup(AbstractTransaction):
    def do(self, group_name, **kwargs):
        group = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@title="{group_name}"]'))
        )
        group.click()
        print(f'"{group_name}" group opened.')
        return self._driver


class CheckMessages(AbstractTransaction):
    def do(self, message_to_check, **kwargs):
        messages = self._driver.find_elements(
            By.XPATH, '//span[@class="_ao3e selectable-text copyable-text"]'
        )
        if messages:
            last_message = messages[-1].text
            print(f"Last message: {last_message}")
            return last_message
        return None


class SendReply(AbstractTransaction):
    def do(self, reply_text, **kwargs):
        message_box = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@aria-label="Type a message" and @role="textbox"]')
            )
        )
        message_box.click()
        message_box.send_keys(reply_text)
        sleep(1)  # Small delay to simulate typing

        send_button = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
        )
        send_button.click()
        print(f"Reply sent: {reply_text}")
        return self._driver


def main():
    # Initialize WebDriver
    # service = Service(executable_path="C:/chromedriver/chromedriver.exe")
    # options = Options()
    driver = webdriver.Chrome()

    app = Application(driver)
    group_name = "Lux_Travel"
    message_to_check = "sedan"
    reply_text = "men"

    try:
        # Open WhatsApp and scan QR code
        app.at(OpenWhatsApp)

        # Select the group
        app.at(SelectGroup, group_name=group_name)

        # Continuously check messages and send a reply if the target message is found
        while True:
            last_message = app.at(CheckMessages, message_to_check=message_to_check).result
            if last_message and message_to_check.lower() in last_message.lower():
                app.at(SendReply, reply_text=reply_text)
                break  # Exit the loop after sending the reply
            sleep(2)  # Wait before checking messages again

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
