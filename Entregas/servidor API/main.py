from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

# Conectar ao MongoDB
MONGO_DETAILS = "mongodb+srv://matheuseddc:2kHij4tU4vdDmd@cluster0.9t5qs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.agendamento_db  # Nome do banco de dados
agendamentos_collection = database.get_collection("agendamentos")  # Coleção para armazenar os agendamentos

# Função auxiliar para converter um documento do MongoDB para um formato JSON-friendly
def agendamento_helper(agendamento) -> dict:
    return {
        "id": str(agendamento["_id"]),
        "cpfPaciente": agendamento["cpfPaciente"],
        "data": agendamento["data"],
        "sintomas": agendamento["sintomas"],
        "crmMedico": agendamento["crmMedico"],
        "especialidade": agendamento["especialidade"]
    }

# Modelo de Agendamento
class Agendamento(BaseModel):
    cpfPaciente: str
    data: str
    sintomas: str
    crmMedico: str
    especialidade: str

# Create - Criar um agendamento
@app.post("/agendar")
async def create_agendamento(agendamento: Agendamento):
    # Verifica se já existe um agendamento com o mesmo CPF
    existing_agendamento = await agendamentos_collection.find_one({"cpfPaciente": agendamento.cpfPaciente})
    if existing_agendamento:
        raise HTTPException(status_code=400, detail="Agendamento já existe para este CPF")
    
    agendamento = agendamento.dict()
    result = await agendamentos_collection.insert_one(agendamento)
    new_agendamento = await agendamentos_collection.find_one({"_id": result.inserted_id})
    return agendamento_helper(new_agendamento)

# Read - Ler todos os agendamentos
@app.get("/agendamentos/", response_model=List[Agendamento])
async def get_agendamentos():
    agendamentos = []
    async for agendamento in agendamentos_collection.find():
        agendamentos.append(agendamento_helper(agendamento))
    return agendamentos

# Read - Ler agendamento específico por CPF
@app.get("/agendamentos/{cpfPaciente}", response_model=Agendamento)
async def read_agendamento(cpfPaciente: str):
    agendamento = await agendamentos_collection.find_one({"cpfPaciente": cpfPaciente})
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    return agendamento_helper(agendamento)

# Update - Atualizar um agendamento existente
@app.put("/agendamentos/{cpfPaciente}", response_model=Agendamento)
async def update_agendamento(cpfPaciente: str, agendamento: Agendamento):
    existing_agendamento = await agendamentos_collection.find_one({"cpfPaciente": cpfPaciente})
    if not existing_agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    await agendamentos_collection.update_one({"cpfPaciente": cpfPaciente}, {"$set": agendamento.dict()})
    updated_agendamento = await agendamentos_collection.find_one({"cpfPaciente": cpfPaciente})
    return agendamento_helper(updated_agendamento)

# Delete - Deletar um agendamento
@app.delete("/agendamentos/{cpfPaciente}")
async def delete_agendamento(cpfPaciente: str):
    agendamento = await agendamentos_collection.find_one({"cpfPaciente": cpfPaciente})
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    await agendamentos_collection.delete_one({"cpfPaciente": cpfPaciente})
    return {"success": True, "message": "Agendamento deletado com sucesso"}
