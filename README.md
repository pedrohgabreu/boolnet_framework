# Unified Boolean Network Framework

Uma arquitetura Python unificada para modelagem, simulação e análise de Redes Booleanas. 

Este framework foi projetado para automação e processamento de dados em biologia de sistemas complexos. Ele utiliza o **Adapter Pattern** para abstrair as diferenças de sintaxe e metodologias de execução entre diversas ferramentas conceituadas da área, permitindo análises comparativas reprodutíveis a partir de um único modelo base (*Source of Truth*).

## 🚀 Características Principais

* **Source of Truth Único:** A biologia e as regras lógicas são definidas uma única vez.
* **Padronização de Saídas:** Resultados de diferentes engines são devolvidos em um formato JSON/Dictionary unificado.
* **Múltiplos Backends:**
  * `PyBoolNet`: Cálculos lógicos e determinísticos/assíncronos (State Transition Graphs).
  * `MaBoSS`: Simulações estocásticas contínuas baseadas em cadeias de Markov.
  * *(Em breve: Pint, BoNesis, etc.)*

## 🏗️ Arquitetura

1. **Modelo Biológico Central (`core/model.py`)**: Valida e armazena as regras Booleanas.
2. **Camada de Adaptação (`adapters/`)**: Converte o modelo central para os formatos nativos (ex: `.bnd`, `.cfg`, `primes`) e executa as análises de forma transparente.
3. **Análise Unificada (`analysis/`)**: Scripts focados em processar respostas das diferentes engines e formatar os dados finais.

## 🛠️ Instalação (Ambiente Linux / WSL)

Devido às dependências de motores matemáticos escritos em C/C++ (como NuSMV e MaBoSS), recomenda-se o uso de ambiente Linux ou WSL.

```bash
# Clone o repositório
git clone [https://github.com/seu-usuario/boolnet_framework.git](https://github.com/seu-usuario/boolnet_framework.git)
cd boolnet_framework

# Crie e ative o ambiente virtual
python3 -m venv venv_linux
source venv_linux/bin/activate

# Instale as dependências Python
pip install -r requirements.txt
pip install maboss