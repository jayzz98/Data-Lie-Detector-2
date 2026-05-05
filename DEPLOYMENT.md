# Deployment Guide

Follow these steps to deploy the **Data Lie Detector** to a production environment.

## 1. Supported Platforms
- **Replit:** Best for quick deployment. Use the "Deploy" button and choose "Autoscale".
- **Render / Railway / Heroku:** Use the provided `Procfile`.

## 2. Environment Variables

You MUST set the following environment variables in your hosting provider's dashboard:

| Variable | Description | Example |
| :--- | :--- | :--- |
| `GOOGLE_CLIENT_ID` | Your Google OAuth Client ID | `12345-abcde.apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | Your Google OAuth Client Secret | `GOCSPX-abcde12345` |
| `REDIRECT_URI` | **CRITICAL:** The public URL of your Streamlit app | `https://8502.my-app.user.replit.dev` |

## 3. Redirect URI Configuration
When setting up your OAuth credentials in the Google/Microsoft Cloud Console:
- The **Authorized Redirect URI** must match exactly what you put in the `REDIRECT_URI` environment variable.
- Example for Replit: `https://8502.my-repl-name.my-username.replit.dev`

## 4. How the App Works
- The app runs a FastAPI "Gateway" on the main port (e.g., 80 or 8080).
- This gateway serves the landing page at `/` and embeds the Streamlit app (running on port 8502) at `/app`.
