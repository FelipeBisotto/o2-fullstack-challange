# TESTES BACKEND - SISTEMA DE GESTÃO DE ESTOQUE

## Objetivo

Este documento descreve os testes automatizados implementados para o backend do sistema de gestão de estoque, utilizando **Pytest** e **FastAPI TestClient**. 
O foco está na validação das **Regras de Negócio (RN)** e dos **Requisitos Funcionais (RF)**, garantindo que todas as operações do sistema estejam funcionando corretamente e de forma consistente.

Os testes estão organizados por módulo: **Produtos**, **Movimentações**, **Dashboard** e **Relatórios**.

---

## Produtos

### Testes com FastAPI:

- `test_criar_produto_sucesso`: Criação de produto com dados válidos (RF01–RF06, RN01–RN05).
- `test_criar_produto_falha_nome_vazio`: Validação do campo “nome” obrigatório (RN01).
- `test_atualizar_produto_sucesso`: Atualização parcial e validação dos campos (RN07).
- `test_deletar_produto_sem_confirmacao`: Bloqueio de exclusão sem confirmação (RN08).
- `test_deletar_produto_com_confirmacao`: Exclusão bem-sucedida com confirmação.
- `test_listar_produtos`: Verificação da listagem completa de produtos (RN09).
- `test_buscar_produto_por_id`: Valida recuperação de produto por ID (RN10).

### Testes com Service + Mock:

- `test_rn01_nome_obrigatorio`: Validação de nome vazio.
- `test_rn02_nome_unico`: Produto com nome duplicado.
- `test_rn03_preco_maior_que_zero`: Preço menor ou igual a zero.
- `test_rn04_schema_valida_quantidade_negativa`: Quantidade negativa via schema.
- `test_rn05_categoria_obrigatoria`: Campo “categoria” obrigatório.
- `test_rn06_exclusao_com_movimentacoes`: Impede exclusão de produto com movimentações.
- `test_rn07_validacao_update`: Campos inválidos na atualização.
- `test_rn07_schema_valida_quantidade_negativa_update`: Validação negativa no update.
- `test_rn08_exclusao_sem_confirmacao`: Tentativa de exclusão sem confirmação.
- `test_rn09_listar_produtos`: Mock da listagem de produtos.
- `test_rn10_buscar_por_id`: Mock da busca por ID.

---

## Movimentações de Estoque

### Testes com FastAPI:

- `test_criar_movimentacao_entrada_sucesso`: Registro válido de entrada (RN09–RN15).
- `test_movimentacao_produto_inexistente`: Produto não encontrado (RN09).
- `test_movimentacao_quantidade_invalida`: Quantidade zero (RN10).
- `test_movimentacao_data_futura`: Data posterior à atual (RN11).
- `test_movimentacao_tipo_invalido`: Tipo diferente de "entrada" ou "saída" (RN12).
- `test_movimentacao_saida_maior_que_estoque`: Estoque insuficiente (RN13).
- `test_movimentacao_entrada_atualiza_estoque`: Atualização correta após entrada (RN14).
- `test_movimentacao_nao_editavel_ou_excluivel`: Verifica imutabilidade de movimentações (RN15).

### Testes com Service + Mock:

- `test_rn09_produto_inexistente`: Produto não encontrado via service.
- `test_rn10_quantidade_invalida`: Validação de quantidade via schema.
- `test_rn11_data_futura`: Rejeição de movimentação futura.
- `test_rn12_tipo_invalido`: Validação de tipo.
- `test_rn13_saida_estoque_insuficiente`: Estoque insuficiente via lógica de negócio.
- `test_rn14_entrada_saida_sucesso`: Simula movimentações e atualizações de estoque.
- `test_listagens`: Testa listagem geral e por produto com mocks.

---

## Dashboard

- `test_dashboard_endpoint_com_dados`: Testa a rota `/dashboard` validando:

  - **RN16** – Exibição de nome, quantidade e valor total.
  - **RN17** – Filtro por intervalo de datas.
  - **RN18** – Cálculo do valor total em estoque.
  - **RN19** – Produtos mais movimentados.
  - **RN21** – Geração de gráfico de vendas mensais.
  - **RN22** – Produtos com movimentações no período.
  - **RN23** – Datas de movimentações por produto.
  - **RN24** – Detalhamento das saídas.
  - **RN25** – Detalhamento das entradas.
  - **RN26** – Tipo e quantidade de cada movimentação.
  - **RN27** – Valor total de vendas.
  - **RN28** – Quantidade total de itens vendidos.
  - **RN29** – Formato brasileiro de datas (DD/MM/AAAA).
  - **RN30** – Dados consolidados corretamente.
  - **RN31** – Retorno JSON válido.

---

## Relatórios

- `test_relatorio_estoque_json`: Relatório de estoque no formato JSON (RR032, RR034, RR035).
- `test_relatorio_estoque_csv`: Exportação de relatório em CSV (RR033, RR034).
- `test_relatorio_estoque_pdf`: Geração de relatório em PDF (RR033).

---

## Observações Técnicas

- Todos os testes foram escritos com **Pytest**.
- Testes de integração utilizam o `TestClient` do FastAPI para simular requisições HTTP reais ao backend.
- Alguns testes utilizam `MagicMock` e `patch` (do módulo `unittest.mock`) para isolar dependências e simular comportamentos internos na camada de serviço (testes unitários).
- Um banco de dados temporário em **SQLite em memória** é utilizado para testes de integração, sendo criado com `Base.metadata.create_all(bind=engine)`.
- Os dados são reiniciados entre os testes por meio de fixtures como `@pytest.fixture`, geralmente nomeadas como `setup_dados()`.

---

## Execução

Para rodar **todos os testes** da aplicação:

```bash
pytest -s