const express = require('express');
const jwt = require('jsonwebtoken');
const Joi = require('joi');
const User = require('../models/User');
const dns = require('dns').promises;

const router = express.Router();

// Email verification function (optional - won't block registration if DNS fails)
async function verifyEmailExists(email) {
  // Basic format validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return { valid: false, message: 'Invalid email format' };
  }

  // Extract domain
  const domain = email.split('@')[1];
  
  // Only verify common email providers to avoid DNS issues
  const trustedDomains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com'];
  
  // If it's a trusted domain, skip DNS check
  if (trustedDomains.includes(domain.toLowerCase())) {
    return { valid: true };
  }
  
  // For other domains, try DNS check but don't fail if it errors
  try {
    const addresses = await dns.resolveMx(domain);
    if (addresses && addresses.length > 0) {
      return { valid: true };
    }
    // If no MX records but format is valid, allow it (might be a valid email)
    return { valid: true, warning: 'Could not verify email domain' };
  } catch (error) {
    // If DNS lookup fails, allow registration anyway (format is valid)
    console.log('DNS lookup failed for', domain, '- allowing registration');
    return { valid: true, warning: 'Could not verify email domain' };
  }
}

const registerSchema = Joi.object({
  name: Joi.string().required(),
  email: Joi.string().email().required(),
  password: Joi.string().min(6).required(),
  role: Joi.string().valid('official', 'admin').default('official'),
  district: Joi.string().required()
});

const loginSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().required()
});

router.post('/register', async (req, res) => {
  try {
    const { error, value } = registerSchema.validate(req.body);
    if (error) return res.status(400).json({ error: error.details[0].message });

    // Verify email exists
    const emailCheck = await verifyEmailExists(value.email);
    if (!emailCheck.valid) {
      return res.status(400).json({ error: emailCheck.message });
    }

    const existingUser = await User.findOne({ email: value.email });
    if (existingUser) return res.status(400).json({ error: 'Email already registered' });

    const user = new User(value);
    await user.save();

    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '7d' });

    res.status(201).json({
      user: { id: user._id, name: user.name, email: user.email, role: user.role, district: user.district },
      token
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.post('/login', async (req, res) => {
  try {
    const { error, value } = loginSchema.validate(req.body);
    if (error) return res.status(400).json({ error: error.details[0].message });

    const user = await User.findOne({ email: value.email });
    if (!user) return res.status(401).json({ error: 'Invalid credentials' });

    const isMatch = await user.comparePassword(value.password);
    if (!isMatch) return res.status(401).json({ error: 'Invalid credentials' });

    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '7d' });

    res.json({
      user: { id: user._id, name: user.name, email: user.email, role: user.role, district: user.district },
      token
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
