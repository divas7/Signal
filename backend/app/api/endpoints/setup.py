from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.services.connection_manager import manager

router = APIRouter()

@router.get("/status")
async def get_system_status() -> Dict[str, Any]:
    """
    Get the overall system status and connector health.
    Used by the frontend to show the 'Setup Wizard' or 'Blocked State'.
    """
    return await manager.check_health()

@router.post("/configure")
async def configure_keys(config: Dict[str, str]):
    """
    Endpoint to receive API keys from the Setup Wizard.
    In production, this should write to a secure vault or env vars.
    For this demo, we might just update the in-memory settings or warn the user.
    """
    # STRICT SECURITY: Do not actually save keys to disk in this demo.
    # Just validate them and update memory? 
    # Or tell the user to restart with env vars.
    
    # We will simulate a successful configuration for the session if keys look valid
    # strictly for the purpose of moving past the wizard during a demo if needed,
    # but the requirement says "Secrets must be stored only in backend environment variables".
    
    return {"message": "Configuration received. Please restart backend with new environment variables for permanent effect."}
