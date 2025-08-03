import pandas as pd
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WhatsAppSender:
    def __init__(self, excel_file_path, headless=False):
        """
        Initialize WhatsApp sender with Excel file path
        
        Args:
            excel_file_path (str): Path to Excel file containing contacts
            headless (bool): Whether to run browser in headless mode
        """
        self.excel_file_path = excel_file_path
        self.driver = None
        self.wait = None
        self.contacts = []
        self.headless = headless
        
    def setup_driver(self):
        """Set up Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User data directory to maintain WhatsApp login session
        user_data_dir = os.path.join(os.getcwd(), "chrome_user_data")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        
        if self.headless:
            chrome_options.add_argument("--headless")
            
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 20)
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
            
    def load_contacts(self):
        """Load contacts from Excel file"""
        try:
            # Read Excel file - support both .xlsx and .xls formats
            if self.excel_file_path.endswith('.xlsx'):
                df = pd.read_excel(self.excel_file_path, engine='openpyxl')
            else:
                df = pd.read_excel(self.excel_file_path)
                
            logger.info(f"Excel file loaded successfully. Shape: {df.shape}")
            logger.info(f"Columns: {list(df.columns)}")
            
            # Try to identify name and phone columns automatically
            name_column = None
            phone_column = None
            
            # Look for common name column names
            name_patterns = ['name', 'contact_name', 'contact name', 'full_name', 'full name', 'first_name', 'first name']
            for col in df.columns:
                if any(pattern in col.lower() for pattern in name_patterns):
                    name_column = col
                    break
                    
            # Look for common phone column names
            phone_patterns = ['phone', 'phone_number', 'phone number', 'mobile', 'contact', 'number', 'tel', 'telephone']
            for col in df.columns:
                if any(pattern in col.lower() for pattern in phone_patterns):
                    phone_column = col
                    break
                    
            # If not found automatically, use first two columns
            if name_column is None:
                name_column = df.columns[0]
                logger.warning(f"Name column not found automatically. Using first column: {name_column}")
                
            if phone_column is None:
                phone_column = df.columns[1] if len(df.columns) > 1 else df.columns[0]
                logger.warning(f"Phone column not found automatically. Using column: {phone_column}")
            
            logger.info(f"Using name column: {name_column}")
            logger.info(f"Using phone column: {phone_column}")
            
            # Clean and validate data
            self.contacts = []
            for index, row in df.iterrows():
                name = str(row[name_column]).strip()
                phone = str(row[phone_column]).strip()
                
                # Skip rows with missing data
                if pd.isna(row[name_column]) or pd.isna(row[phone_column]) or name == 'nan' or phone == 'nan':
                    logger.warning(f"Skipping row {index + 1}: Missing name or phone data")
                    continue
                    
                # Clean phone number (remove spaces, dashes, parentheses)
                phone = ''.join(filter(str.isdigit, phone))
                
                # Skip if phone number is too short
                if len(phone) < 7:
                    logger.warning(f"Skipping {name}: Phone number too short ({phone})")
                    continue
                    
                self.contacts.append({'name': name, 'phone': phone})
                
            logger.info(f"Loaded {len(self.contacts)} valid contacts")
            
            if len(self.contacts) == 0:
                raise ValueError("No valid contacts found in the Excel file")
                
        except Exception as e:
            logger.error(f"Failed to load contacts from Excel file: {e}")
            raise
            
    def open_whatsapp_web(self):
        """Open WhatsApp Web and wait for user to scan QR code"""
        try:
            logger.info("Opening WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            
            # Check if already logged in
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="chat-list"]')))
                logger.info("Already logged into WhatsApp Web")
                return
            except TimeoutException:
                pass
                
            # Wait for QR code scan
            logger.info("Please scan the QR code to login to WhatsApp Web...")
            logger.info("Waiting for login...")
            
            # Wait for the chat list to appear (indicates successful login)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="chat-list"]')))
            logger.info("Successfully logged into WhatsApp Web!")
            
        except TimeoutException:
            logger.error("Timeout waiting for WhatsApp Web login")
            raise
        except Exception as e:
            logger.error(f"Failed to open WhatsApp Web: {e}")
            raise
            
    def send_message_to_contact(self, name, phone, message):
        """Send message to a specific contact"""
        try:
            # Create the URL to open chat with specific phone number
            url = f"https://web.whatsapp.com/send?phone={phone}"
            logger.info(f"Opening chat with {name} ({phone})")
            
            self.driver.get(url)
            time.sleep(3)
            
            # Wait for chat to load
            try:
                # Wait for message input box
                message_box = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="message-composer"] [data-testid="message-composer-input"]'))
                )
                
                # Type the message
                message_box.clear()
                message_box.send_keys(message)
                time.sleep(1)
                
                # Find and click send button
                send_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="send"]')
                send_button.click()
                
                logger.info(f"Message sent successfully to {name}")
                return True
                
            except TimeoutException:
                logger.error(f"Failed to load chat for {name} ({phone}) - Contact may not be on WhatsApp")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send message to {name} ({phone}): {e}")
            return False
            
    def send_messages_to_all_contacts(self, message_template="hi {name} how are you doin?"):
        """Send personalized messages to all contacts"""
        if not self.contacts:
            logger.error("No contacts loaded")
            return
            
        logger.info(f"Starting to send messages to {len(self.contacts)} contacts...")
        
        success_count = 0
        failed_count = 0
        
        for i, contact in enumerate(self.contacts, 1):
            name = contact['name']
            phone = contact['phone']
            
            # Personalize the message
            personalized_message = message_template.format(name=name)
            
            logger.info(f"[{i}/{len(self.contacts)}] Sending message to {name}")
            
            if self.send_message_to_contact(name, phone, personalized_message):
                success_count += 1
            else:
                failed_count += 1
                
            # Add delay between messages to avoid being flagged as spam
            time.sleep(5)
            
        logger.info(f"Message sending completed. Success: {success_count}, Failed: {failed_count}")
        
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")

def main():
    """Main function to run the WhatsApp sender"""
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python whatsapp_sender.py <excel_file_path> [custom_message]")
        print("Example: python whatsapp_sender.py contacts.xlsx")
        print("Example: python whatsapp_sender.py contacts.xlsx 'Hello {name}, hope you are doing well!'")
        return
        
    excel_file = sys.argv[1]
    custom_message = sys.argv[2] if len(sys.argv) > 2 else "hi {name} how are you doin?"
    
    # Check if Excel file exists
    if not os.path.exists(excel_file):
        logger.error(f"Excel file not found: {excel_file}")
        return
        
    sender = None
    try:
        # Initialize sender
        sender = WhatsAppSender(excel_file)
        
        # Load contacts
        sender.load_contacts()
        
        # Setup browser
        sender.setup_driver()
        
        # Open WhatsApp Web
        sender.open_whatsapp_web()
        
        # Send messages
        sender.send_messages_to_all_contacts(custom_message)
        
        logger.info("All done! You can close the browser now.")
        input("Press Enter to close the browser...")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        if sender:
            sender.close()

if __name__ == "__main__":
    main()