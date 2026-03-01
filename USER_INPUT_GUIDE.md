# 📥 User Input Guide

## Three Ways to Add Health Data

### 1️⃣ Web Interface (Recommended)
**Best for:** Individual reports, real-time entry

```bash
# Start the application
cd backend && npm run dev
cd frontend && npm run dev

# Open browser: http://localhost:3000
# Login: official@test.com / password123
# Go to "Submit Report" page
```

**Features:**
- ✅ User-friendly form
- ✅ Real-time validation
- ✅ Instant feedback
- ✅ Mobile responsive

---

### 2️⃣ Interactive CLI (Terminal)
**Best for:** Quick data entry, offline mode

```bash
cd backend
npm run input
```

**Example Session:**
```
=== Health Report Data Entry ===

Village Name: Guwahati Village
District: Kamrup
Patient Age: 25

Symptoms (enter numbers separated by commas):
1. Diarrhea  2. Fever  3. Vomiting  4. Jaundice
5. Abdominal Pain  6. Nausea  7. Headache
Select symptoms (e.g., 1,2,3): 1,2,3

Water Source:
1. Well  2. River  3. Tank  4. Pipeline
Select water source (1-4): 1

Number of cases: 3

Sanitation Level:
1. Low  2. Medium  3. High
Select (1-3): 1

Rainfall Level:
1. Low  2. Medium  3. High
Select (1-3): 3

✅ Report 1 saved successfully!

Add another report? (y/n): y
```

**Features:**
- ✅ Fast keyboard input
- ✅ Works offline
- ✅ Multiple reports in one session
- ✅ No browser needed

---

### 3️⃣ Bulk CSV Import
**Best for:** Large datasets, historical data

```bash
cd backend

# Import default dataset (1000 records)
npm run import

# Or import custom CSV file
node import.js path/to/your/data.csv
```

**CSV Format:**
```csv
date,village_id,latitude,longitude,age_group,symptom_diarrhea,symptom_vomiting,symptom_fever,water_turbidity,water_ph,water_temp,tds,coliform_present,rainfall_mm,confirmed_outbreak
2025-01-01,V001,26.123,91.456,41-60,1,0,0,6.1,6.86,27.5,168.4,0,7.8,0
```

**Features:**
- ✅ Import 1000+ records instantly
- ✅ Historical data analysis
- ✅ Batch processing
- ✅ Dataset integration

---

## 📊 Comparison

| Method | Speed | Use Case | Validation |
|--------|-------|----------|------------|
| **Web Interface** | Moderate | Individual reports | Real-time |
| **CLI Input** | Fast | Quick entry | On submit |
| **CSV Import** | Very Fast | Bulk data | Batch |

---

## 🎯 Recommended Workflow

### For Field Workers (ASHA, Volunteers)
1. Use **Web Interface** on mobile/tablet
2. Submit reports as cases are discovered
3. Works with internet connection

### For Health Officials
1. Use **CLI Input** for quick data entry
2. Use **CSV Import** for historical data
3. View predictions on dashboard

### For Data Analysts
1. Use **CSV Import** for large datasets
2. Analyze patterns on dashboard
3. Export predictions for reports

---

## 🔧 Setup Requirements

### Web Interface
- Browser (Chrome, Firefox, Safari)
- Internet connection
- Login credentials

### CLI Input
- Node.js installed
- MongoDB running
- Terminal access

### CSV Import
- Node.js installed
- MongoDB running
- CSV file in correct format

---

## 📝 Data Validation

All methods validate:
- ✅ Village name (required)
- ✅ District (required)
- ✅ Patient age (0-120)
- ✅ Symptoms (at least 1)
- ✅ Water source (valid type)
- ✅ Number of cases (≥ 1)
- ✅ Sanitation level (low/medium/high)
- ✅ Rainfall level (low/medium/high)

---

## 🚀 Quick Start Examples

### Example 1: Single Report (Web)
```
1. Open http://localhost:3000
2. Login
3. Click "Submit Report"
4. Fill form
5. Submit
```

### Example 2: Multiple Reports (CLI)
```bash
cd backend
npm run input

# Enter 5-10 reports interactively
# Press 'n' when done
```

### Example 3: Bulk Import (CSV)
```bash
cd backend
npm run import

# Imports all records from dataset
# View on dashboard
```

---

## 💡 Tips

### For Accurate Predictions
- Submit at least **5-10 reports** per week
- Include **multiple villages** for better analysis
- Update **water source** and **sanitation** data regularly
- Record **rainfall levels** during monsoon

### For Best Performance
- Use **CLI** for offline data collection
- Use **CSV import** for historical analysis
- Use **Web interface** for real-time monitoring

---

## 🆘 Troubleshooting

### CLI Input Issues
```bash
# If "Default user not found"
npm run seed

# If MongoDB connection error
net start MongoDB  # Windows
sudo systemctl start mongod  # Linux
```

### CSV Import Issues
```bash
# If file not found
node import.js datasets/synthetic_health_water_dataset_1000.csv

# If format error
# Check CSV has correct columns
```

### Web Interface Issues
```bash
# If can't login
# Clear browser localStorage
# Re-seed database: npm run seed
```

---

## 📞 Support

**Need Help?**
1. Check error messages in terminal
2. Verify MongoDB is running
3. Ensure correct file paths
4. Review CSV format

**Common Issues:**
- ❌ MongoDB not running → Start MongoDB service
- ❌ User not found → Run `npm run seed`
- ❌ CSV format error → Check column order
- ❌ Validation error → Check data types

---

## ✅ Success Indicators

After adding data, you should see:
- ✅ "Report saved successfully" message
- ✅ Data appears on dashboard
- ✅ Can run AI prediction
- ✅ Charts show updated statistics

---

**🎉 You're ready to collect health data!**

Choose the method that works best for your use case and start adding reports.
