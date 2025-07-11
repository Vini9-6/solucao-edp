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

## Resumo das Alterações e Funcionalidades

**Introdução:**  
O EDP Solver foi aprimorado para oferecer uma solução educacional completa para EDPs de segunda ordem, permitindo a resolução de problemas estacionários e temporais (Poisson, Calor, Onda, Helmholtz) com múltiplos métodos numéricos e interface gráfica intuitiva.

**Métodos Implementados:**  
O sistema executa automaticamente os métodos Rayleigh-Ritz, Galerkin, Colocação, Momentos, Subdomínios e Mínimos Quadrados, exibindo os resultados lado a lado e permitindo comparação quantitativa (erro RMS) e visual (gráficos).

**Tecnologias Utilizadas:**  
- Python 3.x  
- Tkinter (interface gráfica)  
- SymPy (manipulação simbólica)  
- NumPy (cálculo numérico)  
- Matplotlib (gráficos)  
- FPDF (exportação PDF)

**Resultados e Discussões:**  
O programa valida todas as entradas, executa todos os métodos para cada problema, exibe coeficientes e soluções aproximadas, calcula o erro RMS entre métodos e permite exportar relatórios completos em PDF. Para EDPs temporais, a solução estacionária é somada à dinâmica ao final de cada passo, garantindo resultados fisicamente corretos. O sistema facilita o aprendizado e a comparação entre métodos clássicos de resolução de EDPs.

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

---

# Relatório de Atualizações e Desenvolvimento

## Introdução

O EDP Solver foi desenvolvido com o propósito de fornecer uma ferramenta educacional robusta para a resolução de Equações Diferenciais Parciais (EDPs) de segunda ordem. O sistema foi expandido para abranger problemas estacionários e temporais, com múltiplos métodos numéricos e uma interface gráfica intuitiva, visando facilitar o aprendizado, a comparação e a análise dos métodos clássicos de solução de EDPs.

## Objetivos

- Permitir a resolução automática de EDPs de segunda ordem (Poisson, Calor, Onda, Helmholtz) em 1D com condições de contorno Dirichlet.
- Implementar e comparar diversos métodos numéricos clássicos, exibindo resultados lado a lado.
- Proporcionar uma interface gráfica amigável, com validação robusta das entradas e visualização dos resultados.
- Oferecer exportação profissional dos resultados e relatórios em PDF.
- Facilitar a extensão do sistema para novos métodos e tipos de equações.

## Metodologia

- **Estrutura Modular:** O projeto foi organizado em módulos separados para cada método numérico, facilitando manutenção e expansão.
- **Interface Gráfica (Tkinter):** Desenvolvida para entrada dos parâmetros, seleção do tipo de equação, visualização simbólica e comparação dos resultados.
- **Entrada Simbólica:** Utilização do SymPy para permitir expressões simbólicas nos coeficientes e condições, aumentando a flexibilidade.
- **Validação:** Implementação de checagem automática dos campos, tipos, domínio e expressões, com mensagens de erro detalhadas.
- **Execução Automática:** Todos os métodos são executados em sequência, com resultados exibidos simultaneamente para comparação.
- **Visualização:** Gráficos gerados via Matplotlib, com legenda lateral e cálculo do erro RMS entre métodos.
- **Exportação:** Relatórios completos gerados em PDF, incluindo gráficos, coeficientes e análise de erros.

## Resultados

- O sistema executa com sucesso todos os métodos implementados (Rayleigh-Ritz, Galerkin, Colocação, Momentos, Subdomínios, Mínimos Quadrados), exibindo as soluções aproximadas e coeficientes de cada método.
- A interface gráfica permite fácil entrada dos parâmetros, visualização simbólica da equação e acompanhamento do progresso.
- A validação robusta evita erros comuns de entrada, orientando o usuário com mensagens claras.
- A exportação em PDF inclui todos os dados relevantes, gráficos e análise quantitativa dos métodos.
- Para EDPs temporais, a solução estacionária é corretamente somada à dinâmica, garantindo resultados fisicamente consistentes.

## Discussões e Desafios Encontrados

- **Validação Simbólica:** Garantir que todas as expressões simbólicas inseridas pelo usuário fossem válidas e compatíveis com o domínio exigiu integração cuidadosa entre SymPy e a interface.
- **Montagem dos Sistemas:** A implementação dos métodos exigiu atenção à montagem dos sistemas lineares, especialmente na integração simbólica e numérica dos termos.
- **Interface Gráfica:** Adaptar a interface para suportar múltiplos métodos, visualização simultânea dos resultados e renderização LaTeX das equações foi um desafio de usabilidade.
- **Performance:** Para problemas com muitos pontos, foi necessário implementar barra de progresso e otimizar cálculos para evitar travamentos.
- **Exportação PDF:** Integrar gráficos e textos de forma profissional no relatório PDF demandou ajustes na formatação e compatibilidade entre Matplotlib e FPDF.
- **Extensibilidade:** A estrutura modular foi pensada para facilitar futuras expansões, mas exigiu padronização das interfaces entre módulos e métodos.

O desenvolvimento do EDP Solver proporcionou avanços significativos na usabilidade, robustez e capacidade de comparação entre métodos numéricos, tornando-o uma ferramenta valiosa para ensino e pesquisa em EDPs.