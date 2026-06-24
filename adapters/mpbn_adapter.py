import os
import tempfile
import traceback
from typing import Any, Dict
from core.model import BooleanNetworkModel
from adapters.base import BooleanBackendAdapter

try:
    import mpbn
except ImportError:
    raise ImportError("MPBN não encontrado. Instale com: pip install mpbn")

class MPBNAdapter(BooleanBackendAdapter):
    def __init__(self, model: BooleanNetworkModel):
        super().__init__(model)
        self.mb = self.export_model()

    def export_model(self) -> Any:
        """
        Converte as regras matemáticas do nosso Core para o formato BNET,
        que é a linguagem nativa do MPBN.
        """
        bnet_lines = []
        for node, logic in self.model.rules.items():
            bnet_lines.append(f"{node}, {logic}")
        
        bnet_content = "\n".join(bnet_lines)
        
        # O MPBN carrega arquivos físicos muito bem. Criamos um arquivo fantasma
        # temporário para injetar o modelo nele com segurança.
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".bnet") as tmp:
            tmp.write(bnet_content)
            tmp_path = tmp.name

        try:
            mb = mpbn.load(tmp_path)
        finally:
            os.remove(tmp_path) # Apaga o arquivo fantasma após carregar

        return mb

    def compute_attractors(self, **kwargs) -> Dict[str, Any]:
        try:
            raw_attractors = list(self.mb.attractors())
            
            standardized_states = []
            for attr in raw_attractors:
                standardized_states.append({
                    "type": "steady" if len(attr) == len(self.model.get_nodes()) else "complex_trapspace",
                    "state": attr
                })

            return {
                "tool": "mpbn",
                "type": "attractor",
                "states": standardized_states
            }
        except Exception as e:
            return {
                "tool": "mpbn",
                "type": "attractor",
                "error": traceback.format_exc()
            }

    def compute_reachability(self, source: Dict[str, int], target: Dict[str, int], **kwargs) -> Dict[str, Any]:
        try:
            is_reachable = self.mb.reachability(source, target)
            
            return {
                "tool": "mpbn",
                "type": "reachability",
                "reachable": is_reachable,
                "path": [] 
            }
        except Exception as e:
            return {
                "tool": "mpbn",
                "type": "reachability",
                "reachable": None,
                "error": traceback.format_exc()
            }
