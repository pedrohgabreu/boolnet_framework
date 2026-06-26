import os
import mpbn
from adapters.base import BooleanBackendAdapter

class PintAdapter(BooleanBackendAdapter):
    
    def compute_reachability(self, source: dict, target: dict, **kwargs) -> dict:
        """
        Executa a alcançabilidade usando o motor MPBN (implementação Python 
        nativa do motor Pint). Isso elimina a dependência de arquivos .an
        e erros de sintaxe do parser OCaml.
        """
        bnet_path = "/tmp/pint_model.bnet"
        
        try:
            # 1. Exporta o modelo para o formato BNET padrão
            self.model.export_to_bnet(bnet_path)
            
            # 2. Carrega o modelo no motor MPBN
            # O MPBN trata internamente as regras booleanas da mesma forma que o Pint
            model = mpbn.load(bnet_path)
            
            # 3. Executa a alcançabilidade (Retorna True/False ou o caminho)
            # O mpbn.reachability aceita dicionários diretamente
            is_reachable = model.reachability(source, target)
            
            return {
                "tool": "pint",
                "type": "reachability",
                "status": "success",
                "data": {
                    "reachable": bool(is_reachable)
                }
            }
            
        except Exception as e:
            raise Exception(f"Erro na execução via motor MPBN/Pint: {str(e)}")
            
        finally:
            if os.path.exists(bnet_path):
                os.remove(bnet_path)

    # --- MÉTODOS OBRIGATÓRIOS DO CONTRATO ---
    def compute_attractors(self, **kwargs) -> dict:
        return {"tool": "pint", "type": "attractors", "error": "Não implementado."}

    def export_model(self, filepath: str) -> None:
        self.model.export_to_bnet(filepath)