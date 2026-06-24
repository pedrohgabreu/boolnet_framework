import logging
from typing import Any, Dict
from core.model import BooleanNetworkModel
from adapters.base import BooleanBackendAdapter

# Importações simplificadas do PyBoolNet v3+
try:
    from pyboolnet.file_exchange import bnet2primes
    from pyboolnet.attractors import compute_attractors
    
    # Silencia os logs verbosos do PyBoolNet
    logging.getLogger("pyboolnet").setLevel(logging.WARNING)
except ImportError:
    raise ImportError("PyBoolNet não encontrado. Instale com: pip install pyboolnet")

class PyBoolNetAdapter(BooleanBackendAdapter):
    def __init__(self, model: BooleanNetworkModel):
        super().__init__(model)
        self.primes = self.export_model()

    def export_model(self) -> Any:
        bnet_lines = []
        for node, logic in self.model.rules.items():
            bnet_lines.append(f"{node}, {logic}")
        bnet_str = "\n".join(bnet_lines)
        return bnet2primes(bnet_str)

    def compute_attractors(self, update_mode: str = "asynchronous", **kwargs) -> Dict[str, Any]:
        # 1. Calcula os atratores brutos
        raw_output = compute_attractors(primes=self.primes, update=update_mode)
        
        # 2. Padroniza a saída (O grande truque do Adapter)
        standardized_states = []
        
        for attr in raw_output.get("attractors", []):
            # O PyBoolNet guarda o estado limpo dentro de ['state']['dict']
            state_dict = attr['state']['dict']
            is_steady = attr.get('is_steady', False)
            
            standardized_states.append({
                "type": "steady" if is_steady else "cyclic",
                "state": state_dict
            })
        
        # 3. Retorna o objeto unificado e limpo
        return {
            "tool": "pyboolnet",
            "type": "attractor",
            "update_mode": update_mode,
            "states": standardized_states
        }

    def compute_reachability(self, source: Dict[str, int], target: Dict[str, int], **kwargs) -> Dict[str, Any]:
        return {
            "tool": "pyboolnet",
            "type": "reachability",
            "reachable": None,
            "path": []
        }