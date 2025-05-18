# SISTEMA DE GESTÃO DE ESTOQUE – O2 Fullstack Challenge

Este projeto é um sistema completo de gestão de estoque, desenvolvido como parte do desafio O2 Fullstack Challenge.

Ele incorpora:
- Cadastro/Deleção/Edição de produtos
- Movimentações de entrada e saaídas de produtos de estoque
- Agente Inteligente com comandos naturais de consulta de vendas em um período emovimentação de entradas e saídas de produto
- Dashboard interativo com gráfico de vendas mensais, resumo de estoque(valor total em estoque e total de itens/produtos vendidos) e produtos em estoque.
- Relatório de estoque de um período. Engloba nome do produto, quantidade e valor total em estoque.

O desenvolvimento foi feito em **frontend (React + Vite)** e **backend (FastAPI + PostgreSQL)**

> Toda a documentação detalhada está disponível na pasta [`docs/`](./docs), incluindo requisitos, regras de negócio, modelagem, arquitetura e testes.

---

## Estrutura do Projeto

```
├── backend/                   # API REST com FastAPI, PostgreSQL, SQLAlchemy e Pytest
├── frontend/                  # Interface web com React, Vite, TypeScript, Zod e Axios
├── docs/                      # Documentação completa do projeto
├── README.md                  # Este arquivo (resumo geral)

```

---

## Documentações específicas

### [README do Backend ](./README_BACKEND.md)
Instruções de instalação do backend e do banco de dados

### [README do Frontend](./README_FRONTEND.md)
Guia de inicialização do frontend com Vite + React, comunicação com backend

---

## Pré-requisitos gerais

- Python 3.10+
- Node.js 18+
- PostgreSQL 13+
- Navegador atualizado

---

## Como iniciar o projeto (resumo rápido)

1. Inicie o backend e banco dados conforme o [README-back.md](./README-back.md)
2. Inicie o frontend conforme o [README-front.md](./README-front.md)

---

## Agente Inteligente

O projeto conta com um agente inteligente que interpreta comandos como:

- Consultar vendas no dia 15/05/2025
- Consultar vendas de 01/05/2025 até 10/05/2025
- Movimentar entrada de 10 lapis branco no dia 15/05/2025
- Movimentar saída de 10 lápis branco no dia 15/05/2025

Mais detalhes sobre essa funcionalidade estão documentados nos arquivos do backend e frontend.

---

Projeto foi desenvolvido com muita dedicação!
Para dúvidas, melhorias ou sugestões, fico aberto para possíveis conversas futuras.

