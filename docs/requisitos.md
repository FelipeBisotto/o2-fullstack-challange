# REQUISITOS - SISTEMA DE GESTÃO DE ESTOQUE

## Objetivo

Este documento reúne os **Requisitos Funcionais (RF)**, **Requisitos Não Funcionais (RNF)** e as **Regras de Negócio (RN)** do sistema de gestão de estoque. 
Ele foi criado como **primeira etapa do processo de desenvolvimento**, servindo como base para a compreensão das funcionalidades esperadas, as restrições do domínio 
e as validações a serem aplicadas no backend e frontend. Alguns requisitos foram modificados durante o rpocesso de desenvolvimto.para a compreensao melhor do codigo e desenvolvimento os alguns dos requisitos e regras de negocios sao comentandos qaundo alguma funcionalidade é implementada ou testada
Essa especificação foi essencial para guiar a modelagem do sistema, a criação de casos de uso, a implementação de regras e a posterior realização dos testes de sistema e testes automatizados.

---

## Produtos

### Requisitos Funcionais
- **RF01** – O sistema deve permitir o cadastro de produtos.  
- **RF02** – O sistema deve permitir informar o campo “nome” ao cadastrar um produto.  
- **RF03** – O sistema deve permitir informar o campo “descrição” ao cadastrar um produto.  
- **RF04** – O sistema deve permitir informar o campo “categoria” ao cadastrar um produto.  
- **RF05** – O sistema deve permitir informar o campo “preço unitário” ao cadastrar um produto.  
- **RF06** – O sistema deve permitir informar o campo “quantidade disponível” ao cadastrar um produto.  
- **RF07** – O sistema deve permitir a edição de um produto existente.  
- **RF08** – O sistema deve permitir a exclusão de um produto do cadastro.  
- **RF16** – O sistema deve permitir consultar a lista de produtos cadastrados.  
- **RF17** – O sistema deve apresentar o campo “nome” na consulta de produtos.  
- **RF18** – O sistema deve apresentar o campo “descrição” na consulta de produtos.  
- **RF19** – O sistema deve apresentar o campo “categoria” na consulta de produtos.  
- **RF20** – O sistema deve apresentar o campo “preço unitário” na consulta de produtos.  
- **RF21** – O sistema deve apresentar o campo “quantidade disponível” na consulta de produtos.  

### Regras de Negócio
- **RN01** – O campo “nome” do produto é obrigatório.  
- **RN02** – O campo “nome” deve ser único no cadastro.  
- **RN03** – O campo “preço unitário” deve ser maior que zero.  
- **RN04** – O campo “quantidade disponível” deve ser maior ou igual a zero.  
- **RN05** – O campo “categoria” é obrigatório.  
- **RN06** – O sistema não deve permitir a exclusão de produtos que possuam movimentações registradas.  
- **RN07** – Ao editar um produto, os dados devem ser revalidados com as mesmas regras do cadastro.  
- **RN08** – A exclusão de um produto deve ser confirmada explicitamente pelo usuário.  
- **RN09** – O sistema deve permitir a listagem de todos os produtos cadastrados.  
- **RN10** – O sistema deve permitir a busca de um produto por seu ID.  

---

## Movimentações de Estoque

### Requisitos Funcionais
- **RF09** – O sistema deve permitir registrar movimentações de estoque do tipo “entrada”.  
- **RF10** – O sistema deve permitir registrar movimentações de estoque do tipo “saída”.  
- **RF11** – O sistema deve permitir informar o campo “data” ao registrar uma movimentação.  
- **RF12** – O sistema deve permitir informar o campo “quantidade” ao registrar uma movimentação.  
- **RF13** – O sistema deve permitir associar uma movimentação a um produto.  
- **RF14** – O sistema deve atualizar automaticamente o estoque do produto após o registro de uma movimentação.  
- **RF15** – O sistema deve impedir o registro de movimentações de saída cuja quantidade seja superior à quantidade em estoque.  

### Regras de Negócio
- **RN09** – Toda movimentação deve estar associada a um produto existente.  
- **RN10** – O campo “quantidade” da movimentação deve ser um número inteiro maior que zero.  
- **RN11** – A data da movimentação não pode ser posterior à data atual.  
- **RN12** – O campo “tipo de movimentação” deve ser obrigatoriamente “entrada” ou “saída”.  
- **RN13** – Em uma movimentação do tipo “saída”, a quantidade solicitada não pode ultrapassar a quantidade disponível em estoque.  
- **RN14** – O sistema deve atualizar automaticamente a quantidade em estoque de um produto após a movimentação ser registrada.  
- **RN15** – Uma movimentação não pode ser editada ou excluída após ser registrada.  

---

## Dashboard

