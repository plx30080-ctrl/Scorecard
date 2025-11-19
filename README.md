# 📊 Crescent Scorecard 2025 - Web Application

A modern, mobile-friendly web application to replace manual Excel-based shift tracking with automated data entry and real-time collaboration.

## ✨ Features

### Current Features
- ✅ **Easy Data Entry** - Simplified forms for quick shift data input
- ✅ **Auto Calculations** - Fill rates, variances, and totals calculated automatically
- ✅ **Real-time Updates** - Firebase backend for multi-user collaboration
- ✅ **Mobile Responsive** - Works perfectly on phones and tablets
- ✅ **Visual Scorecard** - Color-coded metrics and easy-to-read dashboards
- ✅ **Weekly/Daily Views** - Switch between summary and detailed views
- ✅ **Historical Data** - Browse any week's performance

### Automated Features (Optional Setup)
- 📧 **Email Integration** - Automatically parse and import shift report emails
- 🔄 **Real-time Sync** - Updates visible to all team members instantly
- 📊 **Trend Analysis** - Track performance over time

## 🚀 Quick Start

### 1. Set Up Firebase
```bash
1. Go to https://console.firebase.google.com/
2. Create new project
3. Add web app
4. Enable Realtime Database
5. Copy config to crescent-scorecard.html
```

### 2. Deploy Application

**Easiest: Firebase Hosting**
```bash
npm install -g firebase-tools
firebase login
firebase init hosting
# Select your project
# Set public directory: ./
firebase deploy
```

**Alternative: Netlify**
- Drag and drop `crescent-scorecard.html` to Netlify
- Done! Get your URL

### 3. Start Using
- Open the deployed URL
- Select current week
- Click "Data Entry"
- Fill in shift information
- Data auto-saves to Firebase

## 📁 Project Structure

```
crescent-scorecard/
├── crescent-scorecard.html    # Main web application
├── email_parser.py             # Python email automation script
├── requirements.txt            # Python dependencies
├── SETUP_GUIDE.md             # Detailed setup instructions
└── README.md                  # This file
```

## 📧 Email Automation Setup

### Option 1: Zapier (No Code Required)
1. Create Zapier account
2. New Zap: Gmail → Firebase
3. Parse email content
4. Send to Firebase API
5. Turn on Zap

**Time to setup:** ~10 minutes

### Option 2: Python Script (More Control)
```bash
# Install dependencies
pip install -r requirements.txt

# Set credentials
export EMAIL_ACCOUNT="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"

# Edit email_parser.py and set FIREBASE_URL

# Test the parser
python email_parser.py test

# Run manually
python email_parser.py

# Or set up cron job (runs every hour)
crontab -e
# Add: 0 * * * * /usr/bin/python3 /path/to/email_parser.py >> /var/log/scorecard.log 2>&1
```

### Option 3: Google Apps Script (For Gmail)
See `SETUP_GUIDE.md` for complete script

**Time to setup:** ~30 minutes

## 📊 Data Structure

### Firebase Structure
```
scorecard/
├── 2025-11-24/  (week ending date)
│   ├── 2025-11-18/  (date)
│   │   ├── 1st/  (shift)
│   │   │   ├── forecasted: 105
│   │   │   ├── requested: 99
│   │   │   ├── required: 107
│   │   │   ├── working: 80
│   │   │   ├── newStarts: 3
│   │   │   ├── sentHome: 0
│   │   │   ├── directHours: 769.75
│   │   │   ├── surveysCompleted: 0
│   │   │   ├── earlyLeaves: 6
│   │   │   └── dnrs: 1
│   │   └── 2nd/
│   │       └── ...
│   └── ...
```

### Metrics Tracked
- **Staffing:** Forecasted, Requested, Required, Working
- **Activity:** New Starts, Sent Home, Direct Hours
- **Quality:** Surveys Completed, Early Leaves, DNRs
- **Calculated:** Variance, Fill Rate %, SLA Fill %

## 🎨 Customization

### Change Fill Rate Thresholds
Edit in `crescent-scorecard.html`:
```javascript
// Line ~450
color={fillRate >= 95 ? 'green' : fillRate >= 85 ? 'yellow' : 'red'}
```

