# EDP Solver

Sistema completo para resolução de Equações Diferenciais Parciais (EDPs) de segunda ordem, com múltiplos métodos numéricos e interface gráfica intuitiva.

---

## Descrição Geral

O EDP Solver permite ao usuário resolver EDPs unidimensionais de segunda ordem do tipo:

    p(x)u''(x) + q(x)u'(x) + r(x)u(x) = f(x),  a ≤ x ≤ b
    u(a) = valor_a,  u(b) = valor_b

O sistema oferece uma interface gráfica (Tkinter) para entrada dos parâmetros, escolha dos métodos, visualização dos resultados, comparação gráfica e exportação de relatórios.

---

## Funcionamento e Lógica do Sistema

### 1. Interface Gráfica
- **Entrada de Dados:**
  - Coeficientes p(x), q(x), r(x), f(x) como expressões simbólicas (ex: `sin(pi*x)`, `x**2`).
  - Domínio [a, b] e condições de contorno Dirichlet.
  - Número de pontos de discretização.
- **Validação:**
  - Checagem de preenchimento, tipos, domínio, número de pontos e expressões válidas (usando sympy).
  - Mensagens de erro detalhadas para cada campo.
- **Ajuda:**
  - Aba de ajuda com instruções, exemplos e dicas de uso.
- **Tema:**
  - Alternância entre tema claro e escuro.
- **Visualização simbólica:**
  - Exibe a equação simbólica montada a partir dos parâmetros inseridos (renderização LaTeX).
- **Barra de progresso:**
  - Indicador visual durante o processamento de problemas grandes.

### 2. Métodos Numéricos Implementados
- **Rayleigh-Ritz**
- **Galerkin**
- **Colocação**
- **Momentos**
- **Subdomínios/Resíduos**
- **Mínimos Quadrados**

Cada método é implementado em um módulo próprio, recebendo os parâmetros da EDP e retornando:
- Vetor solução aproximada nos pontos do domínio.
- Vetor de coeficientes das funções base.

#### Detalhes Técnicos dos Métodos
- **Base de Funções:**
  - Em geral, utiliza funções senoidais (ex: `sin(nπx)`) que satisfazem as condições de contorno homogêneas.
- **Montagem dos Sistemas:**
  - Os métodos constroem sistemas lineares (Ax = b) via integração simbólica (sympy) e numérica (scipy.integrate.quad).
  - O sistema é resolvido com `numpy.linalg.solve`.
- **Discretização:**
  - O domínio é discretizado em N pontos igualmente espaçados.
- **Condições de Contorno:**
  - Implementação padrão para Dirichlet, facilmente extensível para outros tipos.
- **Comparação:**
  - O erro RMS entre soluções é calculado para análise quantitativa.

### 3. Execução e Comparação
- O usuário preenche os campos e clica em "Resolver EDP".
- O sistema executa todos os métodos numéricos e armazena os resultados.
- Os coeficientes e soluções são exibidos em abas de resultados e relatório.
- O relatório compara as soluções dos métodos, exibindo o erro RMS entre pares de métodos.
- O gráfico mostra todas as soluções aproximadas, cada uma com cor e marcador distintos, e legenda na lateral (fora da área do gráfico).

### 4. Exportação
- O relatório e o gráfico podem ser exportados para PDF diretamente pela interface (usando a biblioteca `fpdf`).
- O gráfico é salvo como imagem temporária e embutido no PDF.

---

## Estrutura do Projeto

```
edp-solver/
├── src/
│   ├── app.py                # Ponto de entrada e interface principal
│   ├── methods/              # Implementação dos métodos numéricos
│   │   ├── rayleigh_ritz.py
│   │   ├── galerkin.py
│   │   ├── colocacao.py
│   │   ├── momentos.py
│   │   ├── subdominios.py
│   │   └── minimos_quadrados.py
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

## Fluxo de Uso

1. Preencha os parâmetros da EDP na interface.
2. Clique em "Resolver EDP".
3. Visualize resultados, coeficientes, gráficos e comparações.
4. Exporte o relatório em PDF se desejar.

---

## Funcionalidades Detalhadas

- **Entrada simbólica:** Aceita expressões do sympy para máxima flexibilidade.
- **Comparação visual:** Gráfico com todas as soluções e legenda lateral.
- **Relatório automático:** Inclui coeficientes, erros RMS e exportação para PDF.
- **Validação robusta:** Impede erros comuns de entrada e orienta o usuário.
- **Ajuda integrada:** Guia de uso, exemplos e dicas na própria interface.
- **Extensível:** Estrutura modular para inclusão de novos métodos numéricos.
- **Integração Numérica e Simbólica:** Utiliza sympy para manipulação simbólica e scipy/numpy para cálculos numéricos.
- **Interface Tkinter:** Totalmente baseada em Python, sem dependências externas de GUI.
- **Performance:** Barra de progresso para feedback em problemas grandes.
- **Exportação Profissional:** Relatórios em PDF com texto e gráficos integrados.

---

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.