# 🚀 Crescent Scorecard Deployment Checklist

## Pre-Deployment Setup

### 1. Firebase Setup (15 minutes)
- [ ] Create Firebase project at console.firebase.google.com
- [ ] Add web app to project
- [ ] Enable Realtime Database
- [ ] Copy Firebase config
- [ ] Update config in crescent-scorecard.html (lines 21-28)
- [ ] Set initial database rules to allow read/write
- [ ] Test connection by opening HTML file locally

### 2. Local Testing (10 minutes)
- [ ] Open crescent-scorecard.html in browser
- [ ] Try entering test data for a shift
- [ ] Verify data appears in Firebase Console
- [ ] Test switching between Scorecard and Data Entry views
- [ ] Check mobile responsiveness (browser dev tools)

---

## Deployment Options

### Option A: Firebase Hosting (Recommended)
**Time:** 15 minutes | **Cost:** Free | **Difficulty:** Easy

- [ ] Install Node.js if not already installed
- [ ] Install Firebase CLI: `npm install -g firebase-tools`
- [ ] Login: `firebase login`
- [ ] Initialize: `firebase init hosting`
  - [ ] Select your project
  - [ ] Public directory: current directory (.)
  - [ ] Single-page app: No
- [ ] Deploy: `firebase deploy`
- [ ] Test deployed URL
- [ ] Share URL with team

**Result:** URL like https://your-project.web.app

---

### Option B: Netlify (Alternative)
**Time:** 5 minutes | **Cost:** Free | **Difficulty:** Very Easy

- [ ] Go to netlify.com
- [ ] Sign up or login
- [ ] Drag and drop crescent-scorecard.html
- [ ] Get deployment URL
- [ ] (Optional) Set custom domain

**Result:** URL like https://your-app.netlify.app

---

### Option C: Vercel
**Time:** 10 minutes | **Cost:** Free | **Difficulty:** Easy

- [ ] Go to vercel.com
- [ ] Sign up or login
- [ ] Import from GitHub (or drag & drop)
- [ ] Deploy
- [ ] Get deployment URL

---

## Post-Deployment Testing

### 3. Production Testing (10 minutes)
- [ ] Open deployed URL on desktop
- [ ] Open deployed URL on mobile phone
- [ ] Test data entry from both devices
- [ ] Verify real-time sync between devices
- [ ] Check all calculations are correct
- [ ] Test week navigation
- [ ] Verify totals match

---

## Email Automation Setup (Optional)

### Option 1: Zapier (Easiest - 20 minutes)
- [ ] Create Zapier account (free tier works)
- [ ] Create new Zap
- [ ] Trigger: Gmail "New Email"
  - [ ] Add filter for subject: "Shift Report"
- [ ] Action: "Code by Zapier" or "Email Parser"
  - [ ] Parse date, shift, and all metrics
- [ ] Action: "Webhooks by Zapier"
  - [ ] Method: PUT
  - [ ] URL: Your Firebase database REST endpoint
  - [ ] Body: Parsed data as JSON
- [ ] Test with sample email
- [ ] Turn on Zap

---

### Option 2: Python Script (Advanced - 30 minutes)
- [ ] Server/computer that runs 24/7 (or use cloud VM)
- [ ] Install Python 3: `python3 --version`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Update email_parser.py with Firebase URL
- [ ] Set up environment variables:
  ```bash
  export EMAIL_ACCOUNT="your-email@gmail.com"
  export EMAIL_PASSWORD="your-app-password"
  ```
- [ ] Test parser: `python3 email_parser.py test`
- [ ] Run manual test: `python3 email_parser.py`
- [ ] Set up automation:
  - [ ] Run setup script: `./setup_automation.sh`
  - [ ] Or manually add cron job: `crontab -e`
  - [ ] Add: `0 * * * * /path/to/email_parser.py >> ~/scorecard.log 2>&1`
- [ ] Monitor log file for errors

---

### Option 3: Google Apps Script (Gmail Users - 25 minutes)
- [ ] Open script.google.com
- [ ] Create new project
- [ ] Paste script from SETUP_GUIDE.md
- [ ] Update Firebase URL
- [ ] Test run the script
- [ ] Create time-based trigger (hourly)
- [ ] Authorize script
- [ ] Monitor execution logs

---

## Team Onboarding

### 4. Train Your Team (15 minutes per person)
- [ ] Share deployed URL
- [ ] Show how to enter shift data
- [ ] Explain fill rate calculations
- [ ] Demo mobile usage
- [ ] Show how to review historical data
- [ ] Explain when/how to use scorecard view
- [ ] Answer questions

