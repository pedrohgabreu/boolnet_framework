# BoolNet Framework

Um framework unificado em Python para modelagem e análise de Redes Booleanas, focado em Biologia de Sistemas. Ele atua como uma interface de alto nível que conecta modelos criados visualmente no GINsim a motores de cálculo avançados, abstraindo a complexidade algorítmica e de infraestrutura.

## Funcionalidades Principais

* **Leitura Nativa do GINsim:** Extração direta de regras matemáticas e topologia a partir de arquivos `.zginml` (ou `.zip`), sem necessidade de exportações manuais ou bibliotecas Java.
* **Sanitização Automática:** Tratamento e padronização de nomes de variáveis biológicas para garantir compatibilidade estrita com motores compilados em C/C++.
* **Arquitetura Desacoplada:** Execução simultânea de múltiplos backends matemáticos através de uma única interface de comando (`AnalysisEngine`).

## Backends Integrados

O framework consolida três das ferramentas mais robustas da literatura científica:

1. **PyBoolNet (NuSMV):** Análise lógica assíncrona formal e checagem de modelos para cálculo exato de atratores e alcançabilidade.
2. **MaBoSS:** Simulação estocástica baseada em tempo usando Cadeias de Markov, retornando a probabilidade estatística de transições celulares.
3. **MPBN (Most Permissive Boolean Networks):** Análise de alcançabilidade matemática projetada para contornar a explosão do espaço de estados em redes massivas.

## Instalação e Dependências

O projeto requer Python 3 e as seguintes bibliotecas biológicas:

```bash
pip install pyboolnet maboss mpbn