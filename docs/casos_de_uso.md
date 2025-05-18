# CASOS DE USO - SISTEMA DE GESTÃO DE ESTOQUE

## Objetivo

Este documento descreve os casos de uso do sistema de gestão de estoque, com base nos requisitos funcionais identificados. 
O objetivo é esclarecer as interações principais entre o usuário e o sistema, cobrindo as funcionalidades essenciais como cadastro de produtos, 
movimentações de estoque, geração de relatórios, visualização de métricas e comandos por linguagem natural via agente inteligente.
Esses casos de uso foram um esboço para os testes: Teste de Sistema e Teste End-to-End.

---

## UC01 – Cadastrar Produto

**Ator Principal:** Usuário do sistema  
**Descrição:** Permite ao usuário cadastrar um novo produto.  
**Pré-condições:** O sistema está acessível e o usuário está na tela de cadastro.

**Fluxo Principal:**
1. O usuário acessa o formulário de cadastro de produto.
2. Preenche os campos: nome, descrição, categoria, preço unitário, quantidade.
3. Clica em “Salvar”.
4. O sistema valida os dados e armazena o produto.

**Pós-condições:** O produto fica disponível na listagem.

**Fluxo Alternativo:**  
- Se algum campo obrigatório estiver vazio, o sistema exibe uma mensagem de erro.

---

## UC02 – Editar Produto

**Ator Principal:** Usuário do sistema  
**Descrição:** Permite atualizar informações de um produto existente.  
**Pré-condições:** O produto já está cadastrado.

**Fluxo Principal:**
1. O usuário acessa a listagem de produtos.
2. Clica em “Editar” no produto desejado.
3. Altera os dados e clica em “Salvar”.

**Pós-condições:** As informações são atualizadas no sistema.

---

## UC03 – Excluir Produto

**Ator Principal:** Usuário do sistema  
**Descrição:** Permite remover um produto do sistema.  
**Pré-condições:** O produto existe e está selecionado.

**Fluxo Principal:**
1. O usuário acessa a listagem.
2. Clica em “Excluir” e confirma a ação.
3. O sistema remove o produto.

**Pós-condições:** O produto deixa de aparecer na listagem.

---

## UC04 – Registrar Movimentação de Estoque

**Ator Principal:** Usuário do sistema  
**Descrição:** Permite registrar entrada ou saída de um produto no estoque.  
**Pré-condições:** Um produto deve estar previamente cadastrado.

**Fluxo Principal:**
1. O usuário seleciona um produto.
2. Informa tipo (entrada ou saída), data e quantidade.
3. Clica em “Registrar”.
4. O sistema processa e atualiza o estoque.

**Pós-condições:** O estoque é alterado e o registro é salvo.

**Fluxo Alternativo:**  
- Se a saída for maior que o estoque atual, o sistema bloqueia e exibe erro.

---

## UC05 – Consultar Produtos

**Ator Principal:** Usuário do sistema  
**Descrição:** Exibe todos os produtos cadastrados com suas respectivas informações.  
**Pré-condições:** Devem existir produtos no sistema.

**Fluxo Principal:**
1. O usuário acessa a tela de consulta.
2. O sistema exibe a lista com nome, descrição, categoria, preço e quantidade.

---

## UC06 – Gerar Relatório de Estoque Atual

**Ator Principal:** Usuário do sistema  
**Descrição:** Gera uma visão completa do estoque atual da empresa.  
**Pré-condições:** Produtos e quantidades devem estar cadastrados no sistema.

**Fluxo Principal:**
1. O usuário acessa a aba de relatórios.
2. Seleciona a opção “Estoque Atual”.
3. O sistema exibe produtos com quantidade e valor total por item.

---

## UC07 – Gerar Relatório de Movimentações por Período

**Ator Principal:** Usuário do sistema  
**Descrição:** Lista todas as movimentações (entradas/saídas) dentro de um intervalo de tempo.  
**Pré-condições:** Devem existir registros de movimentação.

**Fluxo Principal:**
1. O usuário informa data inicial e final.
2. O sistema retorna todas as movimentações correspondentes ao período.

---

## UC08 – Exibir Dashboard com Métricas e Gráficos

**Ator Principal:** Usuário do sistema  
**Descrição:** Apresenta visão visual e resumida de indicadores de estoque.  
**Pré-condições:** Deve haver movimentações registradas no sistema.

**Fluxo Principal:**
1. O usuário acessa o painel do dashboard.
2. O sistema exibe:
   - Gráfico de vendas por período
   - Valor total em estoque
   - Total de saídas registradas

---

## UC09 – Usar Comando em Linguagem Natural

**Ator Principal:** Usuário do sistema  
**Descrição:** Permite inserir comandos em linguagem natural para interagir com o sistema.  
**Pré-condições:** O agente de IA está disponível.

**Fluxo Principal:**
1. O usuário digita um comando textual (ex: “registrar entrada de 5 cadernos”).
2. O sistema interpreta o comando e executa a ação equivalente.

**Fluxo Alternativo:**  
- Se o comando for ambíguo ou inválido, o sistema solicita confirmação ou exibe uma mensagem de erro.

---
