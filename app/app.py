from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from app.controlador.PatientCrud import GetPatientById, WritePatient  # Asegúrate de que este import sea correcto

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hl7-patient-write-omar-9855.onrender.com"],  # Permitir solo este dominio
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/patient/{patient_id}")
async def get_patient_by_id(patient_id: str):
    """Obtiene un paciente por ID."""
    status, patient = GetPatientById(patient_id)  # Se eliminó el ":" incorrecto
    if status == 'success':
        return patient
    elif status == 'notFound':
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error: {status}")

@app.get("/patient")
async def get_patient_by_system_value(system: str, value: str):
    """Obtiene un paciente por sistema y valor."""
    status, patient = GetPatientById(system, value)
    if status == 'success':
        return patient
    elif status == 'notFound':
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error: {status}")

@app.post("/patient")
async def add_patient(request: Request):
    """Agrega un nuevo paciente."""
    new_patient_dict = await request.json()
    status, patient_id = WritePatient(new_patient_dict)
    if status == 'success':
        return {"_id": patient_id}
    else:
        raise HTTPException(status_code=500, detail=f"Validating error: {status}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
