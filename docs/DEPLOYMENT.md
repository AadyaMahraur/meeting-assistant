# Deployment Guide

This document outlines the step-by-step process for deploying the Meeting-to-Execution Assistant to a production environment. 

The application uses a decoupled architecture, so the backend (FastAPI) and frontend (React/Vite) are deployed as separate services. Our recommended stack for deployment is **Railway** (Backend & Database) and **Vercel** or **Netlify** (Frontend).

---

##  Environment Variables

Before deploying, ensure you have the following credentials ready.

### Backend (FastAPI)
| Variable | Description | Example |
| :--- | :--- | :--- |
| `DATABASE_URL` | PostgreSQL connection string. | `postgresql://user:pass@host:port/db` |
| `GEMINI_API_KEY` | Your Google Gemini API Key. | `AIzaSy...` |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend URLs. | `https://my-frontend.vercel.app` |
| `MAX_FILE_SIZE` | Fixed as 10MB                 |                             |

### Frontend (React/Vite)
| Variable | Description | Example |
| :--- | :--- | :--- |
| `VITE_API_BASE_URL` | The public URL of your deployed backend. | `https://my-backend.up.railway.app` |

---

## Step-by-Step Deployment Instructions

### Part 1: Database Setup (Railway)
1. Log in to [Railway](https://railway.app/).
2. Click **New Project** -> **Provision PostgreSQL**.
3. Once provisioned, click on the Postgres service, go to the **Connect** tab, and copy the `Database URL`.

### Part 2: Backend Deployment (Railway)
1. In the same Railway project, click **New** -> **GitHub Repo** and select this repository.
2. Go to the new service's **Variables** tab and add:
   * `DATABASE_URL`: (Paste the URL from Part 1. Ensure it starts with `postgresql://` and not `postgres://`).
   * `GEMINI_API_KEY`: (Your Gemini key).
3. Go to the **Settings** tab.
   * Under **Environment**, ensure the **Start Command** is set to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   * Under **Networking**, click **Generate Domain** to get your public API URL.
4. Railway will automatically build and deploy the Python app. 

### Part 3: Frontend Deployment (Vercel)
1. Log in to [Vercel](https://vercel.com/) and click **Add New Project**.
2. Import this GitHub repository.
3. In the **Configure Project** section:
   * Set the **Framework Preset** to `Vite`.
   * Open **Environment Variables** and add `VITE_API_URL` mapped to the Railway domain generated in Part 2.
4. Click **Deploy**.
5. Once deployed, copy the Vercel URL and add it to your Railway backend's `CORS_ORIGINS` variable.

---

##  How to Redeploy

The CI/CD pipeline is automatically configured through GitHub integrations.

* **Automatic Redeploys:** Pushing any changes to the `main` branch will automatically trigger a new build and deployment on both Railway and Vercel.
* **Manual Redeploys:** * **Railway:** Go to your service, click the **Deployments** tab, click the three dots on the latest commit, and select **Redeploy**.
  * **Vercel:** Go to the project dashboard, click **Deployments**, click the three dots next to the latest build, and select **Redeploy**.

---

##  Common Issues and Solutions

### 1. CORS Errors in the Browser Console
* **Symptom:** The frontend loads, but API calls fail with a "Cross-Origin Resource Sharing" error.
* **Cause:** The backend does not recognize the frontend's domain as a safe origin.
* **Solution:** Check the `CORS_ORIGINS` environment variable on Railway. Ensure it exactly matches the frontend URL (do not include a trailing slash `/` at the end of the URL).

### 2. Database Migrations Not Applying
* **Symptom:** API returns `500 Internal Server Error` stating a table or column does not exist.
* **Cause:** The PostgreSQL database is empty or outdated.
* **Solution:** Connect to your database locally or via a GUI tool (like DBeaver) and run the setup script, or ensure your Railway start command includes an Alembic migration trigger if configured: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`.