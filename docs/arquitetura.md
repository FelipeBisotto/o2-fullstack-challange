# ARQUITETURA DO SISTEMA

## Objetivo  
Descrever a arquitetura de software adotada no sistema de gestão de estoque, detalhando a divisão de camadas, responsabilidades e a comunicação entre frontend e backend.

---

## Visão Geral

O sistema é dividido em dois módulos principais:

- **Backend:** Desenvolvido em Python com FastAPI, SQLAlchemy e banco de dados PostgreSQL.  
- **Frontend:** Desenvolvido em React + Vite com TypeScript, utilizando Axios para requisições e Zod para validações.

A comunicação entre frontend e backend ocorre via **API RESTful**, com troca de dados em formato **JSON**.

## Tecnologias Utilizadas

### Backend
- Python  
- FastAPI  
- SQLAlchemy  
- PostgreSQL  
- Pydantic  
- Pytest  

### Frontend
- React  
- TypeScript  
- Vite  
- Axios  
- Zod  
- React Router DOM 

---

## Backend – Estrutura de Pastas e Responsabilidades
backend/
├── agent/ incorporado diretamente às camadas padrão do sistema
├── database/ # Conexão e configuração do banco de dados
├── model/ # Entidades ORM mapeadas com SQLAlchemy
├── repository/ # Operações diretas no banco de dados
├── router/ # Definição dos endpoints da API
├── schema/ # DTOs e validações com Pydantic
├── service/ # Regras de negócio e lógica da aplicação
├── tests/ # Testes unitários e de integração
├── utils/ # Funções auxiliares (ex: exportação de relatórios)
└── main.py # Ponto de entrada da aplicação FastAPI


### Fluxo de uma Requisição no Backend:

1. O `router/` recebe a requisição HTTP.
2. O `service/` aplica as regras de negócio e validações.
3. O `repository/` realiza a operação no banco.
4. O `model/` representa a estrutura persistida.
5. A resposta é enviada ao cliente (frontend) em JSON.

---

## Frontend – Estrutura de Pastas e Responsabilidades
frontend/src/
├── components/ # Componentes reutilizáveis (modal, layout, loader, etc.)
├── pages/ # Telas da aplicação (Produtos, Dashboard, Agente, etc.)
├── repository/ # Camada de requisições HTTP com Axios
├── schema/ # Tipagens e validações com Zod
├── service/ # Lógica de transformação de dados e chamada ao repository
├── router/ # Navegação com React Router DOM
├── utils/ # Funções auxiliares (formatação, helpers)
└── App.tsx # Componente principal da aplicação



### Fluxo no Frontend

1. O usuário acessa uma `page/` específica.
2. A página utiliza um `service/` para processar a lógica.
3. O `service/` chama o `repository/`, que executa uma requisição com Axios.
4. A resposta é validada por um `schema/` (Zod) e renderizada na interface (`components/`).

---

## Comunicação entre Backend e Frontend

A integração segue o padrão REST, com endpoints como:

- `GET /produtos/` – Listar produtos
- `POST /movimentacoes/` – Registrar entrada ou saída
- `GET /dashboard/` – Dados agregados e gráficos
- `POST /agente/interpretar-comando` – Comando em linguagem natural

O frontend consome essas rotas usando `axios` via `repository/` e trata os dados com `service/` e `schema/`.

---

## Relação entre as Camadas

| Camada Backend   | Função                                      | Camada Frontend   | Função                                               |
|------------------|---------------------------------------------|--------------------|------------------------------------------------------|
| `model/`         | Mapeamento das entidades no banco           | —                  | Interfaces inferidas a partir dos schemas           |
| `schema/`        | DTOs e validações com Pydantic              | `schema/`          | DTOs e validações com Zod                           |
| `repository/`    | CRUD com SQLAlchemy                         | `repository/`      | Requisições HTTP com Axios                          |
| `service/`       | Regras de negócio e orquestração            | `service/`         | Transformação de dados e chamada ao repository      |
| `router/`        | Endpoints REST da aplicação                 | `pages/ + router/` | Interface e navegação entre telas                   |
| `utils/`         | Helpers e exportação de relatórios          | `utils/`           | Formatação de dados e utilitários genéricos         |

---

## Observações Técnicas

- O backend segue os princípios de **Clean Architecture**, com separação clara entre entidades, lógica de negócio, persistência e API.
- O frontend está **totalmente desacoplado**, consumindo a API como cliente REST.
- Os `schema/` do frontend e backend servem como **DTOs validados**, usando **Pydantic** e **Zod**, respectivamente.
- Toda a aplicação foi construída visando **modularidade**, **testabilidade** e **manutenibilidade**.

---

## Agente Inteligente – Estrutura e Integração

O agente inteligente é um componente que interpreta comandos em linguagem natural e os converte em ações estruturadas dentro do sistema.
Do ponto de vista arquitetural, ele está **integrado diretamente nas camadas existentes** do backend e frontend:

- **Backend:**
  - `router/agent_router.py` – Recebe comandos via API.
  - `service/agent_service.py` – Interpreta e aplica as regras de negócio.
  - `schema/agent_schema.py` – Valida a estrutura dos comandos recebidos.

- **Frontend:**
  - `pages/agent_page.tsx` – Interface para envio de comandos.
  - `repository/agent_repository.ts` – Comunicação com o backend.
  - `service/agent_service.ts` – Interpretação e exibição da resposta.
  - `schema/agent_schema.ts` – Tipagem e validação dos dados recebidos.

### Decisão Arquitetural

Inicialmente previsto como um módulo isolado, o agente foi incorporado diretamente às camadas padrão do sistema para:

- Garantir **consistência estrutural** com os demais módulos.
- Permitir **reaproveitamento dos serviços e repositórios** existentes.
- Facilitar **manutenção, testes e expansão** do sistema.

Essa decisão fortalece o princípio de modularidade e evita a criação de silos desnecessários na aplicação.


### Integração ao Projeto

Inicialmente planejado como um módulo separado, o agente inteligente foi **integrado diretamente às camadas existentes** de backend e frontend para garantir melhor acoplamento com os fluxos do sistema.

### Motivos da Integração Direta

- **Consistência Arquitetural:** o agente agora segue a mesma divisão por camadas usada para produtos, movimentações e relatórios.
- **Evita Redundância:** reutiliza os `services` e `repositories` já existentes sem duplicação de lógica.
- **Manutenção Facilitada:** está alinhado com a estrutura já validada da aplicação, tornando evolução e testes mais simples.

### Estrutura Atual do Agente

#### Backend
- `router/agent_router.py` – Endpoint REST para interpretar comandos.
- `service/agent_service.py` – Processamento da linguagem natural e lógica de decisão.
- `schema/agent_schema.py` – Estrutura e validação dos comandos.

#### Frontend
- `pages/agent_page.tsx` – Interface de entrada do usuário.
- `repository/agent_repository.ts` – Envio da requisição ao backend.
- `service/agent_service.ts` – Processamento da resposta da API.
- `schema/agent_schema.ts` – Tipagem e validação dos comandos no frontend.

---

## Uso das Bibliotecas Axios e Zod

### Axios

- Local: `frontend/src/repository/`
- Função: Executa as chamadas HTTP (`get`, `post`, etc.) para os endpoints da API.
- Exemplo: `axios.post("/movimentacoes", payload)`

### Zod

- Local: `frontend/src/schema/`
- Função: Validação de formulários e resposta da API com tipagem robusta.
- Exemplo: `z.object({ nome: z.string().min(1), preco_unitario: z.number().positive() })`

---