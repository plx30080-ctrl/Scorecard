# Crescent Scorecard Setup & Email Automation Guide

## 🚀 Quick Start

### Step 1: Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project (or use existing)
3. Add a web app to your project
4. Copy the Firebase configuration object
5. In `crescent-scorecard.html`, replace the firebaseConfig object with your values:

```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT.firebaseapp.com",
    databaseURL: "https://YOUR_PROJECT.firebaseio.com",
    projectId: "YOUR_PROJECT",
    storageBucket: "YOUR_PROJECT.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

6. Enable Realtime Database in Firebase Console
7. Set database rules to allow read/write (for testing):

```json
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```

**Security Note:** For production, implement proper authentication and rules!

### Step 2: Deploy the Application

**Option A: Firebase Hosting (Recommended)**
```bash
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy
```

**Option B: Netlify/Vercel**
- Drag and drop the HTML file
- Or connect via GitHub

**Option C: GitHub Pages**
- Push to a GitHub repository
- Enable GitHub Pages in settings

---

## 📧 Email Automation Setup

### Understanding Email Format

Your team currently receives shift data via email. Here's how to automate it:

### Method 1: Zapier Integration (Easiest)

1. **Create Zapier Account** at zapier.com

2. **Set up Gmail/Outlook Trigger**
   - Trigger: "New Email" 
   - Filter by subject line (e.g., "Shift Report" or specific sender)

3. **Add Email Parser**
   - Use Zapier's Email Parser or built-in text extraction
   - Example email format to parse:
   ```
   Date: 11/19/2025
   Shift: 1st
   Forecasted: 105
   Requested: 99
   Required: 107
   Working: 80
   New Starts: 3
   Direct Hours: 769.75
   ```

4. **Add Firebase Action**
   - Action: "Webhooks by Zapier" → POST request
   - URL: Your Firebase Realtime Database REST API
   - Format: `https://YOUR_PROJECT.firebaseio.com/scorecard/WEEK_ENDING/DATE/SHIFT.json`
   - Body: JSON with parsed data

### Method 2: Google Apps Script (For Gmail)

If emails come to Gmail, use this script:

```javascript
function processShiftEmails() {
  // Search for unread emails with specific label or subject
  const threads = GmailApp.search('label:shift-reports is:unread');
  
  threads.forEach(thread => {
    const messages = thread.getMessages();
    messages.forEach(message => {
      const body = message.getPlainBody();
      const data = parseShiftData(body);
      
      if (data) {
        sendToFirebase(data);
        message.markRead();
      }
    });
  });
}

function parseShiftData(emailBody) {
  // Customize based on your email format
  const dateMatch = emailBody.match(/Date:\s*(\d{1,2}\/\d{1,2}\/\d{4})/);
  const shiftMatch = emailBody.match(/Shift:\s*(1st|2nd)/);
  const forecastedMatch = emailBody.match(/Forecasted:\s*(\d+)/);
  const requestedMatch = emailBody.match(/Requested:\s*(\d+)/);
  const requiredMatch = emailBody.match(/Required:\s*(\d+)/);
  const workingMatch = emailBody.match(/Working:\s*(\d+)/);
  const newStartsMatch = emailBody.match(/New Starts:\s*(\d+)/);
  const directHoursMatch = emailBody.match(/Direct Hours:\s*([\d.]+)/);
  
  if (!dateMatch || !shiftMatch) return null;
  
  return {
    date: formatDate(dateMatch[1]),
    shift: shiftMatch[1],
    forecasted: parseInt(forecastedMatch?.[1] || 0),
    requested: parseInt(requestedMatch?.[1] || 0),
    required: parseInt(requiredMatch?.[1] || 0),
    working: parseInt(workingMatch?.[1] || 0),
    newStarts: parseInt(newStartsMatch?.[1] || 0),
    directHours: parseFloat(directHoursMatch?.[1] || 0),
    // Add other fields as needed
  };
}

function sendToFirebase(data) {
  const weekEnding = getWeekEnding(data.date);
  const url = `https://YOUR_PROJECT.firebaseio.com/scorecard/${weekEnding}/${data.date}/${data.shift}.json`;
  
  const options = {
    method: 'put',
    contentType: 'application/json',
    payload: JSON.stringify(data)
  };
  
  UrlFetchApp.fetch(url, options);
}

function formatDate(dateStr) {
  // Convert MM/DD/YYYY to YYYY-MM-DD
  const parts = dateStr.split('/');
  return `${parts[2]}-${parts[0].padStart(2, '0')}-${parts[1].padStart(2, '0')}`;
}

