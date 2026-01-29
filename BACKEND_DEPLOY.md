# Deploying the AI Backend

Since your Frontend is on Vercel, you need to deploy your Python Backend so the Frontend can talk to it. We recommend **Render** as it is free and easy for Python apps.

## Part 1: Deploy Backend to Render

1.  Push your latest code (including `api_server.py`) to GitHub.
2.  Sign up at [render.com](https://render.com).
3.  Click **"New +"** -> **"Web Service"**.
4.  Connect your GitHub repository.
5.  **Configure the Service**:
    *   **Name**: `wallet-risk-api` (or similar)
    *   **Root Directory**: Leave empty (repository root).
    *   **Environment**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `python api_server.py`
6.  **Environment Variables** (Advanced):
    *   Add `OPENAI_API_KEY` : `sk-...` (Your OpenAI Key)
7.  Click **"Create Web Service"**.

Render will deploy your API. Once finished, it will give you a URL like:
`https://wallet-risk-api.onrender.com`

## Part 2: Connect Frontend to Backend

Now tell your Vercel Frontend where the Backend lives.

1.  Go to your Project Dashboard on **Vercel**.
2.  Click **"Settings"** -> **"Environment Variables"**.
3.  Add a new Variable:
    *   **Key**: `NEXT_PUBLIC_API_URL`
    *   **Value**: `https://wallet-risk-api.onrender.com` (The URL you got from Render - **no trailing slash**)
4.  **Save**.
5.  **Redeploy** your frontend (go to Deployments -> select latest -> Redeploy) for the changes to take effect.

## Summary

-   **Frontend (Vercel)** serves the UI.
-   **Backend (Render)** runs the AI.
-   **NEXT_PUBLIC_API_URL** connects them.
