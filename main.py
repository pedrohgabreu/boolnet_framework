import json
from core.model import BooleanNetworkModel
from adapters.pyboolnet_adapter import PyBoolNetAdapter
from adapters.maboss_adapter import MaBoSSAdapter

def print_results(results):
    print(f"\n--- Resultados via {results['tool'].upper()} ---")
    print(json.dumps(results['states'], indent=2))

def main():
    print("1. Instanciando o Modelo Central...")
    model = BooleanNetworkModel(name="Cell_Fate_Model")
    
    # O Source of Truth
    model.load_from_dict({
        "Sox2": "Oct4",
        "Oct4": "Sox2 & Nanog",
        "Nanog": "Sox2"
    })

    print("2. Conectando aos Backends...")
    pyboolnet_engine = PyBoolNetAdapter(model)
    maboss_engine = MaBoSSAdapter(model) # Adicionado!
    
    print("3. Executando cálculos de Atratores lado a lado...")
    
    try:
        results_pyboolnet = pyboolnet_engine.compute_attractors(update_mode="synchronous")
        print_results(results_pyboolnet)
    except Exception as e:
        print(f"Erro no PyBoolNet: {e}")

    try:
        results_maboss = maboss_engine.compute_attractors()
        print_results(results_maboss)
    except Exception as e:
        print(f"Erro no MaBoSS: {e}")

if __name__ == "__main__":
    main()