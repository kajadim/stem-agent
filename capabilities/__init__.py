from pydantic import BaseModel
from typing import Optional
from enum import Enum

class PermissionLevel(Enum):
    READ_ONLY = "read_only"
    READ_WRITE = "read_write"
    EXECUTE = "execute"
    NETWORK = "network"

class ToolMetadata(BaseModel):
    name: str
    description: str
    cost_estimate: float  
    required_permissions: list[PermissionLevel]
    suitable_for: list[str]  

class BaseTool(BaseModel):
    metadata: ToolMetadata
    
    def execute(self, **kwargs) -> dict:
        raise NotImplementedError("Must implement execute()")
    
    def validate_input(self, **kwargs) -> bool:
        raise NotImplementedError("Must implement validate_input()")