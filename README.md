# WhatsApp Bulk Messenger 📱

Automatically send personalized WhatsApp messages to multiple contacts from an Excel file.

## Features ✨

- 📊 Read contacts from Excel files (.xlsx/.xls)
- 🤖 Automated WhatsApp Web integration
- 💬 Personalized messages with contact names
- ⚡ Smart column detection (automatically finds name/phone columns)
- 🛡️ Built-in delays to avoid spam detection
- 📝 Comprehensive logging
- 🔄 Session persistence (stay logged in)

## Quick Start 🚀

### 1. Setup
```bash
python setup.py
```

This will:
- Install all required dependencies
- Check for Chrome browser
- Setup ChromeDriver
- Create a sample Excel template

### 2. Prepare Your Contacts
Edit `contacts_template.xlsx` or create your own Excel file with:
- **Name column**: Contact names (any variation like "Name", "Contact Name", "Full Name")
- **Phone column**: Phone numbers (any variation like "Phone", "Mobile", "Phone Number")

### 3. Run the Program
```bash
# With default message
python whatsapp_sender.py contacts_template.xlsx

# With custom message
python whatsapp_sender.py contacts_template.xlsx "Hello {name}, how are you today?"
```

### 4. Login to WhatsApp
- Browser will open to WhatsApp Web
- Scan QR code with your phone
- Messages will be sent automatically!

## Requirements 📋

- Python 3.7+
- Google Chrome or Chromium browser
- WhatsApp account
- Internet connection

## Excel File Format 📊

Your Excel file should have two columns:
- **Names**: Contact names
- **Phone Numbers**: Phone numbers (with or without country codes)

Example:
```
Name          | Phone
------------- | -------------
John Doe      | +1234567890
Jane Smith    | 9876543210
Mike Johnson  | +1-555-123-456
```

The program automatically detects common column names like:
- Names: "Name", "Contact Name", "Full Name", "First Name"
- Phones: "Phone", "Mobile", "Phone Number", "Contact", "Number"

## Message Templates 💬

Use `{name}` in your message template to personalize messages:

```bash
# Default message
"hi {name} how are you doin?"

# Custom messages
"Hello {name}, hope you're doing well!"
"Hi {name}, checking in to see how things are going"
"Hey {name}! Long time no talk, how have you been?"
```

## Safety Features 🛡️

- **Automatic delays**: 5-second delay between messages
- **Error handling**: Skips invalid contacts gracefully
- **Session persistence**: Maintains WhatsApp login between runs
- **Validation**: Checks phone number format and length

## Troubleshooting 🔧

### Chrome/ChromeDriver Issues
```bash
# Install Chrome on Ubuntu/Debian
sudo apt update
sudo apt install google-chrome-stable

# Install Chrome on CentOS/RHEL
sudo yum install google-chrome-stable
```

### WhatsApp Login Issues
- Make sure you're logged into WhatsApp on your phone
- Try refreshing the WhatsApp Web page
- Clear browser cache and try again

### Excel File Issues
- Ensure your Excel file has proper headers
- Check that phone numbers are in text format
- Remove any empty rows or invalid entries

## Advanced Usage 🔧

### Custom Column Names
If your Excel has different column names, the program will auto-detect them. Supported patterns:
- **Name columns**: name, contact_name, full_name, first_name
- **Phone columns**: phone, mobile, phone_number, contact, number

### Headless Mode (for servers)
```python
sender = WhatsAppSender(excel_file, headless=True)
```

### Custom Messages with More Variables
Extend the program to use more Excel columns:
```python
message = "Hi {name}, calling you at {phone}. Your email is {email}"
```

## File Structure 📁

```
whatsapp-bulk-messenger/
├── whatsapp_sender.py      # Main program
├── setup.py               # Setup script
├── create_sample_excel.py # Sample Excel generator
├── requirements.txt       # Dependencies
├── contacts_template.xlsx # Sample Excel file
└── README.md             # This file
```

## License 📄

This project is for educational purposes. Please respect WhatsApp's Terms of Service and use responsibly.

## Disclaimer ⚠️

- Use at your own risk
- Respect privacy and consent
- Follow WhatsApp's usage policies
- Don't spam or send unsolicited messages

## Support 💪

If you encounter issues:
1. Check the troubleshooting section
2. Ensure all requirements are met
3. Verify your Excel file format
4. Check the logs for error messages

Happy messaging! 🎉