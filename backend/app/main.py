from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import meetings, search

app = FastAPI(title="Meeting Assistant API")
app.include_router(search.router, prefix="/api/meetings", tags=["Search"])
app.include_router(meetings.router, prefix="/api/meetings", tags=["Meetings"])

origins = [
    "http://localhost:3000", #for local testing
    "http://localhost:5173", #to use Vite locally
    "https://meeting-assistant-red.vercel.app" 
]

# Allows API to accept requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
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