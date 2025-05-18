# MODELAGEM DE DADOS - - SISTEMA DE GESTÃO DE ESTOQUE

## Objetivo
Este documento descreve a modelagem de dados do sistema de gestão de estoque, com base nas definições das entidades ORM em SQLAlchemy. 
A modelagem contempla os nomes das tabelas, os atributos de cada entidade, seus tipos, restrições e relacionamentos.

---

## Entidade: `Produto`
Tabela responsável por armazenar os dados dos produtos controlados pelo sistema.

### Campos:
| Campo            | Tipo             | Restrições                               | Descrição                               |
|------------------|------------------|-------------------------------------------|--------------------------------------------|
| `id`             | Integer          | PK, auto increment, NOT NULL               | Identificador único do produto              |
| `nome`           | String(100)      | UNIQUE, NOT NULL                           | Nome do produto                             |
| `descricao`      | String           | Opcional                                   | Descrição textual do produto               |
| `categoria`      | String(50)       | NOT NULL                                   | Categoria/classificação do produto         |
| `preco_unitario` | Numeric(10, 2)   | NOT NULL                                   | Preço por unidade                          |
| `quantidade`     | Integer          | NOT NULL                                   | Quantidade atual em estoque                 |

---

## Entidade: `Movimentacao`
Tabela que registra todas as entradas e saídas de estoque vinculadas a produtos.

### Campos:
| Campo         | Tipo         | Restrições                                            | Descrição                                         |
|---------------|--------------|--------------------------------------------------------|----------------------------------------------------|
| `id`          | Integer      | PK, auto increment, NOT NULL                           | Identificador único da movimentação               |
| `tipo`        | String(10)   | NOT NULL, CHECK (“entrada” ou “saida”)                 | Tipo da movimentação                              |
| `quantidade`  | Integer      | NOT NULL, CHECK (> 0)                                  | Quantidade movimentada                            |
| `data`        | DateTime     | NOT NULL, default = datetime.utcnow                    | Data da movimentação                              |
| `produto_id`  | Integer      | FK para `produto.id`, NOT NULL                         | Relacionamento com a entidade Produto             |

### Restrições e Checks:
- `tipo` deve ser "entrada" ou "saida" (`check_tipo_valido`)
- `quantidade` deve ser maior que 0 (`check_quantidade_positiva`)

---

## Relacionamento
- **Produto 1:N Movimentacao**
  - Um produto pode estar associado a diversas movimentações.
  - Cada movimentação está ligada a apenas um produto.

---

## Considerações Adicionais
- O modelo foi implementado com SQLAlchemy, com mapeamento via classes e uso de `Base = declarative_base()`.
- A conexão com o banco de dados é configurada dinamicamente via variável de ambiente `DATABASE_URL`.
- Todas as tabelas são criadas com `Base.metadata.create_all()` utilizando o engine configurado.

---

## Trecho SQL Equivalente (DDL)
```sql
CREATE TABLE produto (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    descricao TEXT,
    categoria VARCHAR(50) NOT NULL,
    preco_unitario NUMERIC(10, 2) NOT NULL,
    quantidade INTEGER NOT NULL
);

CREATE TABLE movimentacao (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('entrada', 'saida')),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    produto_id INTEGER NOT NULL REFERENCES produto(id)
);
