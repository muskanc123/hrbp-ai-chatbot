# Environment Setup Guide

## Quick Setup

1. **Copy the example file:**
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Edit `.env` and add your Gemini API key:**
   ```bash
   nano .env  # or use any text editor
   ```

3. **Update the GEMINI_API_KEY value:**
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Getting Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Paste it in your `.env` file

## Environment Variables Explained

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `GEMINI_API_KEY` | Your Google Gemini AI API key (Required) | None - you must provide this |
| `MONGODB_URL` | MongoDB connection string | `mongodb://mongodb:27017` |
| `MONGODB_DB_NAME` | Database name | `chatbot_db` |
| `BACKEND_PORT` | Backend server port | `8000` |
| `CORS_ORIGINS` | Allowed frontend origins | `http://localhost:5173,http://localhost:3000` |
| `EXCEL_FILE_PATH` | Path to employee data Excel file | `../Banking Demo File.xlsx` |

## Troubleshooting

**Issue:** "GEMINI_API_KEY not set" error
- **Solution:** Make sure you copied `.env.example` to `.env` and added your actual API key

**Issue:** Can't find `.env.example` file
- **Solution:** Make sure you're in the `backend` directory: `cd backend`

**Issue:** API key not working
- **Solution:** Verify your API key is correct at https://makersuite.google.com/app/apikey
