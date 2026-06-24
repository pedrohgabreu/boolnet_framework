import logging
import traceback
from typing import Any, Dict
from core.model import BooleanNetworkModel
from adapters.base import BooleanBackendAdapter

try:
    from pyboolnet.file_exchange import bnet2primes
    from pyboolnet.attractors import compute_attractors
    from pyboolnet.model_checking import model_checking 
    
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
        raw_output = compute_attractors(primes=self.primes, update=update_mode)
        
        standardized_states = []
        for attr in raw_output.get("attractors", []):
            state_dict = attr['state']['dict']
            is_steady = attr.get('is_steady', False)
            
            standardized_states.append({
                "type": "steady" if is_steady else "cyclic",
                "state": state_dict
            })
        
        return {
            "tool": "pyboolnet",
            "type": "attractor",
            "update_mode": update_mode,
            "states": standardized_states
        }

    def compute_reachability(self, source: Dict[str, int], target: Dict[str, int], **kwargs) -> Dict[str, Any]:
        update_mode = kwargs.get("update_mode", "asynchronous")
        
        def dict_to_logic(state_dict):
            # Traduzindo 1 e 0 para TRUE e FALSE para o C++ do NuSMV não surtar
            clauses = []
            for k, v in state_dict.items():
                val_str = "TRUE" if v == 1 else "FALSE"
                clauses.append(f"{k}={val_str}")
            return " & ".join(clauses)

        source_logic = "INIT " + dict_to_logic(source)
        target_logic = dict_to_logic(target)

        # Garantindo a sintaxe formal completa exigida pelo NuSMV
        ctl_query = f"CTLSPEC EF ({target_logic})"
        
        try:
            is_reachable = model_checking(
                primes=self.primes, 
                update=update_mode, 
                initial_states=source_logic,
                specification=ctl_query
            )
            
            return {
                "tool": "pyboolnet",
                "type": "reachability",
                "reachable": is_reachable,
                "path": []
            }
        except Exception as e:
            return {
                "tool": "pyboolnet",
                "type": "reachability",
                "reachable": None,
                "error": traceback.format_exc()
            }