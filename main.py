import json
from core.model import BooleanNetworkModel
from analysis.engine import AnalysisEngine

def main():
    print("1. Lendo modelo direto do GINsim...")
    model = BooleanNetworkModel()
    # Lendo o arquivo compactado corretamente:
    model.load_from_ginsim("1.redesimplesdefinitiva.zginml.zip")
    nos_da_rede = model.get_nodes()
    print(f"-> Nós disponíveis na rede ({len(nos_da_rede)}):", nos_da_rede)

    print("\n2. Iniciando a Central de Análise...")
    engine = AnalysisEngine(model)

    print("\n3. Executando cálculo de Atratores...")
    # Opcional: Se quiser calcular os atratores dessa rede imensa, basta descomentar as duas linhas abaixo
    # report_attr = engine.compute_attractors(tools=["pyboolnet", "maboss"])
    # print("Atratores calculados!")

    print("\n4. Executando análise de Alcançabilidade (Reachability)...")
    
    # Estado Inicial: Fator de pluripotência ON, Fatores mesenquimais OFF
    estado_inicial = {"v___Oct4_Sox2": 1, "Zeb1": 0, "Snai1": 0}

    # Estado Final: Célula diferenciada/mesenquimal (Pluripotência OFF, Mesenquimais ON)
    estado_final = {"v___Oct4_Sox2": 0, "Zeb1": 1, "Snai1": 1}

    report_reach = engine.compute_reachability(
        source=estado_inicial, 
        target=estado_final, 
        tools=["pyboolnet", "maboss", "mpbn"]
    )

    print("\n=== PYBOOLNET (Reachability) ===")
    print(json.dumps(report_reach.get("pyboolnet", {}), indent=2))

    print("\n=== MABOSS (Reachability) ===")
    print(json.dumps(report_reach.get("maboss", {}), indent=2))

    print("\n=== MPBN (Reachability) ===")
    print(json.dumps(report_reach.get("mpbn", {}), indent=2))

if __name__ == "__main__":
    main()
