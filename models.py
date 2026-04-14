from sqlalchemy import Column, DateTime, Integer, String, func, Boolean, ForeignKey
from database import Base
from datetime import datetime

class Empresa(Base):
    __tablename__ = 'empresas'

    id = Column(Integer, autoincrement=True, primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    cnpj = Column(String(14), nullable=False, unique=True)
    telefone = Column(String(11), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now())
    updated_at = Column(DateTime(timezone=True), default= datetime.now(), onupdate=datetime.now())
    status = Column(Boolean, default=True, nullable=False)

class Historico(Base):
    __tablename__ = 'historicos'

    id = Column(Integer, autoincrement=True, primary_key=True)
    empresa_id = Column(Integer, ForeignKey('empresas.id'), nullable=False)
    descricao = Column(String(60), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())