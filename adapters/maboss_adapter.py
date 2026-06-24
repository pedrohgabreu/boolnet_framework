import os
import tempfile
from typing import Any, Dict
from core.model import BooleanNetworkModel
from adapters.base import BooleanBackendAdapter

# Importação específica do MaBoSS
try:
    import maboss
except ImportError:
    raise ImportError("MaBoSS não encontrado. Instale com: pip install maboss")

class MaBoSSAdapter(BooleanBackendAdapter):
    def __init__(self, model: BooleanNetworkModel):
        super().__init__(model)
        self.maboss_model = self.export_model()

    def export_model(self) -> Any:
        """
        Converte o modelo unificado para os formatos BND e CFG do MaBoSS.
        """
        bnd_lines = []
        cfg_lines = [
            # Configurações padrão para simulação estocástica
            "time_tick = 0.1;",
            "max_time = 100;", 
            "sample_count = 10000;",
            "discrete_time = 0;",
            "use_physrandgen = 1;",
            "seed_pseudorandom = 0;"
        ]

        for node, logic in self.model.rules.items():
            # Sintaxe BND: Define os nós e a lógica com taxas de transição baseadas na lógica
            bnd_lines.append(f"Node {node} {{\n  logic = ({logic});\n  rate_up = @logic ? 1.0 : 0.0;\n  rate_down = @logic ? 0.0 : 1.0;\n}}")
            # Sintaxe CFG: Define estado inicial equiprovável (50% de chance de 0 ou 1)
            cfg_lines.append(f"[{node}].istate = 0.5 [0], 0.5 [1];")

        bnd_str = "\n".join(bnd_lines)
        cfg_str = "\n".join(cfg_lines)

        # O MaBoSS consome arquivos, então criamos arquivos temporários
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".bnd") as bnd_file:
            bnd_file.write(bnd_str)
            bnd_path = bnd_file.name
            
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".cfg") as cfg_file:
            cfg_file.write(cfg_str)
            cfg_path = cfg_file.name

        # Carrega o modelo na engine do MaBoSS via arquivos
        model_mb = maboss.load(bnd_path, cfg_path)
        
        # Limpa o disco (o modelo já está na memória)
        os.remove(bnd_path)
        os.remove(cfg_path)
        
        return model_mb

    def compute_attractors(self, **kwargs) -> Dict[str, Any]:
        """
        Roda a simulação de Markov e extrai os estados assintóticos finais.
        """
        # Executa a simulação estocástica
        sim_result = self.maboss_model.run()
        
        # Pega a linha de probabilidades no final do tempo de simulação
        last_states = sim_result.get_states_probtraj().iloc[-1]
        
        standardized_states = []
        
        for state_str, prob in last_states.items():
            if prob < 0.01: # Ignora ruídos (estados com menos de 1% de chance)
                continue
                
            # O MaBoSS retorna os nós ativos separados por ' -- ', ou '<nil>' se for tudo zero
            state_dict = {}
            active_nodes = state_str.split(' -- ') if state_str != '<nil>' else []
            
            for node in self.model.get_nodes():
                state_dict[node] = 1 if node in active_nodes else 0
                
            standardized_states.append({
                "type": "stochastic_steady",
                "state": state_dict,
                "probability": round(prob, 4) # Bônus do MaBoSS: traz a probabilidade do atrator
            })
            
        return {
            "tool": "maboss",
            "type": "attractor",
            "update_mode": "stochastic",
            "states": standardized_states
        }

    def compute_reachability(self, source: Dict[str, int], target: Dict[str, int], **kwargs) -> Dict[str, Any]:
        import traceback

        try:
            # O Pulo do Gato: Não copiamos a simulação. 
            # Criamos uma nova do zero usando a nossa própria função nativa do adapter!
            sim = self.export_model()

            # Configurando o Estado Inicial (100% de chance de estar na condição 'source')
            for node in list(sim.network.keys()):
                if node in source:
                    prob_1 = source[node]
                    prob_0 = 1 - prob_1
                    sim.network.set_istate(node, [prob_0, prob_1])

            # Executando a Cadeia de Markov contínua no tempo
            res = sim.run()

            # Extraindo a Trajetória de Probabilidades (Dataframe do Pandas)
            df = res.get_states_probtraj()

            # Mapeia quais nós deveriam estar ativos no estado alvo
            target_active_set = set([k for k, v in target.items() if v == 1])

            max_prob = 0.0
            # Varre as colunas do MaBoSS para achar a que tem exatamente os mesmos nós, independente da ordem
            for col_name in df.columns:
                col_nodes = set() if col_name == "<nil>" else set(col_name.split(" -- "))
                
                if col_nodes == target_active_set:
                    max_prob = float(df[col_name].max())
                    break

            # Consideramos alcançável se a probabilidade for maior que um ruído estatístico (ex: 0.1%)
            is_reachable = max_prob > 0.001

            return {
                "tool": "maboss",
                "type": "reachability",
                "reachable": is_reachable,
                "max_probability": round(max_prob, 4), 
                "path": []
            }

        except Exception as e:
            return {
                "tool": "maboss",
                "type": "reachability",
                "reachable": None,
                "error": traceback.format_exc()
            }