# EDP Solver

Este projeto é um sistema completo para resolver Equações Diferenciais Parciais (EDPs) utilizando diversos métodos numéricos. A aplicação possui uma interface gráfica desenvolvida em Tkinter, permitindo que os usuários interajam facilmente com o sistema.

## Estrutura do Projeto

O projeto é organizado da seguinte forma:

```
edp-solver
├── src
│   ├── app.py                     # Ponto de entrada da aplicação
│   ├── methods
│   │   ├── __init__.py            # Inicializa o pacote de métodos
│   │   ├── rayleigh_ritz.py       # Implementação do método Rayleigh-Ritz
│   │   ├── galerkin.py            # Implementação do método Galerkin
│   │   ├── colocacao.py           # Implementação do método da Colocação
│   │   ├── momentos.py             # Implementação do Método dos Momentos
│   │   ├── subdominios.py         # Implementação do método de Subdomínios/Resíduos
│   │   └── minimos_quadrados.py   # Implementação do método de Mínimos Quadrados
│   └── ui
│       ├── __init__.py            # Inicializa o pacote da interface do usuário
│       └── main_window.py         # Implementação da janela principal da interface gráfica
├── requirements.txt                # Dependências do projeto
└── README.md                       # Documentação do projeto
```

## Instalação

Para instalar as dependências do projeto, execute o seguinte comando:

```
pip install -r requirements.txt
```

## Uso

1. Execute o arquivo `app.py` para iniciar a aplicação.
2. Na interface gráfica, insira os parâmetros da EDP que deseja resolver.
3. Selecione os métodos numéricos que deseja utilizar.
4. Clique no botão "Resolver EDP" para obter os resultados.
5. Os resultados e gráficos serão exibidos na interface.

## Funcionalidades

- Suporte a múltiplos métodos de resolução de EDPs:
  - Rayleigh-Ritz
  - Método dos Momentos
  - Método da Colocação
  - Subdomínios/Resíduos
  - Mínimos Quadrados
  - Galerkin
- Interface gráfica intuitiva para facilitar a interação do usuário.
- Exibição de resultados e gráficos diretamente na aplicação.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias e correções.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.