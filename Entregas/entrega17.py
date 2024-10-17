from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
from pybloom_live import BloomFilter  # Importando Bloom Filter
from countminsketch import CountMinSketch  # Importando Count-Min Sketch

app = FastAPI()

# Conectar ao MongoDB
MONGO_DETAILS = "mongodb+srv://matheuseddc:2kHij4tU4vdDmd@cluster0.9t5qs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.Clinica_Server  # Nome da database

# Coleções
paciente_collection = database.get_collection("pacientes")
agendamentos_collection = database.get_collection("agendamentos")
medico_collection = database.get_collection("medicos")

# Modelo Paciente
class Paciente(BaseModel):
    cpf: str
    nome: str
    dataNasc: str
    email: str
    telefone: str

# Modelo Agendamento
class Agendamento(BaseModel):
    cpfPaciente: str
    nome: str
    sexo: str
    data: datetime
    email: str
    telefone: str
    crmMedico: str
    especialidade: str

# Modelo Médico
class Medico(BaseModel):
    crm: str
    nome: str
    dataNasc: str
    email: str
    cpf: str
    telefone: str
    especialidade: str

# Bloom Filter para CPFs de pacientes
cpf_bloom_filter = BloomFilter(capacity=100000, error_rate=0.001)

consulta_count_sketch = CountMinSketch(m=1000, d=10)

# Verificar se CPF já está no Bloom Filter
async def cpf_existe(cpf: str) -> bool:
    return cpf in cpf_bloom_filter

# Adicionar CPF ao Bloom Filter
async def adicionar_cpf_bloom_filter(cpf: str):
    cpf_bloom_filter.add(cpf)

# Incrementar contagem de consultas para um médico no Count-Min Sketch
async def incrementar_contagem_medico(crmMedico: str):
    consulta_count_sketch.add(crmMedico)

# Obter contagem aproximada de consultas para um médico
async def contar_consultas_medico(crmMedico: str) -> int:
    return consulta_count_sketch[crmMedico]

# Auxiliar para converter documentos
def paciente_helper(paciente) -> dict:
    return {
        "id": str(paciente["_id"]),
        "cpf": paciente["cpf"],
        "nome": paciente["nome"],
        "dataNasc": paciente["dataNasc"],
        "email": paciente["email"],
        "telefone": paciente["telefone"]
    }

def agendamento_helper(agendamento) -> dict:
    return {
        "id": str(agendamento["_id"]),
        "cpfPaciente": agendamento["cpfPaciente"],
        "nome": agendamento["nome"],  # Adicionado
        "sexo": agendamento["sexo"],  # Adicionado
        "data": agendamento["data"],
        "email": agendamento["email"],  # Adicionado
        "telefone": agendamento["telefone"],  # Adicionado
        "crmMedico": agendamento["crmMedico"],
        "especialidade": agendamento["especialidade"]
    }


def medico_helper(medico) -> dict:
    return {
        "id": str(medico["_id"]),
        "crm": medico["crm"],
        "nome": medico["nome"],
        "dataNasc": medico["dataNasc"],
        "email": medico["email"],
        "cpf": medico["cpf"],
        "telefone": medico["telefone"],
        "especialidade": medico["especialidade"]
    }

# Create - Criar um paciente
@app.post("/pacientes")
async def create_paciente(paciente: Paciente):
    # Verificar se o CPF já está no Bloom Filter
    if await cpf_existe(paciente.cpf):
        raise HTTPException(status_code=400, detail="Paciente já existe (CPF verificado via Bloom Filter)")
    
    paciente = paciente.dict()
    result = await paciente_collection.insert_one(paciente)
    await adicionar_cpf_bloom_filter(paciente["cpf"])  # Adicionar CPF ao Bloom Filter após inserção
    new_paciente = await paciente_collection.find_one({"_id": result.inserted_id})
    return new_paciente

# Read - Ler todos os pacientes
@app.get("/pacientes", response_model=List[Paciente])
async def get_pacientes():
    pacientes = []
    async for paciente in paciente_collection.find():
        pacientes.append(paciente_helper(paciente))
    return pacientes

# Read - Ler paciente específico por CPF
@app.get("/pacientes/{cpf}", response_model=Paciente)
async def read_paciente(cpf: str):
    paciente = await paciente_collection.find_one({"cpf": cpf})
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente_helper(paciente)