function getWeekEnding(dateStr) {
  const date = new Date(dateStr);
  const day = date.getDay();
  const diff = day === 0 ? 0 : 7 - day;
  date.setDate(date.getDate() + diff);
  return date.toISOString().split('T')[0];
}

// Set up a time-based trigger to run every hour
function createTrigger() {
  ScriptApp.newTrigger('processShiftEmails')
    .timeBased()
    .everyHours(1)
    .create();
}
```

**Setup Instructions:**
1. Open Gmail → Settings → Filters → Create filter for shift emails
2. Apply label "shift-reports"
3. Go to script.google.com
4. Paste the code above
5. Update YOUR_PROJECT with your Firebase project
6. Run `createTrigger()` once to set up automation
7. Authorize the script

### Method 3: Make.com (Integromat)

Similar to Zapier but with more visual flow:
1. Create scenario
2. Gmail/Email trigger
3. Text parser module
4. HTTP module → Firebase REST API
5. Activate scenario

---

## 📊 Expected Email Format

Work with your team to standardize email format. Suggested template:

```
Subject: Shift Report - [Date] - [Shift]

Date: 11/19/2025
Shift: 1st

STAFFING:
Forecasted: 105
Requested: 99
Required: 107
Working: 80

ACTIVITY:
New Starts: 3
Sent Home: 0
Direct Hours: 769.75

QUALITY:
Surveys Completed: 0
Early Leaves: 6
DNRs: 1
```

---

## 🔧 Customization Options

### Adding More Fields

Edit the `getEmptyShiftData()` function:
```javascript
const getEmptyShiftData = () => ({
    forecasted: 0,
    requested: 0,
    required: 0,
    working: 0,
    newStarts: 0,
    sentHome: 0,
    directHours: 0,
    surveysCompleted: 0,
    earlyLeaves: 0,
    dnrs: 0,
    // Add new fields here
    yourNewField: 0
});
```

Then add input fields in the DataEntryView component.

### Changing Color Thresholds

Find the `SummaryCard` component and adjust:
```javascript
color={overallFillRate >= 95 ? 'green' : overallFillRate >= 85 ? 'yellow' : 'red'}
```

### Mobile Optimization

The app is already responsive, but you can adjust breakpoints in the Tailwind classes (md:, lg:, etc.)

---

## 🔐 Security Best Practices

### Firebase Rules (Production)

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

```javascript
// Add to your HTML file
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-auth-compat.js"></script>

// In your JavaScript
const auth = firebase.auth();

// Simple email/password login
function login(email, password) {
    auth.signInWithEmailAndPassword(email, password)
        .then((userCredential) => {
            console.log('Logged in:', userCredential.user);
        })
        .catch((error) => {
            console.error('Login error:', error);
        });
}
```

---

## 📱 Mobile App (Future Enhancement)

Consider converting to a Progressive Web App (PWA):
1. Add manifest.json
2. Add service worker for offline support
3. Enable "Add to Home Screen"

---

## 🐛 Troubleshooting

### Data Not Saving
- Check Firebase config is correct
- Verify database rules allow write
- Check browser console for errors

### Email Parsing Not Working
- Verify email format matches regex patterns
- Check email subject/sender filters
- Test with sample emails first

### Calculations Wrong
- Verify all input fields are numbers
- Check variance formula: `working - required`
- Ensure fill rate: `(working / required) * 100`

---

## 💡 Tips for Your Team

1. **Daily Routine**: Have shift leads fill in data at end of shift
2. **Quick Access**: Bookmark the web app or add to phone home screen
3. **Batch Entry**: Can enter multiple days/shifts at once if needed
4. **Review Weekly**: Check scorecard view every Friday
5. **Data Validation**: Set up Firebase Cloud Functions to validate data

---

## 📈 Future Enhancements

- [ ] Historical trend charts
- [ ] Export to PDF/Excel
- [ ] Automated weekly email reports
- [ ] Integration with ProLogistix/Crescent Core APIs
- [ ] Predictive analytics for staffing needs
- [ ] Mobile push notifications for low fill rates
- [ ] Manager dashboard with multiple locations

---

## 🆘 Need Help?

- Firebase Docs: https://firebase.google.com/docs
- Zapier Guides: https://zapier.com/learn
- Tailwind CSS: https://tailwindcss.com/docs

**Questions?** Check the README or reach out for support!
