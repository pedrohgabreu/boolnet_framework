import json
from typing import Dict, List

class BooleanNetworkModel:
    def __init__(self, name: str = "Default_Model"):
        self.name = name
        self._rules: Dict[str, str] = {}

    @property
    def rules(self) -> Dict[str, str]:
        """Retorna as regras atuais do modelo."""
        return self._rules

    def add_rule(self, node: str, logic: str) -> None:
        """Adiciona ou atualiza a regra de um nó específico."""
        if not isinstance(node, str) or not isinstance(logic, str):
            raise ValueError("O nó e a lógica devem ser strings.")
        self._rules[node] = logic.strip()

    def load_from_dict(self, model_dict: Dict[str, str]) -> None:
        """Carrega regras diretamente de um dicionário."""
        for node, logic in model_dict.items():
            self.add_rule(node, logic)

    def load_from_json(self, filepath: str) -> None:
        """Carrega o modelo a partir de um arquivo JSON padrão."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.name = data.get("name", self.name)
            self.load_from_dict(data.get("rules", {}))

    def save_to_json(self, filepath: str) -> None:
        """Salva o modelo atual em um arquivo JSON."""
        data = {
            "name": self.name,
            "rules": self._rules
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def get_nodes(self) -> List[str]:
        """Retorna a lista de todos os nós presentes no modelo."""
        return list(self._rules.keys())

    def __repr__(self) -> str:
        return f"<BooleanNetworkModel '{self.name}' with {len(self._rules)} nodes>"