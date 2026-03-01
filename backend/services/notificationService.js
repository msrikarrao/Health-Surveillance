const axios = require('axios');

class NotificationService {
  constructor() {
    this.twilioSid = process.env.TWILIO_ACCOUNT_SID;
    this.twilioToken = process.env.TWILIO_AUTH_TOKEN;
    this.twilioPhone = process.env.TWILIO_PHONE_NUMBER;
    this.twilioWhatsApp = process.env.TWILIO_WHATSAPP_NUMBER;
  }

  async sendSMS(to, message) {
    if (!this.twilioSid || !this.twilioToken) {
      console.log('[SMS] Twilio not configured. Message:', message);
      return { success: false, message: 'SMS service not configured' };
    }

    try {
      const response = await axios.post(
        `https://api.twilio.com/2010-04-01/Accounts/${this.twilioSid}/Messages.json`,
        new URLSearchParams({
          To: to,
          From: this.twilioPhone,
          Body: message
        }),
        {
          auth: {
            username: this.twilioSid,
            password: this.twilioToken
          }
        }
      );
      return { success: true, data: response.data };
    } catch (error) {
      console.error('[SMS] Error:', error.message);
      return { success: false, error: error.message };
    }
  }

  async sendWhatsApp(to, message) {
    if (!this.twilioSid || !this.twilioToken) {
      console.log('[WhatsApp] Twilio not configured. Message:', message);
      return { success: false, message: 'WhatsApp service not configured' };
    }

    try {
      const response = await axios.post(
        `https://api.twilio.com/2010-04-01/Accounts/${this.twilioSid}/Messages.json`,
        new URLSearchParams({
          To: `whatsapp:${to}`,
          From: `whatsapp:${this.twilioWhatsApp}`,
          Body: message
        }),
        {
          auth: {
            username: this.twilioSid,
            password: this.twilioToken
          }
        }
      );
      return { success: true, data: response.data };
    } catch (error) {
      console.error('[WhatsApp] Error:', error.message);
      return { success: false, error: error.message };
    }
  }

  async sendOutbreakAlert(prediction, officials) {
    const message = `🚨 HEALTH ALERT\n\nDistrict: ${prediction.district}\nRisk Level: ${prediction.riskLevel}\nDisease: ${prediction.predictedDisease}\nConfidence: ${prediction.confidenceScore}%\n\nImmediate action required.`;

    const results = [];
    for (const official of officials) {
      if (official.phone) {
        const smsResult = await this.sendSMS(official.phone, message);
        results.push({ type: 'SMS', phone: official.phone, ...smsResult });
      }
      if (official.whatsapp) {
        const whatsappResult = await this.sendWhatsApp(official.whatsapp, message);
        results.push({ type: 'WhatsApp', phone: official.whatsapp, ...whatsappResult });
      }
    }

    return results;
  }

  async sendReportConfirmation(phone, reportDetails) {
    const message = `✅ Health Report Submitted\n\nVillage: ${reportDetails.villageName}\nDistrict: ${reportDetails.district}\nCases: ${reportDetails.numberOfCasesReported}\n\nThank you for reporting.`;
    
    return await this.sendSMS(phone, message);
  }
}

module.exports = new NotificationService();
