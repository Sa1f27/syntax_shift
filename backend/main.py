from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os
from pathlib import Path

# Import our custom modules
from transformer import CodeTransformer
from converter import LanguageConverter
from explainer import CodeExplainer

app = FastAPI(title="Syntax Shift API", version="1.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Initialize our core components
transformer = CodeTransformer()
converter = LanguageConverter()
explainer = CodeExplainer()

# Request/Response models
class CodeRequest(BaseModel):
    code: str
    source_language: str = "python"
    target_language: str = None
    operation: str  # "transform", "optimize", "convert", "explain"

class CodeResponse(BaseModel):
    original_code: str
    transformed_code: str
    explanations: list
    suggestions: list
    success: bool
    error_message: str = None

@app.get("/")
async def serve_frontend():
    """Serve the main frontend page"""
    frontend_file = frontend_path / "index.html"
    if frontend_file.exists():
        return FileResponse(str(frontend_file))
    return {"message": "Syntax Shift API is running! Frontend not found."}

@app.post("/api/transform", response_model=CodeResponse)
async def transform_code(request: CodeRequest):
    """Main endpoint for code transformation operations"""
    try:
        result = {
            "original_code": request.code,
            "transformed_code": request.code,
            "explanations": [],
            "suggestions": [],
            "success": True
        }
        
        if request.operation == "optimize":
            # Optimize the code for performance and readability
            optimized_code, suggestions = transformer.optimize_code(
                request.code, request.source_language
            )
            result["transformed_code"] = optimized_code
            result["suggestions"] = suggestions
            
        elif request.operation == "transform":
            # Apply general transformations (DRY, clean structure)
            transformed_code, suggestions = transformer.transform_code(
                request.code, request.source_language
            )
            result["transformed_code"] = transformed_code
            result["suggestions"] = suggestions
            
        elif request.operation == "convert":
            # Convert to target language
            if not request.target_language:
                raise HTTPException(400, "Target language required for conversion")
            
            converted_code, notes = converter.convert_language(
                request.code, request.source_language, request.target_language
            )
            result["transformed_code"] = converted_code
            result["suggestions"] = notes
            
        elif request.operation == "explain":
            # Generate explanations for the code
            explanations = explainer.explain_code(
                request.code, request.source_language
            )
            result["explanations"] = explanations
            result["transformed_code"] = request.code  # No transformation, just explanation
            
        # Always add explanations for changes if code was modified
        if result["transformed_code"] != request.code:
            change_explanations = explainer.explain_changes(
                request.code, result["transformed_code"], request.source_language
            )
            result["explanations"].extend(change_explanations)
            
        return CodeResponse(**result)
        
    except Exception as e:
        return CodeResponse(
            original_code=request.code,
            transformed_code=request.code,
            explanations=[],
            suggestions=[],
            success=False,
            error_message=str(e)
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Syntax Shift API"}

@app.get("/api/languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    return {
        "supported_languages": ["python", "javascript", "cpp", "java"],
        "default_language": "python"
    }

if __name__ == "__main__":
    print("🚀 Starting Syntax Shift API Server...")
    print("📂 Frontend path:", frontend_path)
    print("🌐 Server will be available at: http://localhost:8000")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )