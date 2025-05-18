# README BACKEND E BANCO DE DADOS – SISTEMA DE GESTÃO DE ESTOQUE

# Setup do Projeto – Sistema de Gestão de Estoque

Este guia descreve como preparar e executar o sistema localmente, incluindo instalação de dependências, configuração do banco de dados e execução do backend.

# Ver documentação completa na raiz do projeto
Consulte a pasta [docs/](../docs) para detalhes sobre a estrutura(requisitos, casos de uso, regras de negócio, modelagem de dados, arquitetura e testes) do projeto.
---

---

## 1. Instalação das Dependências

1. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
```

2. Ative o ambiente virtual:

- **Windows (bash):**
  ```bash
  source venv/Scripts/activate
  ```

- **Windows (cmd):**
  ```cmd
  venv\Scripts\activate
  ```

- **PowerShell:**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

- **Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```

3. Entre na pasta backend:
cd backend
Instale as dependências com base no `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 2. Banco de Dados – PostgreSQL

O sistema utiliza um banco PostgreSQL chamado `estoque`. Crie o banco conforme as instruções abaixo:

### Opção 1 – SQL Shell (psql)

1. Abra o **SQL Shell (psql)**.
2. Pressione `Enter` até o campo da porta. Digite: `5433`.

Server [localhost]:           <-- pressione ENTER
Database [postgres]:          <-- pressione ENTER
Port [5432]: 5433             <-- digite 5433
Username [postgres]:          <-- pressione ENTER
Password for user postgres:   <-- digite sua senha

3. Digite sua senha do PostgreSQL.
4. Depois de conectado, no terminal do psql, evocê verá algo assim:

postgres=#

Digite o comando: CREATE DATABASE estoque;
Ex: postgres=# CREATE DATABASE estoque;

5. Depois entre no estoque
\c estoque
Ex: postgres=# \c estoque

6. Digite o comando: CREATE EXTENSION IF NOT EXISTS unaccent;
estoque=# CREATE EXTENSION IF NOT EXISTS unaccent;

> Isso criará o banco de dados necessário.

### Opção 2 – pgAdmin

1. Abra o **pgAdmin**.
2. Conecte-se ao servidor PostgreSQL.
3. Clique com o botão direito em **Databases > Create > Database**.
4. Nomeie como `estoque` e clique em **Save**.
5. Clique com o botao direiro em estoque. Va em Query Tool e insira o comando:
```sql
CREATE EXTENSION IF NOT EXISTS unaccent;
```

---

## 3. Configuração do `.env`

1. Crie um arquivo `.env` na pasta `backend/`.

2. Copie e edite o conteúdo abaixo com seus dados reais:

```env
DATABASE_URL=postgresql://postgres:sua_senha@localhost:5433/estoque
```
# Ex:
DATABASE_URL=postgresql://admin:minhasenha123@192.168.0.100:5432/estoque

| Campo   | Valor           |
| ------- | --------------- |
| Usuário | `admin`         |
| Senha   | `minhasenha123` |
| Host    | `192.168.0.100` |
| Porta   | `5432`          |
| Banco   | `estoque`       |

# 3. Já está finalizada a configuração 

---

## 4. Executando o Backend

Com tudo pronto, inicie o backend com o seguinte comando (no diretório `backend/`):

```bash
uvicorn main:app --reload
```

> O servidor será iniciado em: http://127.0.0.1:8000

---

## Pronto!

O sistema estará em execução. Use a interface frontend (React) para interagir com ele ou explore os endpoints diretamente via Swagger em:

```
http://127.0.0.1:8000/docs
```
