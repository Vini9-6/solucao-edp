# EDP Solver

Sistema completo para resolução de Equações Diferenciais Parciais (EDPs) de segunda ordem, incluindo problemas estacionários e temporais (Poisson, Calor, Onda, Helmholtz), com múltiplos métodos numéricos e interface gráfica intuitiva.

---

## Descrição Geral

O EDP Solver oferece uma interface gráfica (Tkinter) para entrada dos parâmetros, escolha dos métodos, visualização dos resultados, comparação gráfica e exportação de relatórios em PDF.

---

## Principais Funcionalidades

- **Suporte a Diversos Tipos de EDPs:**
  - Poisson, Calor, Onda e Helmholtz (1D, Dirichlet)
- **Entrada Simbólica Flexível:**
  - Coeficientes p(x), q(x), r(x), f(x) como expressões do SymPy (ex: `sin(pi*x)`, `x**2`)
  - Condições iniciais e de contorno também como expressões simbólicas
- **Interface Gráfica Completa:**
  - Campos para todos os parâmetros relevantes
  - Seleção do tipo de equação
  - Visualização simbólica da equação (renderização LaTeX)
  - Barra de progresso durante o processamento
  - Aba de ajuda com instruções, exemplos e dicas
- **Validação Robusta:**
  - Checagem de preenchimento, tipos, domínio, número de pontos e expressões válidas (usando sympy)
  - Mensagens de erro detalhadas para cada campo
- **Execução Automática de Todos os Métodos:**
  - Rayleigh-Ritz, Galerkin, Colocação, Momentos, Subdomínios, Mínimos Quadrados
  - Resultados e coeficientes exibidos lado a lado
- **Comparação Visual e Numérica:**
  - Gráfico com todas as soluções aproximadas e legenda lateral
  - Cálculo do erro RMS entre métodos
- **Exportação Profissional:**
  - Relatório completo e gráfico exportáveis em PDF

---

## Métodos Numéricos Implementados

- **Rayleigh-Ritz**
- **Galerkin**
- **Colocação**
- **Momentos**
- **Subdomínios/Resíduos**
- **Mínimos Quadrados**

Cada método é implementado em módulo próprio, recebendo os parâmetros da EDP e retornando:
- Vetor solução aproximada nos pontos do domínio
- Vetor de coeficientes das funções base

#### Detalhes Técnicos
- **Base de Funções:**
  - Funções senoidais (ex: `sin(nπx)`) que satisfazem as condições de contorno homogêneas
- **Montagem dos Sistemas:**
  - Sistemas lineares (Ax = b) via integração simbólica (sympy) e numérica (scipy/numpy)
- **Discretização:**
  - Domínio discretizado em N pontos igualmente espaçados
- **Condições de Contorno:**
  - Dirichlet padrão, facilmente extensível
- **Comparação:**
  - Erro RMS entre soluções para análise quantitativa

---

## Fluxo de Uso

1. Preencha os parâmetros da EDP na interface (coeficientes, domínio, condições de contorno, condições iniciais se necessário, número de pontos, etc.)
2. Selecione o tipo de equação (Poisson, Calor, Onda, Helmholtz)
3. Clique em "Resolver"
4. Visualize resultados, coeficientes, gráficos e comparações
5. Exporte o relatório em PDF se desejar

---

## Estrutura do Projeto

```
edp-solver/
├── src/
│   ├── app.py                # Interface principal e lógica de controle
│   ├── methods/              # Implementação dos métodos numéricos
│   │   ├── rayleigh_ritz.py
│   │   ├── galerkin.py
│   │   ├── colocacao.py
│   │   ├── momentos.py
│   │   ├── subdominios.py
│   │   └── minimos_quadrados.py
│   ├── time_solvers/         # Solvers para EDPs temporais (Calor, Onda)
│   │   ├── calor_1d.py
│   │   └── onda_1d.py
│   └── ui/
│       └── main_window.py    # (Estrutura para expansão da interface)
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação e instruções
```

---

## Instalação

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

2. Execute a aplicação:
   ```
   python src/app.py
   ```

---

## Funcionalidades Detalhadas

- **Entrada simbólica:** Aceita expressões do sympy para máxima flexibilidade
- **Comparação visual:** Gráfico com todas as soluções e legenda lateral
- **Relatório automático:** Inclui coeficientes, erros RMS e exportação para PDF
- **Validação robusta:** Impede erros comuns de entrada e orienta o usuário
- **Ajuda integrada:** Guia de uso, exemplos e dicas na própria interface
- **Extensível:** Estrutura modular para inclusão de novos métodos numéricos
- **Integração Numérica e Simbólica:** sympy para manipulação simbólica, scipy/numpy para cálculos numéricos
- **Interface Tkinter:** Totalmente baseada em Python, sem dependências externas de GUI
- **Performance:** Barra de progresso para feedback em problemas grandes
- **Exportação Profissional:** Relatórios em PDF com texto e gráficos integrados

---

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.