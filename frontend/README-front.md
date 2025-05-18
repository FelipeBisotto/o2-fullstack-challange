# README FRONTEND – SISTEMA DE GESTÃO DE ESTOQUE

Este guia apresenta o passo a passo para configurar o ambiente do **frontend** do sistema desenvolvido com **React + Vite + TypeScript**.

# Ver documentação completa na raiz do projeto
Consulte a pasta [docs/](../docs) para detalhes sobre a estrutura (requisitos, casos de uso, regras de negócio, modelagem de dados, arquitetura e testes) do projeto.

---

## Requisitos

- Node.js instalado (versão recomendada: 18+)
- npm (instalado junto com o Node.js)
- Backend em execução (para consumir a API)

---

## Instalação e execução

### 1. Acesse o diretório do frontend

```bash
cd frontend
```

### 2. Instale as dependências

```bash
npm install
```

Este comando instala todas as bibliotecas listadas no `package.json`.

### 3. Execute o servidor de desenvolvimento

```bash
npm run dev
```

A aplicação ficará disponível em:

```
http://localhost:5173/
```

---

## Dicas úteis

- Verifique se o backend está rodando em `http://localhost:8000` (ajuste se necessário).
- As rotas da aplicação estão organizadas no arquivo `src/router/app_router.tsx`.
- Os estilos e validações seguem boas práticas com CSS modularizado, TypeScript e Zod.

---

Pronto! O frontend estará em funcionamento e se comunicando com o backend via HTTP.