import json
from core.model import BooleanNetworkModel
from analysis.engine import AnalysisEngine

def main():
    print("1. Instanciando o Modelo Central...")
    model = BooleanNetworkModel("Cell_Fate_Model")
    
    model.load_from_dict({
        "Sox2": "Oct4",
        "Oct4": "Sox2 & Nanog",
        "Nanog": "Sox2"
    })

    print("2. Iniciando a Central de Análise...")
    engine = AnalysisEngine(model)
    
    # ---------------------------------------------------------
    # TESTE 1: Atratores (como já estava funcionando)
    # ---------------------------------------------------------
    print("\n3. Executando cálculo de Atratores...")
    report_attractors = engine.compute_attractors(tools=["pyboolnet", "maboss"], update_mode="synchronous")
    
    for tool_name, result in report_attractors.items():
        if result["status"] == "success":
            print(f"[{tool_name.upper()}] Atratores encontrados com sucesso.")
        else:
            print(f"[{tool_name.upper()}] Falha: {result['message']}")

    # ---------------------------------------------------------
    # TESTE 2: Alcançabilidade (Reachability)
    # ---------------------------------------------------------
    print("\n4. Executando análise de Alcançabilidade (Reachability)...")
    
    estado_inicial = {"Sox2": 1, "Oct4": 0, "Nanog": 0}
    estado_final = {"Sox2": 1, "Oct4": 1, "Nanog": 1}
    
    report_reach = engine.compute_reachability(
        source=estado_inicial, 
        target=estado_final, 
        tools=["pyboolnet", "maboss"]
    )

    for tool_name, result in report_reach.items():
        print(f"\n=== {tool_name.upper()} (Reachability) ===")
        if result["status"] == "success":
            print(json.dumps(result["data"], indent=2))
        else:
            print(f"Falha: {result['message']}")

if __name__ == "__main__":
    main()