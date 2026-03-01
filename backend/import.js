require('dotenv').config();
const fs = require('fs');
const path = require('path');
const mongoose = require('mongoose');
const HealthReport = require('./models/HealthReport');
const User = require('./models/User');

async function connectDB() {
  await mongoose.connect(process.env.MONGODB_URI);
  console.log('✅ Connected to MongoDB');
}

async function importCSV(filePath) {
  try {
    await connectDB();

    const user = await User.findOne({ email: 'official@test.com' });
    if (!user) {
      console.log('❌ Default user not found. Run: npm run seed');
      process.exit(1);
    }

    const csvData = fs.readFileSync(filePath, 'utf-8');
    const lines = csvData.split('\n').slice(1); // Skip header
    
    let imported = 0;
    let skipped = 0;

    console.log(`📊 Processing ${lines.length} records...\n`);

    for (const line of lines) {
      if (!line.trim()) continue;

      const cols = line.split(',');
      if (cols.length < 15) {
        skipped++;
        continue;
      }

      try {
        const symptoms = [];
        if (cols[5] === '1') symptoms.push('diarrhea');
        if (cols[6] === '1') symptoms.push('vomiting');
        if (cols[7] === '1') symptoms.push('fever');

        if (symptoms.length === 0) {
          skipped++;
          continue;
        }

        const ageGroup = cols[4];
        let age = 25;
        if (ageGroup === '0-5') age = 3;
        else if (ageGroup === '6-18') age = 12;
        else if (ageGroup === '19-40') age = 30;
        else if (ageGroup === '41-60') age = 50;
        else if (ageGroup === '60+') age = 65;

        const report = new HealthReport({
          villageName: cols[1],
          district: 'Kamrup',
          patientAge: age,
          symptoms,
          date: new Date(cols[0]),
          waterSourceType: 'well',
          numberOfCasesReported: 1,
          sanitationLevel: parseFloat(cols[13]) > 50 ? 'low' : 'medium',
          rainfallLevel: parseFloat(cols[13]) > 30 ? 'high' : 'medium',
          reportedBy: user._id
        });

        await report.save();
        imported++;

        if (imported % 50 === 0) {
          console.log(`✅ Imported ${imported} records...`);
        }
      } catch (err) {
        skipped++;
      }
    }

    console.log(`\n🎉 Import Complete!`);
    console.log(`✅ Imported: ${imported} records`);
    console.log(`⚠️  Skipped: ${skipped} records`);
    console.log(`\n💡 Run AI prediction on dashboard to analyze data\n`);

  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    mongoose.connection.close();
  }
}

const csvPath = process.argv[2] || path.join(__dirname, 'datasets/synthetic_health_water_dataset_1000.csv');
importCSV(csvPath);
