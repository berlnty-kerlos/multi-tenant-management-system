import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from app.api.routers import auth,tenants , projects, tasks

from pyfiglet import Figlet

app = FastAPI(title="Multi-Tenant Mangment System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(tasks.router, prefix="", tags=["tasks"])  # routes start with /projects/{id}/tasks and /tasks/{id}



@app.get("/",response_class=PlainTextResponse)
async def root():
    f = Figlet(font='big')  # 'standard', 'block', 'big', 'slant'
    text = "Multi-Tenant Mangment System Project"
    return f.renderText(text)