from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Meeting Assistant API")

# CORS Middleware 
# This allows your API to accept requests from different domains (like a React or Vue frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace "*" with frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check Endpoint 
@app.get("/api/health")
async def health_check():
    # currently checks if server running
    # will check connection to db and ai pipeline later
    return {
        "status": "healthy",
        "message": "Meeting Assistant API is up and running"
    }

# Root endpoint 
@app.get("/")
async def root():
    return {"message": "Welcome to the Meeting Assistant API"}