# Update - Atualizar um paciente
@app.put("/pacientes/{cpf}", response_model=Paciente)
async def update_paciente(cpf: str, paciente: Paciente):
    existing_paciente = await paciente_collection.find_one({"cpf": cpf})
    if not existing_paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    await paciente_collection.update_one({"cpf": cpf}, {"$set": paciente.dict()})
    updated_paciente = await paciente_collection.find_one({"cpf": cpf})
    return paciente_helper(updated_paciente)

# Delete - Deletar um paciente
@app.delete("/pacientes/{cpf}")
async def delete_paciente(cpf: str):
    paciente = await paciente_collection.find_one({"cpf": cpf})
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    await paciente_collection.delete_one({"cpf": cpf})
    return {"success": True, "message": "Paciente deletado com sucesso"}

# Create - Criar um agendamento
@app.post("/agendar")
async def create_agendamento(agendamento: Agendamento):
    # Verifica se já existe um agendamento com o mesmo CPF
    existing_agendamento = await agendamentos_collection.find_one({"cpfPaciente": agendamento.cpfPaciente})
    if existing_agendamento:
        raise HTTPException(status_code=400, detail="Agendamento já existe para este CPF")
    
    agendamento_dict = agendamento.dict()
    result = await agendamentos_collection.insert_one(agendamento_dict)
    
    # Incrementar contagem de consultas para o médico
    await incrementar_contagem_medico(agendamento.crmMedico)

    new_agendamento = await agendamentos_collection.find_one({"_id": result.inserted_id})
    return new_agendamento


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
    
    # Atualiza o agendamento com os novos dados
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

# Create - Criar um médico
@app.post("/medicos")
async def create_medico(medico: Medico):
    medico = medico.dict()
    result = await medico_collection.insert_one(medico)
    new_medico = await medico_collection.find_one({"_id": result.inserted_id})
    return medico_helper(new_medico)

# Read - Ler todos os médicos
@app.get("/medicos", response_model=List[Medico])
async def get_medicos():
    medicos = []
    async for medico in medico_collection.find():
        medicos.append(medico_helper(medico))
    return medicos

# Read - Ler médico específico por CRM
@app.get("/medicos/{crm}", response_model=Medico)
async def read_medico(crm: str):
    medico = await medico_collection.find_one({"crm": crm})
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return medico_helper(medico)

# Update - Atualizar um médico
@app.put("/medicos/{crm}", response_model=Medico)
async def update_medico(crm: str, medico: Medico):
    existing_medico = await medico_collection.find_one({"crm": crm})
    if not existing_medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    await medico_collection.update_one({"crm": crm}, {"$set": medico.dict()})
    updated_medico = await medico_collection.find_one({"crm": crm})
    return medico_helper(updated_medico)

# Delete - Deletar um médico
@app.delete("/medicos/{crm}")
async def delete_medico(crm: str):
    medico = await medico_collection.find_one({"crm": crm})
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    await medico_collection.delete_one({"crm": crm})
    return {"success": True, "message": "Médico deletado com sucesso"}

# AGREGATION PIPELINE

async def listar_consultas_por_medico(crmMedico: str):
    pipeline = [
        {
            "$match": {
                "crmMedico": crmMedico
            }
        },
        {
            "$lookup": {
                "from": "pacientes",  # Coleção de pacientes
                "localField": "cpfPaciente",  # CPF do paciente na coleção de agendamentos
                "foreignField": "cpf",  # CPF do paciente na coleção de pacientes
                "as": "paciente_info"
            }
        },
        {
            "$unwind": "$paciente_info"  # Descompactar a lista de informações do paciente
        },
        {
            "$project": {
                "_id": 0,  # Não mostrar o _id no resultado
                "nomePaciente": "$paciente_info.nome",  # Nome do paciente da coleção pacientes
                "data": 1  # Data da consulta
            }
        },
        {
            "$sort": {
                "data": 1  # Ordenar pela data (1 para ordem crescente)
            }
        }
    ]

    consultas = await agendamentos_collection.aggregate(pipeline).to_list(length=None)
    return consultas

# Endpoint para obter contagem de consultas de um médico
@app.get("/consultas/contagem/{crmMedico}")
async def get_contagem_consultas(crmMedico: str):
    contagem = await contar_consultas_medico(crmMedico)
    return {"crmMedico": crmMedico, "contagem_aproximada": contagem}
