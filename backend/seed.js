require('dotenv').config();
const mongoose = require('mongoose');
const User = require('./models/User');
const HealthReport = require('./models/HealthReport');

const connectDB = async () => {
  await mongoose.connect(process.env.MONGODB_URI);
  console.log('MongoDB connected');
};

const seedData = async () => {
  try {
    await connectDB();

    // Clear existing data
    await User.deleteMany({});
    await HealthReport.deleteMany({});
    console.log('Cleared existing data');

    // Create test user
    const user = new User({
      name: 'Test Official',
      email: 'official@test.com',
      password: 'password123',
      role: 'district_officer',
      district: 'Kamrup'
    });
    await user.save();
    console.log('Created test user: official@test.com / password123');

    // Create sample reports
    const reports = [
      {
        villageName: 'Guwahati Village',
        district: 'Kamrup',
        patientAge: 25,
        symptoms: ['diarrhea', 'fever', 'vomiting'],
        waterSourceType: 'well',
        numberOfCasesReported: 3,
        sanitationLevel: 'low',
        rainfallLevel: 'high',
        reportedBy: user._id,
        date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000) // 2 days ago
      },
      {
        villageName: 'Dispur Village',
        district: 'Kamrup',
        patientAge: 35,
        symptoms: ['diarrhea', 'abdominal_pain', 'nausea'],
        waterSourceType: 'river',
        numberOfCasesReported: 5,
        sanitationLevel: 'low',
        rainfallLevel: 'high',
        reportedBy: user._id,
        date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000)
      },
      {
        villageName: 'Guwahati Village',
        district: 'Kamrup',
        patientAge: 12,
        symptoms: ['fever', 'vomiting', 'headache'],
        waterSourceType: 'well',
        numberOfCasesReported: 2,
        sanitationLevel: 'medium',
        rainfallLevel: 'high',
        reportedBy: user._id,
        date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000)
      },
      {
        villageName: 'Beltola Village',
        district: 'Kamrup',
        patientAge: 45,
        symptoms: ['diarrhea', 'fever'],
        waterSourceType: 'tank',
        numberOfCasesReported: 4,
        sanitationLevel: 'low',
        rainfallLevel: 'medium',
        reportedBy: user._id,
        date: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000)
      },
      {
        villageName: 'Dispur Village',
        district: 'Kamrup',
        patientAge: 8,
        symptoms: ['vomiting', 'diarrhea', 'abdominal_pain'],
        waterSourceType: 'river',
        numberOfCasesReported: 6,
        sanitationLevel: 'low',
        rainfallLevel: 'high',
        reportedBy: user._id,
        date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000)
      },
      {
        villageName: 'Jalukbari Village',
        district: 'Kamrup',
        patientAge: 55,
        symptoms: ['jaundice', 'fever', 'nausea'],
        waterSourceType: 'well',
        numberOfCasesReported: 2,
        sanitationLevel: 'medium',
        rainfallLevel: 'medium',
        reportedBy: user._id,
        date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)
      },
      {
        villageName: 'Guwahati Village',
        district: 'Kamrup',
        patientAge: 30,
        symptoms: ['diarrhea', 'vomiting'],
        waterSourceType: 'well',
        numberOfCasesReported: 7,
        sanitationLevel: 'low',
        rainfallLevel: 'high',
        reportedBy: user._id,
        date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000)
      },
      {
        villageName: 'Beltola Village',
        district: 'Kamrup',
        patientAge: 18,
        symptoms: ['fever', 'headache', 'abdominal_pain'],
        waterSourceType: 'tank',
        numberOfCasesReported: 3,
        sanitationLevel: 'medium',
        rainfallLevel: 'high',
        reportedBy: user._id,
        date: new Date()
      }
    ];

    await HealthReport.insertMany(reports);
    console.log(`Created ${reports.length} sample health reports`);

    console.log('\n✅ Database seeded successfully!');
    console.log('\nLogin credentials:');
    console.log('Email: official@test.com');
    console.log('Password: password123');
    console.log('\nYou can now run AI prediction on the dashboard!');

    process.exit(0);
  } catch (error) {
    console.error('Seeding error:', error);
    process.exit(1);
  }
};

seedData();