### 5. Create Email Templates
- [ ] Share EMAIL_TEMPLATE.txt with team
- [ ] Choose which template format to use
- [ ] Create Gmail/Outlook template if possible
- [ ] Test email with automation (if enabled)

---

## Security & Permissions

### 6. Lock Down Firebase (Important!)
- [ ] Go to Firebase Console → Database → Rules
- [ ] Replace with production rules:
  ```json
  {
    "rules": {
      "scorecard": {
        ".read": true,
        ".write": true
      }
    }
  }
  ```
- [ ] For additional security, add authentication:
  - [ ] Enable Email/Password auth in Firebase Console
  - [ ] Update rules to require authentication
  - [ ] Add login page to app (see SETUP_GUIDE.md)

---

## Monitoring & Maintenance

### 7. Set Up Monitoring (10 minutes)
- [ ] Bookmark Firebase Console
- [ ] Check usage daily for first week
- [ ] Monitor email parser logs (if using)
- [ ] Set up Firebase alerts for unusual activity
- [ ] Create backup routine (Firebase auto-backs up, but good to export monthly)

### 8. Weekly Review Process
- [ ] Assign someone to review data weekly
- [ ] Check for anomalies or missing entries
- [ ] Verify calculations are correct
- [ ] Address any team questions
- [ ] Monitor fill rate trends

---

## Troubleshooting Checklist

### Common Issues

**Data Not Saving**
- [ ] Check Firebase config is correct
- [ ] Verify database rules allow write
- [ ] Check browser console for errors (F12)
- [ ] Try different browser

**Email Parser Not Working**
- [ ] Verify email format matches template
- [ ] Check credentials are correct
- [ ] Verify Firebase URL is correct
- [ ] Test with python email_parser.py test
- [ ] Check log files for errors

**Mobile Issues**
- [ ] Clear browser cache
- [ ] Try adding to home screen
- [ ] Check internet connection
- [ ] Verify Firebase rules allow access

**Calculation Errors**
- [ ] Verify input data is correct
- [ ] Check for zero values in Required field
- [ ] Ensure numbers (not text) in input fields

---

## Success Metrics

### Measure Your Success
After 2 weeks, evaluate:
- [ ] Average time to enter shift data: Target < 2 minutes
- [ ] Data accuracy: Target 100% (no manual calc errors)
- [ ] Team adoption: Target 100% using new system
- [ ] Fill rate visibility: Real-time vs. end-of-week
- [ ] Time saved per week: Target 2+ hours

---

## Quick Start Commands

```bash
# Test locally
open crescent-scorecard.html

# Deploy to Firebase
firebase deploy

# Test email parser
python3 email_parser.py test

# Check parser logs
tail -f ~/crescent_scorecard.log

# View cron jobs
crontab -l

# Manual parser run
python3 email_parser.py
```

---

## Support Resources

- **Firebase Issues:** https://firebase.google.com/support
- **Zapier Help:** https://zapier.com/help
- **Python Email:** https://docs.python.org/3/library/email.html
- **Cron Setup:** https://crontab.guru/

---

## Emergency Contacts

**If Something Breaks:**
1. Check Firebase Console for errors
2. Review browser console (F12)
3. Check email parser logs
4. Verify internet connectivity
5. Try manual data entry as backup

**Rollback Plan:**
- Original Excel sheet available as backup
- All data in Firebase is preserved
- Can export Firebase data to Excel if needed

---

## Next Steps After Deployment

### Week 1: Monitor & Adjust
- Daily check-ins with team
- Fix any issues immediately
- Gather feedback
- Make minor adjustments

### Week 2: Optimize
- Review automation logs
- Optimize email parsing
- Add any missing features
- Improve user experience based on feedback

### Month 1: Analyze
- Compare to old Excel process
- Calculate time savings
- Review fill rate trends
- Plan future enhancements

---

## Completion Checklist

- [ ] Firebase set up and tested
- [ ] Application deployed and accessible
- [ ] Team trained and onboarded
- [ ] Email automation configured (optional)
- [ ] Security rules implemented
- [ ] Monitoring in place
- [ ] Backup process established
- [ ] Success metrics defined
- [ ] Team feedback collected
- [ ] Old Excel process deprecated

---

**Estimated Total Time:**
- Basic setup: 1-2 hours
- With email automation: 2-3 hours
- Team training: 30 minutes - 1 hour

**Ready to deploy? Start with step 1 above!** 🚀
