import zipfile
import xml.etree.ElementTree as ET
import re  # Biblioteca de expressões regulares para limpar textos
from typing import Dict

class BooleanNetworkModel:
    def __init__(self, name: str = "Unnamed_Model"):
        self.name = name
        self.rules: Dict[str, str] = {}

    def load_from_dict(self, rules_dict: Dict[str, str]):
        self.rules = rules_dict

    def load_from_ginsim(self, filepath: str):
        """
        Lê nativamente um arquivo .zginml, .zip ou .ginml e higieniza
        os nomes das variáveis para evitar quebras nos motores C/C++.
        """
        # --- O SANITIZADOR DE VARIÁVEIS ---
        def sanitize(name: str) -> str:
            if not name: return "unknown"
            # 1. Troca qualquer caractere estranho (hífen, espaço, etc) por underline '_'
            clean = re.sub(r'[^a-zA-Z0-9]', '_', name)
            # 2. Motores C odeiam variáveis começando com número ou '_'. Prependemos 'v_'
            if clean[0].isdigit() or clean[0] == '_':
                clean = "v_" + clean
            # 3. NuSMV odeia variáveis de 1 letra. Se for "O", vira "O_node"
            if len(clean) == 1:
                clean = clean + "_node"
            return clean

        # 1. Abertura do Arquivo
        if filepath.endswith(".zginml") or filepath.endswith(".zip"):
            with zipfile.ZipFile(filepath, 'r') as z:
                ginml_filename = [name for name in z.namelist() if name.endswith('.ginml')][0]
                with z.open(ginml_filename) as f:
                    tree = ET.parse(f)
        else:
            tree = ET.parse(filepath)

        root = tree.getroot()

        # 2. Mapeamento e Higienização das Arestas
        edges = {}
        for elem in root.iter():
            if elem.tag.endswith('edge'):
                edge_id = elem.attrib.get('id')
                source = sanitize(elem.attrib.get('from'))
                target = sanitize(elem.attrib.get('to'))
                edges[edge_id] = {'source': source, 'target': target}

        # 3. Extração da Lógica Matemática
        extracted_rules = {}
        for elem in root.iter():
            if elem.tag.endswith('node'):
                node_id = sanitize(elem.attrib.get('id'))
                
                incoming = {e_id: e for e_id, e in edges.items() if e['target'] == node_id}
                
                params_or = []
                for param in elem.iter():
                    if param.tag.endswith('parameter'):
                        if param.attrib.get('val') == '1':
                            active_ids = param.attrib.get('idActiveInteractions', '').split()
                            
                            if not incoming:
                                params_or.append("1")
                                continue
                                
                            term_and = []
                            for inc_id, inc_data in incoming.items():
                                src = inc_data['source']
                                if inc_id in active_ids:
                                    term_and.append(src)
                                else:
                                    term_and.append(f"!{src}")
                            
                            params_or.append("(" + " & ".join(term_and) + ")")
                
                extracted_rules[node_id] = " | ".join(params_or) if params_or else "0"

        self.rules = extracted_rules
        self.name = filepath.split('/')[-1]

    def get_nodes(self):
        """Retorna a lista de todos os nós (genes/proteínas) presentes na rede."""
        return list(self.rules.keys())