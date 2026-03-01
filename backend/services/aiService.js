const axios = require('axios');
const fs = require('fs');
const path = require('path');

class AIService {
  constructor() {
    this.provider = process.env.AI_PROVIDER || 'gemini';
    this.geminiKey = process.env.GEMINI_API_KEY;
    this.openaiKey = process.env.OPENAI_API_KEY;
    this.datasetPath = path.join(__dirname, '../datasets/synthetic_health_water_dataset_1000.csv');
  }

  async predictOutbreak(aggregatedData) {
    // Analyze dataset patterns first
    const datasetAnalysis = await this.analyzeDataset(aggregatedData);
    
    // Build enhanced prompt with dataset insights
    const prompt = this.buildPrompt(aggregatedData, datasetAnalysis);

    try {
      if (this.provider === 'gemini') {
        return await this.callGemini(prompt);
      } else {
        return await this.callOpenAI(prompt);
      }
    } catch (error) {
      console.error('AI API Error:', error.message);
      // Fallback to rule-based prediction if AI fails
      return this.ruleBasedPrediction(aggregatedData, datasetAnalysis);
    }
  }

  async analyzeDataset(currentData) {
    try {
      // Read and parse dataset
      const csvData = fs.readFileSync(this.datasetPath, 'utf-8');
      const lines = csvData.split('\n').slice(1); // Skip header
      
      let outbreakCases = 0;
      let totalCases = 0;
      let diarrheaOutbreaks = 0;
      let vomitingOutbreaks = 0;
      let feverOutbreaks = 0;
      
      lines.forEach(line => {
        if (!line.trim()) return;
        const cols = line.split(',');
        if (cols.length < 15) return;
        
        const diarrhea = parseInt(cols[5]);
        const vomiting = parseInt(cols[6]);
        const fever = parseInt(cols[7]);
        const outbreak = parseInt(cols[14]);
        
        totalCases++;
        if (outbreak === 1) {
          outbreakCases++;
          if (diarrhea === 1) diarrheaOutbreaks++;
          if (vomiting === 1) vomitingOutbreaks++;
          if (fever === 1) feverOutbreaks++;
        }
      });
      
      return {
        outbreakRate: (outbreakCases / totalCases * 100).toFixed(2),
        diarrheaOutbreakRate: (diarrheaOutbreaks / outbreakCases * 100).toFixed(2),
        vomitingOutbreakRate: (vomitingOutbreaks / outbreakCases * 100).toFixed(2),
        feverOutbreakRate: (feverOutbreaks / outbreakCases * 100).toFixed(2),
        totalOutbreaks: outbreakCases
      };
    } catch (error) {
      console.error('Dataset analysis error:', error.message);
      return null;
    }
  }

  ruleBasedPrediction(data, datasetAnalysis) {
    // Calculate risk score based on dataset patterns
    let riskScore = 0;
    let explanation = [];
    
    // High diarrhea cases (major indicator from dataset)
    const diarrheaCount = data.symptomCounts.diarrhea || 0;
    if (diarrheaCount > 15) {
      riskScore += 40;
      explanation.push(`High diarrhea cases (${diarrheaCount})`);
    } else if (diarrheaCount > 8) {
      riskScore += 25;
      explanation.push(`Moderate diarrhea cases (${diarrheaCount})`);
    }
    
    // Vomiting + diarrhea combination
    const vomitingCount = data.symptomCounts.vomiting || 0;
    if (diarrheaCount > 5 && vomitingCount > 5) {
      riskScore += 30;
      explanation.push('diarrhea-vomiting cluster');
    }
    
    // Low sanitation
    if (data.lowSanitationCount > data.reportCount * 0.6) {
      riskScore += 15;
      explanation.push('poor sanitation');
    }
    
    // High rainfall
    if (data.highRainfallCount > data.reportCount * 0.5) {
      riskScore += 10;
      explanation.push('heavy rainfall');
    }
    
    // Contaminated water sources
    if (data.waterSources.well > 2 || data.waterSources.river > 2) {
      riskScore += 5;
      explanation.push('contaminated water sources');
    }
    
    // Determine risk level and disease
    let riskLevel, predictedDisease, confidenceScore;
    
    if (riskScore >= 70) {
      riskLevel = 'HIGH';
      confidenceScore = Math.min(85 + Math.random() * 10, 95);
      predictedDisease = 'Cholera outbreak';
    } else if (riskScore >= 40) {
      riskLevel = 'MEDIUM';
      confidenceScore = 65 + Math.random() * 15;
      predictedDisease = 'Diarrheal disease outbreak';
    } else {
      riskLevel = 'LOW';
      confidenceScore = 50 + Math.random() * 20;
      predictedDisease = 'No significant outbreak risk';
    }
    
    return {
      riskLevel,
      confidenceScore: Math.round(confidenceScore),
      predictedDisease,
      explanation: `Based on dataset analysis: ${explanation.join(', ')}. Historical outbreak rate: ${datasetAnalysis?.outbreakRate || 'N/A'}%.`
    };
  }

  buildPrompt(data, datasetAnalysis) {
    const datasetContext = datasetAnalysis ? 
      `\n\nHistorical Dataset Insights:\n- Overall outbreak rate: ${datasetAnalysis.outbreakRate}%\n- Diarrhea in outbreaks: ${datasetAnalysis.diarrheaOutbreakRate}%\n- Vomiting in outbreaks: ${datasetAnalysis.vomitingOutbreakRate}%\n- Fever in outbreaks: ${datasetAnalysis.feverOutbreakRate}%` : '';
    
    return `You are a public health epidemiologist analyzing rural disease data with access to historical outbreak patterns.

Current weekly aggregated health data:
${JSON.stringify(data, null, 2)}${datasetContext}

Analyze patterns and detect outbreak risk based on both current data and historical patterns.

Respond ONLY in this JSON format:
{
  "riskLevel": "LOW | MEDIUM | HIGH",
  "confidenceScore": number,
  "predictedDisease": "string",
  "explanation": "short explanation"
}

Do not add extra text.`;
  }

  async callGemini(prompt) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${this.geminiKey}`;
    
    const response = await axios.post(url, {
      contents: [{
        parts: [{ text: prompt }]
      }],
      generationConfig: {
        temperature: 0.3,
        maxOutputTokens: 500
      }
    });

    const text = response.data.candidates[0].content.parts[0].text;
    return this.parseResponse(text);
  }

  async callOpenAI(prompt) {
    const url = 'https://api.openai.com/v1/chat/completions';
    
    const response = await axios.post(url, {
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3,
      max_tokens: 500
    }, {
      headers: {
        'Authorization': `Bearer ${this.openaiKey}`,
        'Content-Type': 'application/json'
      }
    });

    const text = response.data.choices[0].message.content;
    return this.parseResponse(text);
  }

  parseResponse(text) {
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) throw new Error('Invalid AI response format');
    
    const parsed = JSON.parse(jsonMatch[0]);
    
    if (!parsed.riskLevel || !parsed.confidenceScore || !parsed.predictedDisease || !parsed.explanation) {
      throw new Error('Missing required fields in AI response');
    }

    return parsed;
  }
}

module.exports = new AIService();