### Requisitos Funcionais
- **RF27** – O sistema deve apresentar um dashboard com gráfico de vendas por período.  
- **RF28** – O sistema deve apresentar no dashboard o valor total em estoque.  
- **RF29** – O sistema deve apresentar no dashboard o total de saídas registradas.  
- **RF26** – O sistema deve exibir os produtos mais movimentados, ordenados por número de movimentações.  
- **RF24** – O sistema deve calcular o valor total em estoque com base em (quantidade × preço unitário) de cada item.  
- **RF25** – O sistema deve calcular a quantidade total de itens vendidos, com base nas movimentações de saída.  

### Regras de Negócio
- **RN16** – O dashboard deve exibir nome, quantidade e valor total de cada produto.  
- **RN17** – Deve permitir filtros por intervalo de datas válidas.  
- **RN18** – O valor em estoque deve ser calculado em tempo real.  
- **RN19** – Os produtos mais movimentados devem ser ordenados por movimentações (entradas + saídas).  
- **RN20** – O padrão de visualização deve ser dos últimos 12 meses, com opção de filtro personalizado.  
- **RN21** – O gráfico deve considerar apenas saídas.  
- **RN22** – O dashboard deve listar produtos com movimentações em um intervalo informado.  
- **RN23** – Deve exibir as datas de todas as movimentações de cada produto.  
- **RN24** – Deve apresentar separadamente as datas e quantidades de saídas (vendas).  
- **RN25** – Deve apresentar separadamente as datas e quantidades de entradas (reposição).  
- **RN26** – Deve informar o tipo de movimentação e quantidade em cada exibição.  
- **RN27** – Deve calcular o valor total de vendas por período.  
- **RN28** – Deve somar a quantidade total de itens vendidos no período.  
- **RN29** – Datas exibidas devem estar no formato brasileiro (DD/MM/AAAA).  
- **RN30** – Deve disponibilizar um endpoint REST para fornecer os dados do dashboard.  
- **RN31** – As visualizações devem ser retornadas em JSON por padrão, com possibilidade futura de exportação.  

---

## Relatórios

### Requisitos Funcionais
- **RF22** – O sistema deve gerar relatório de estoque atual com nome do produto, quantidade disponível e valor total por item.  
- **RF23** – O sistema deve gerar relatório de movimentações de estoque filtradas por intervalo de datas.  
- **RF33** – O sistema deve permitir visualizar relatórios por meio da interface frontend.  

### Regras de Negócio
- **RN32** – Os relatórios devem ser gerados a partir dos dados do dashboard.  
- **RN33** – Devem ser disponibilizados em CSV e PDF.  
- **RN34** – Devem refletir exatamente os dados filtrados no dashboard.  
- **RN35** – O formato das datas deve seguir o padrão DD/MM/AAAA.  

---

## Agente Inteligente

### Requisitos Funcionais

- **RF32** – O sistema deve aceitar comandos textuais com os verbos “movimentar” ou “consultar”.
- **RF33** – O sistema deve identificar automaticamente: tipo da operação, nome do produto, quantidade e data.
- **RF34** – O sistema deve validar os comandos e exibir mensagens de erro se incompletos.
- **RF35** – O sistema deve interpretar expressões como “este mês”, “abril de 2025”, “de 01/03 até 30/03”.
- **RF36** – O sistema deve responder com dados estruturados e compreensíveis.
- **RF37** – A data padrão para movimentações deve ser a data atual.
- **RF38** – O sistema deve tratar letras maiúsculas e acentos de forma insensível.

### Regras de Negócio

- **RN24** – Apenas comandos com os verbos “movimentar” e “consultar” são aceitos.
- **RN25** – A quantidade deve ser um número inteiro positivo.
- **RN26** – A movimentação só pode ser realizada na data atual.
- **RN27** – Tipos de movimentação válidos: “entrada” e “saída”.
- **RN28** – Expressões relativas de tempo (ex: “última semana”) devem ser interpretadas corretamente.
- **RN29** – O sistema deve aceitar comandos com ou sem acentuação gráfica e com qualquer uso de maiúsculas/minúsculas.
- **RN30** – O produto informado deve existir previamente no cadastro.

---

## Interface e Validação (Frontend)

### Regras de Negócio
- **RN26** – Todos os campos obrigatórios devem ser verificados no frontend antes do envio.  
- **RN27** – Todos os dados devem ser validados também no backend.  
- **RN28** – O sistema deve apresentar mensagens de erro claras e específicas.  
- **RN29** – Campos numéricos devem aceitar apenas valores válidos.  
- **RN30** – Campos de texto devem aceitar no máximo 255 caracteres (exceto descrições).  

---

## Requisitos Não Funcionais (RNF)

- **RNF01** – Utilizar banco de dados relacional PostgreSQL.  
- **RNF02** – Backend em Python com FastAPI.  
- **RNF03** – Frontend em React, com layout responsivo.    
- **RNF05** – Validação obrigatória de campos e impedimento de envio de dados inválidos.  
- **RNF06** – Arquitetura backend modular: rotas, modelos, serviços, esquemas e banco.  
- **RNF10** – O agente de IA deve interpretar comandos simples com regras/linguagem natural.  