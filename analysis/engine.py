from typing import List, Dict, Any
from core.model import BooleanNetworkModel

# Importação dos Adapters disponíveis
from adapters.pyboolnet_adapter import PyBoolNetAdapter
from adapters.maboss_adapter import MaBoSSAdapter
# from adapters.pint_adapter import PintAdapter
from adapters.mpbn_adapter import MPBNAdapter

# Dicionário que mapeia o nome da ferramenta para a sua respectiva classe Adapter
REGISTERED_BACKENDS = {
    "pyboolnet": PyBoolNetAdapter,
    "maboss": MaBoSSAdapter,
    "mpbn": MPBNAdapter
}
    

class AnalysisEngine:
    """
    Central de Comando unificada. 
    Abstrai a inicialização dos adapters e consolida os resultados.
    """
    def __init__(self, model: BooleanNetworkModel):
        self.model = model

    def compute_attractors(self, tools: List[str] = ["pyboolnet"], **kwargs) -> Dict[str, Any]:
        """
        Executa o cálculo de atratores em múltiplas ferramentas simultaneamente.
        """
        consolidated_results = {}

        for tool in tools:
            tool_key = tool.lower()
            
            if tool_key not in REGISTERED_BACKENDS:
                consolidated_results[tool_key] = {"status": "error", "message": f"Ferramenta '{tool}' não registrada."}
                continue
                
            try:
                # Instancia o adapter correto dinamicamente
                adapter_class = REGISTERED_BACKENDS[tool_key]
                adapter_instance = adapter_class(self.model)
                
                # Executa e salva o resultado
                result = adapter_instance.compute_attractors(**kwargs)
                consolidated_results[tool_key] = {"status": "success", "data": result}
                
            except Exception as e:
                consolidated_results[tool_key] = {"status": "error", "message": str(e)}

        return consolidated_results

    # O mesmo padrão se aplica para a alcançabilidade (Reachability)
    def compute_reachability(self, source: Dict[str, int], target: Dict[str, int], tools: List[str] = ["pyboolnet"], **kwargs) -> Dict[str, Any]:
            """
            Calcula se é possível alcançar um estado 'target' a partir de um estado 'source'.
            """
            consolidated_results = {}

            for tool in tools:
                tool_key = tool.lower()
                
                if tool_key not in REGISTERED_BACKENDS:
                    consolidated_results[tool_key] = {"status": "error", "message": f"Ferramenta '{tool}' não registrada."}
                    continue
                    
                try:
                    # Instancia o adapter correto
                    adapter_class = REGISTERED_BACKENDS[tool_key]
                    adapter_instance = adapter_class(self.model)
                    
                    # Executa a alcançabilidade passando o estado inicial e final
                    result = adapter_instance.compute_reachability(source=source, target=target, **kwargs)
                    consolidated_results[tool_key] = {"status": "success", "data": result}
                    
                except Exception as e:
                    consolidated_results[tool_key] = {"status": "error", "message": str(e)}

            return consolidated_results