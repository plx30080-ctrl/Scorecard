#!/bin/bash

# Crescent Scorecard Email Parser - Cron Setup Script
# This script sets up automated email processing

echo "==================================="
echo "Crescent Scorecard Automation Setup"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found"

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARSER_PATH="$SCRIPT_DIR/email_parser.py"
LOG_PATH="$HOME/crescent_scorecard.log"

# Check if email_parser.py exists
if [ ! -f "$PARSER_PATH" ]; then
    echo "❌ email_parser.py not found in $SCRIPT_DIR"
    exit 1
fi

echo "✓ email_parser.py found"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"

# Get email credentials
echo ""
echo "==================================="
echo "Email Configuration"
echo "==================================="
echo ""

read -p "Enter your email address: " EMAIL_ACCOUNT
read -sp "Enter your email password (or app password): " EMAIL_PASSWORD
echo ""
read -p "Enter IMAP server (default: imap.gmail.com): " IMAP_SERVER
IMAP_SERVER=${IMAP_SERVER:-imap.gmail.com}

# Get Firebase URL
echo ""
read -p "Enter your Firebase URL (e.g., https://your-project.firebaseio.com): " FIREBASE_URL

# Create environment file
ENV_FILE="$SCRIPT_DIR/.env"
cat > "$ENV_FILE" << EOF
export EMAIL_ACCOUNT="$EMAIL_ACCOUNT"
export EMAIL_PASSWORD="$EMAIL_PASSWORD"
export IMAP_SERVER="$IMAP_SERVER"
export FIREBASE_URL="$FIREBASE_URL"
EOF

chmod 600 "$ENV_FILE"
echo "✓ Credentials saved to $ENV_FILE"

# Test the parser
echo ""
echo "Testing email parser..."
source "$ENV_FILE"
python3 "$PARSER_PATH" test

if [ $? -ne 0 ]; then
    echo "❌ Parser test failed"
    exit 1
fi

echo "✓ Parser test successful"

# Create wrapper script
WRAPPER_SCRIPT="$SCRIPT_DIR/run_parser.sh"
cat > "$WRAPPER_SCRIPT" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/.env"
python3 "$SCRIPT_DIR/email_parser.py" >> "$HOME/crescent_scorecard.log" 2>&1
EOF

chmod +x "$WRAPPER_SCRIPT"
echo "✓ Wrapper script created"

# Setup cron job
echo ""
echo "==================================="
echo "Cron Job Setup"
echo "==================================="
echo ""
echo "How often should the email parser run?"
echo "1) Every hour"
echo "2) Every 30 minutes"
echo "3) Every 2 hours"
echo "4) Twice a day (8am and 4pm)"
echo "5) Custom"
echo ""
read -p "Select option (1-5): " CRON_OPTION

case $CRON_OPTION in
    1)
        CRON_SCHEDULE="0 * * * *"
        DESCRIPTION="every hour"
        ;;
    2)
        CRON_SCHEDULE="*/30 * * * *"
        DESCRIPTION="every 30 minutes"
        ;;
    3)
        CRON_SCHEDULE="0 */2 * * *"
        DESCRIPTION="every 2 hours"
        ;;
    4)
        CRON_SCHEDULE="0 8,16 * * *"
        DESCRIPTION="at 8am and 4pm"
        ;;
    5)
        read -p "Enter custom cron schedule (e.g., '0 * * * *'): " CRON_SCHEDULE
        DESCRIPTION="custom schedule"
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

# Add cron job
CRON_JOB="$CRON_SCHEDULE $WRAPPER_SCRIPT"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "$WRAPPER_SCRIPT"; then
    echo ""
    echo "⚠️  Cron job already exists for this script"
    read -p "Do you want to replace it? (y/n): " REPLACE
    if [ "$REPLACE" != "y" ]; then
        echo "Setup cancelled"
        exit 0
    fi
    # Remove old entry
    crontab -l 2>/dev/null | grep -v "$WRAPPER_SCRIPT" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo ""
echo "==================================="
echo "✓ Setup Complete!"
echo "==================================="
echo ""
echo "Cron job added: $DESCRIPTION"
echo "Schedule: $CRON_SCHEDULE"
echo ""
echo "Log file: $LOG_PATH"
echo "Environment: $ENV_FILE"
echo ""
echo "To view your cron jobs:"
echo "  crontab -l"
echo ""
echo "To view the log:"
echo "  tail -f $LOG_PATH"
echo ""
echo "To remove the cron job:"
echo "  crontab -e"
echo "  (then delete the line with $WRAPPER_SCRIPT)"
echo ""
echo "To test manually:"
echo "  $WRAPPER_SCRIPT"
echo ""

# Ask if user wants to run it now
read -p "Run the email parser now? (y/n): " RUN_NOW
if [ "$RUN_NOW" = "y" ]; then
    echo ""
    echo "Running email parser..."
    "$WRAPPER_SCRIPT"
    echo ""
    echo "Check the log for results:"
    echo "  cat $LOG_PATH"
fi

echo ""
echo "All done! The parser will now run automatically $DESCRIPTION."
