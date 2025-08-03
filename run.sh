#!/bin/bash

# WhatsApp Bulk Messenger - Quick Start Script
echo "🚀 Starting WhatsApp Bulk Messenger..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.py first:"
    echo "   python3 setup.py"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if contacts file is provided
if [ $# -eq 0 ]; then
    echo "📋 Usage: ./run.sh <excel_file> [custom_message]"
    echo ""
    echo "Examples:"
    echo "  ./run.sh contacts_template.xlsx"
    echo "  ./run.sh my_contacts.xlsx"
    echo '  ./run.sh contacts.xlsx "Hello {name}, how are you today?"'
    echo ""
    echo "Available files:"
    ls -la *.xlsx 2>/dev/null || echo "  No Excel files found in current directory"
    exit 1
fi

# Run the WhatsApp sender
echo "📱 Starting WhatsApp automation..."
python whatsapp_sender.py "$@"

echo "✅ Done!"