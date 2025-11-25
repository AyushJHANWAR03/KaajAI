# Deployment Guide - Kaaj AI Financial Analyzer

This guide shows how to deploy the frontend to Netlify and backend to Render.

---

## Prerequisites

- GitHub account
- Netlify account (free tier works)
- Render account (free tier works)
- OpenAI API key

---

## Step 1: Push Code to GitHub

```bash
cd /Users/ayush/Kaaj/kaaj-multi-agent-analyzer

# Add all files
git add .

# Commit
git commit -m "Initial commit: Multi-Agent AI Financial Analyzer with DSCR fix"

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend to Render

### Option A: One-Click Deploy (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account and select the `KaajAI` repository
4. Configure:
   - **Name:** `kaaj-ai-backend`
   - **Region:** Oregon (US West)
   - **Root Directory:** `backend`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free

5. **Add Environment Variables:**
   - `OPENAI_API_KEY` = `your-openai-api-key-here`
   - `DATABASE_URL` = `sqlite:///./kaaj_analyzer.db`
   - `CORS_ORIGINS` = `*`
   - `LLM_MODEL` = `gpt-4o-mini`
   - `PYTHON_VERSION` = `3.11.0`

6. Click **"Create Web Service"**

7. Wait 5-10 minutes for deployment

8. Copy your backend URL (e.g., `https://kaaj-ai-backend.onrender.com`)

### Option B: Using render.yaml

The `backend/render.yaml` file is already configured. Just:
1. Push to GitHub
2. Connect repo to Render
3. It will auto-detect the config

---

## Step 3: Deploy Frontend to Netlify

### Option A: Drag & Drop (Quick Test)

1. Build locally:
```bash
cd frontend
npm run build
```

2. Go to [Netlify](https://app.netlify.com/)
3. Drag the `frontend/dist` folder onto Netlify

### Option B: GitHub Integration (Recommended)

1. Go to [Netlify Dashboard](https://app.netlify.com/)
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect GitHub and select `KaajAI` repository
4. Configure:
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `frontend/dist`

5. **Add Environment Variable:**
   - Key: `VITE_API_URL`
   - Value: `https://kaaj-ai-backend.onrender.com` (your Render URL)

6. Click **"Deploy site"**

7. Wait 2-3 minutes

8. Copy your frontend URL (e.g., `https://kaaj-ai-analyzer.netlify.app`)

---

## Step 4: Update Frontend API URL

If you didn't add the environment variable during deployment:

1. Go to Netlify Dashboard → Your Site → **Site Configuration** → **Environment Variables**
2. Add:
   - `VITE_API_URL` = `https://kaaj-ai-backend.onrender.com`
3. **Trigger redeploy** (Deploys → Trigger deploy → Deploy site)

---

## Step 5: Test Your Deployment

1. Open your Netlify URL in browser
2. Try the Main Street Restaurant scenario from TEST_SCENARIOS.md:
   - Business Name: Main Street Restaurant
   - Industry: Restaurant
   - Business Age: 3 years
   - Loan Amount: $65,000
   - Annual Interest Rate: 10.5%
   - Term: 48 months
   - Existing Debt: $55,000
   - Monthly Deposits: `28000, 32000, 25000, 31000, 27000, 33000, 29000, 26000, 34000, 30000, 28000, 31000`
   - Monthly Withdrawals: `24000, 27000, 23000, 26000, 25000, 28000, 26000, 24000, 29000, 27000, 25000, 27000`
   - NSF Fees: 3

3. Expected Results:
   - **DSCR:** 1.17 (includes existing debt!)
   - **Score:** ~40/100
   - **Risk Level:** HIGH
   - **Recommendation:** DECLINE or APPROVE_WITH_CONDITIONS

---

## Troubleshooting

### CORS Issues
✅ Already fixed! Backend uses `allow_origins=["*"]`

### API Not Connecting
- Check Render backend logs for errors
- Verify `OPENAI_API_KEY` is set in Render
- Make sure Render service is not sleeping (free tier sleeps after 15min inactivity)

### Frontend Build Fails
```bash
# Test build locally first
cd frontend
npm install
npm run build
```

### Backend Fails to Start
- Check Python version is 3.11+
- Verify all dependencies in requirements.txt
- Check Render logs for specific error

---

## Production URLs

After deployment, you'll have:

- **Frontend:** `https://your-app.netlify.app`
- **Backend:** `https://kaaj-ai-backend.onrender.com`
- **API Docs:** `https://kaaj-ai-backend.onrender.com/docs`
- **Health Check:** `https://kaaj-ai-backend.onrender.com/api/health`

---

## Cost

- **Netlify Free Tier:** 100GB bandwidth, 300 build minutes/month
- **Render Free Tier:** 750 hours/month, sleeps after 15min inactivity
- **Total Cost:** $0/month (but OpenAI API usage costs apply)

---

## Monitoring

### Backend Health
```bash
curl https://kaaj-ai-backend.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "agents_loaded": ["FinancialAnalyzerAgent", "RiskAssessorAgent", "MemoGeneratorAgent"]
}
```

### Wake Up Sleeping Backend
On Render free tier, first request after 15min takes ~30 seconds to wake up.
Just refresh the page if you get a timeout.

---

## Video Demo Tips

1. **Show the Fix:**
   - Explain the DSCR bug (only counted new loan, not total debt)
   - Show Main Street Restaurant: DSCR 1.17 vs wrong 4.08
   - Show score dropped from 92 to 40

2. **Demo the App:**
   - Walk through all 5 steps of the form
   - Show real-time analysis (30 seconds)
   - Show credit memo generation

3. **Highlight Features:**
   - Multi-agent architecture (Financial Analyzer, Risk Assessor, Memo Generator)
   - Industry-standard DSCR calculation
   - Beautiful UI with step-by-step wizard
   - Test scenarios included

4. **Show Different Scenarios:**
   - ABC Construction (APPROVE - score 93)
   - Main Street Restaurant (CONDITIONS - score 40)
   - Quick Cash Payday (DECLINE - score 19)

---

## Need Help?

- Frontend Issues: Check Netlify build logs
- Backend Issues: Check Render logs
- CORS Issues: Already handled with `*`
- OpenAI Issues: Verify API key and billing

---

**You're all set!** 🚀

Now push to GitHub and follow the deployment steps above.
