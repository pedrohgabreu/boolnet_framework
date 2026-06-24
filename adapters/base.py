from abc import ABC, abstractmethod
from typing import Any, Dict
from core.model import BooleanNetworkModel

class BooleanBackendAdapter(ABC):
    """
    Classe base abstrata para todos os adaptadores de ferramentas booleanas.
    Define o contrato obrigatório que toda ferramenta deve implementar.
    """
    
    def __init__(self, model: BooleanNetworkModel):
        self.model = model

    @abstractmethod
    def export_model(self) -> Any:
        """
        Converte o BooleanNetworkModel para o formato/sintaxe nativo da ferramenta.
        Deve retornar o modelo pronto para uso na ferramenta específica.
        """
        pass

    @abstractmethod
    def compute_attractors(self, **kwargs) -> Dict[str, Any]:
        """
        Calcula os atratores do modelo.
        Deve retornar um dicionário padronizado no formato unificado do framework.
        """
        pass

    @abstractmethod
    def compute_reachability(self, source: Dict[str, int], target: Dict[str, int], **kwargs) -> Dict[str, Any]:
        """
        Calcula a alcançabilidade de um estado 'source' para um estado 'target'.
        """
        pass