### Add New Fields
1. Update `getEmptyShiftData()` function
2. Add input field in DataEntryView
3. Add column in ScorecardView table

### Modify Email Parser
Edit regex patterns in `email_parser.py`:
```python
def parse_number(text: str, field_name: str) -> int:
    pattern = rf'{field_name}:\s*(\d+)'
    # Customize pattern as needed
```

## 🔐 Security

### Production Firebase Rules
```json
{
  "rules": {
    "scorecard": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```

### Add Authentication
See `SETUP_GUIDE.md` for complete authentication setup

## 📱 Mobile Usage

### Add to Home Screen (iOS)
1. Open in Safari
2. Tap Share button
3. "Add to Home Screen"
4. App icon appears on home screen

### Add to Home Screen (Android)
1. Open in Chrome
2. Tap menu (3 dots)
3. "Add to Home screen"
4. App shortcut created

## 🛠️ Troubleshooting

### Data Not Saving
- Check Firebase config is correct
- Verify database rules allow write access
- Open browser console (F12) for error messages

### Email Parser Not Working
- Verify email credentials (use App Password for Gmail)
- Check FIREBASE_URL is set correctly
- Test with `python email_parser.py test`
- Check email subject matches filter

### Fill Rate Calculations Wrong
- Ensure all numbers are entered correctly
- Formula: (Working / Required) × 100
- Check for division by zero

## 📈 Roadmap

### Phase 2 (Future)
- [ ] Charts and trend analysis
- [ ] Export to Excel/PDF
- [ ] Weekly email reports
- [ ] Manager dashboard
- [ ] Multi-location support
- [ ] Integration with ProLogistix API
- [ ] Predictive staffing recommendations
- [ ] Mobile push notifications

### Phase 3 (Advanced)
- [ ] Machine learning for forecasting
- [ ] Automated shift scheduling
- [ ] Employee performance tracking
- [ ] Custom reporting builder

## 💡 Usage Tips

### For Shift Leads
1. **End of Shift:** Open app, select today, enter data
2. **Quick Entry:** Most fields default to 0 - only fill what's needed
3. **Auto-Save:** Data saves automatically when you submit
4. **Review:** Check variance and fill rate before submitting

### For Managers
1. **Weekly Review:** Check scorecard view every Friday
2. **Trend Spotting:** Look for patterns in fill rates
3. **Early Intervention:** Address low fill rates proactively
4. **Data Export:** (Future) Generate reports for leadership

### For Admins
1. **Monitor Email Parser:** Check logs for errors
2. **Data Validation:** Spot-check entries weekly
3. **Backup:** Firebase auto-backs up, but export monthly
4. **Updates:** Keep Firebase SDK up to date

## 🤝 Contributing

Have ideas? Want to add features? Here's how:

1. **Report Issues:** Note any bugs or problems
2. **Request Features:** Suggest improvements
3. **Submit Changes:** Modify and test locally
4. **Share Updates:** Help teammates learn new features

## 📞 Support

### Common Questions

**Q: Can multiple people enter data at once?**
A: Yes! Firebase syncs in real-time across all users.

**Q: What happens if someone enters wrong data?**
A: Just re-enter the correct data for that shift - it will overwrite.

**Q: Can we access historical data?**
A: Yes, select any previous week using the date picker.

**Q: Will this work offline?**
A: Not currently, but can add offline support if needed.

**Q: How much does Firebase cost?**
A: Free tier includes 1GB storage and 10GB bandwidth - plenty for this use case.

## 📄 License

Internal use for Crescent operations.

## 🎯 Success Metrics

Track your improvement:
- ⬆️ **Fill Rate:** Target 95%+ overall
- ⬇️ **Data Entry Time:** From 15 min → 2 min per shift
- ✅ **Accuracy:** Eliminate manual calculation errors
- 📊 **Visibility:** Real-time insights for faster decisions
- 🚀 **Efficiency:** Automated email parsing saves hours weekly

---

Built with ❤️ for efficient workforce management
