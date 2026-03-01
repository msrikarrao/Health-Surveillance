require('dotenv').config();
const readline = require('readline');
const mongoose = require('mongoose');
const HealthReport = require('./models/HealthReport');
const User = require('./models/User');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const question = (query) => new Promise((resolve) => rl.question(query, resolve));

async function connectDB() {
  await mongoose.connect(process.env.MONGODB_URI);
  console.log('✅ Connected to MongoDB\n');
}

async function getUserInput() {
  console.log('=== Health Report Data Entry ===\n');

  const villageName = await question('Village Name: ');
  const district = await question('District: ');
  const patientAge = await question('Patient Age: ');
  
  console.log('\nSymptoms (enter numbers separated by commas):');
  console.log('1. Diarrhea  2. Fever  3. Vomiting  4. Jaundice');
  console.log('5. Abdominal Pain  6. Nausea  7. Headache');
  const symptomInput = await question('Select symptoms (e.g., 1,2,3): ');
  
  const symptomMap = {
    '1': 'diarrhea', '2': 'fever', '3': 'vomiting', '4': 'jaundice',
    '5': 'abdominal_pain', '6': 'nausea', '7': 'headache'
  };
  const symptoms = symptomInput.split(',').map(s => symptomMap[s.trim()]).filter(Boolean);
  
  console.log('\nWater Source:');
  console.log('1. Well  2. River  3. Tank  4. Pipeline');
  const waterInput = await question('Select water source (1-4): ');
  const waterMap = { '1': 'well', '2': 'river', '3': 'tank', '4': 'pipeline' };
  const waterSourceType = waterMap[waterInput] || 'well';
  
  const numberOfCasesReported = await question('Number of cases: ');
  
  console.log('\nSanitation Level:');
  console.log('1. Low  2. Medium  3. High');
  const sanitationInput = await question('Select (1-3): ');
  const sanitationMap = { '1': 'low', '2': 'medium', '3': 'high' };
  const sanitationLevel = sanitationMap[sanitationInput] || 'medium';
  
  console.log('\nRainfall Level:');
  console.log('1. Low  2. Medium  3. High');
  const rainfallInput = await question('Select (1-3): ');
  const rainfallMap = { '1': 'low', '2': 'medium', '3': 'high' };
  const rainfallLevel = rainfallMap[rainfallInput] || 'medium';

  return {
    villageName,
    district,
    patientAge: parseInt(patientAge),
    symptoms,
    waterSourceType,
    numberOfCasesReported: parseInt(numberOfCasesReported),
    sanitationLevel,
    rainfallLevel
  };
}

async function main() {
  try {
    await connectDB();
    
    // Get default user
    const user = await User.findOne({ email: 'official@test.com' });
    if (!user) {
      console.log('❌ Default user not found. Run: npm run seed');
      process.exit(1);
    }

    let continueInput = true;
    let reportCount = 0;

    while (continueInput) {
      const data = await getUserInput();
      
      const report = new HealthReport({
        ...data,
        reportedBy: user._id
      });

      await report.save();
      reportCount++;
      console.log(`\n✅ Report ${reportCount} saved successfully!\n`);

      const more = await question('Add another report? (y/n): ');
      continueInput = more.toLowerCase() === 'y';
    }

    console.log(`\n🎉 Total reports added: ${reportCount}`);
    console.log('💡 Run AI prediction on dashboard to analyze data\n');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    rl.close();
    mongoose.connection.close();
  }
}

main();
