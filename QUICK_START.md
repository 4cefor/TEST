# 🚀 Quick Start Guide

## Installation & Setup (One-time)

```bash
# 1. Install dependencies and setup
python3 setup.py

# 2. Make run script executable (if not already)
chmod +x run.sh
```

## Usage

### Option 1: Use the helper script (Recommended)
```bash
# Run with default message
./run.sh contacts_template.xlsx

# Run with custom message
./run.sh contacts_template.xlsx "Hello {name}, hope you're well!"
```

### Option 2: Direct Python execution
```bash
# Activate virtual environment first
source venv/bin/activate

# Run the program
python whatsapp_sender.py contacts_template.xlsx
python whatsapp_sender.py contacts_template.xlsx "Custom message for {name}"
```

## Steps When Running

1. **Prepare your Excel file** with columns:
   - Name column (Name, Contact Name, etc.)
   - Phone column (Phone, Mobile, Phone Number, etc.)

2. **Run the program** using one of the methods above

3. **Browser will open** to WhatsApp Web

4. **Scan QR code** with your phone to login

5. **Messages send automatically** with 5-second delays

## Excel File Format

| Name         | Phone        |
|-------------|--------------|
| John Doe    | +1234567890  |
| Jane Smith  | 9876543210   |
| Mike Johnson| +1-555-123-456|

## Important Notes

- ⚠️ **Use responsibly** - Don't spam people
- 📱 **WhatsApp must be active** on your phone
- 🔄 **Browser stays logged in** for future runs
- ⏱️ **5-second delay** between messages (anti-spam)
- 📝 **Check logs** for detailed information

## Troubleshooting

- **Chrome not found**: Install Google Chrome browser
- **Login issues**: Clear browser data and retry
- **Excel errors**: Check file format and column names
- **Virtual env errors**: Run `python3 setup.py` again

---

**Ready to go!** 🎉