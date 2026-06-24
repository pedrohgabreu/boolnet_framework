import os
import tempfile
from typing import Any, Dict
from core.model import BooleanNetworkModel
from adapters.base import BooleanBackendAdapter

try:
    import pypint
except ImportError:
    raise ImportError("PyPint não encontrado. Instale com: pip install pypint")

class PintAdapter(BooleanBackendAdapter):
    def __init__(self, model: BooleanNetworkModel):
        super().__init__(model)
        self.pint_model = self.export_model()

    def export_model(self) -> Any:
        """
        Converte o Source of Truth para o formato BNET e carrega no Pint.
        """
        bnet_lines = []
        for node, logic in self.model.rules.items():
            bnet_lines.append(f"{node}, {logic}")
        
        bnet_str = "\n".join(bnet_lines)

        # O PyPint consome arquivos BNET (ou .an), então usamos o tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".bnet") as f:
            f.write(bnet_str)
            temp_path = f.name

        try:
            # Carrega o modelo na engine do Pint
            model_pint = pypint.load(temp_path)
        finally:
            os.remove(temp_path) # Limpa o disco imediatamente
            
        return model_pint

    def compute_attractors(self, **kwargs) -> Dict[str, Any]:
        """
        Calcula os atratores assíncronos usando a abstração do Pint.
        """
        # O Pint retorna uma lista de dicionários com os estados
        raw_attractors = self.pint_model.compute_attractors()
        
        standardized_states = []
        for attr in raw_attractors:
            standardized_states.append({
                "type": "steady",
                "state": attr
            })

        return {
            "tool": "pint",
            "type": "attractor",
            "update_mode": "asynchronous",
            "states": standardized_states
        }

    def compute_reachability(self, source: Dict[str, int], target: Dict[str, int], **kwargs) -> Dict[str, Any]:
        return {
            "tool": "pint",
            "type": "reachability",
            "reachable": None,
            "path": []
        }
