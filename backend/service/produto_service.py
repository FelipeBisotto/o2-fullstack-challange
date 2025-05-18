from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from model.produto import Produto
from repository import produto_repository, movimentacao_repository
from schema.produto_schema import ProdutoCreate, ProdutoUpdate


class ProdutoService:
    def __init__(self, db: Session):
        self.db = db

    def criar_produto(self, dados: ProdutoCreate) -> Produto:
        # RN01 – O campo “nome” do produto é obrigatório
        if not dados.nome.strip():
            raise ValueError("O nome do produto é obrigatório.")

        # RN05 – O campo “categoria” é obrigatório
        if not dados.categoria.strip():
            raise ValueError("A categoria do produto é obrigatória.")

        # RN03 – O campo “preço unitário” deve ser maior que zero
        if dados.preco_unitario <= 0:
            raise ValueError("O preço unitário deve ser maior que zero.")

        # RN04 – O campo “quantidade disponível” deve ser maior ou igual a zero
        if dados.quantidade < 0:
            raise ValueError("A quantidade deve ser maior ou igual a zero.")

        # RN02 – O campo “nome” deve ser único no cadastro
        try:
            return produto_repository.criar_produto(self.db, dados)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Já existe um produto com esse nome.")

    def listar_produtos(self) -> list[Produto]:
        return produto_repository.listar_produtos(self.db)

    def buscar_por_id(self, produto_id: int) -> Produto | None:
        return produto_repository.buscar_produto_por_id(self.db, produto_id)

    def buscar_por_nome(self, nome: str) -> Produto | None:
        """
        Permite buscar um produto pelo nome, encapsulando a lógica do repositório.
        Usado por outras camadas como o agent_service.
        """
        return produto_repository.buscar_produto_por_nome(self.db, nome)

    def atualizar_produto(self, produto_id: int, dados: ProdutoUpdate) -> Produto:
        produto = self.buscar_por_id(produto_id)
        if not produto:
            raise ValueError("Produto não encontrado.")

        # RN07 – Ao editar um produto, os dados devem ser revalidados com as mesmas regras do cadastro
        if dados.nome is not None and not dados.nome.strip():
            raise ValueError("O nome do produto é obrigatório.")
        if dados.categoria is not None and not dados.categoria.strip():
            raise ValueError("A categoria do produto é obrigatória.")
        if dados.preco_unitario is not None and dados.preco_unitario <= 0:
            raise ValueError("O preço unitário deve ser maior que zero.")
        if dados.quantidade is not None and dados.quantidade < 0:
            raise ValueError("A quantidade deve ser maior ou igual a zero.")

        # RN02 – O campo “nome” deve ser único no cadastro (se for alterado)
        if dados.nome and dados.nome != produto.nome:
            existente = self.buscar_por_nome(dados.nome)
            if existente and existente.id != produto_id:
                raise ValueError("Já existe um produto com esse nome.")

        try:
            return produto_repository.atualizar_produto(self.db, produto_id, dados)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao atualizar o produto.")

    def deletar_produto(self, produto_id: int, confirmado: bool = False) -> bool:
        # RN08 – A exclusão de um produto deve ser confirmada explicitamente pelo usuário
        if not confirmado:
            raise ValueError("Exclusão não confirmada. Marque como confirmada para prosseguir.")

        produto = self.buscar_por_id(produto_id)
        if not produto:
            raise ValueError("Produto não encontrado.")

        # RN06 – O sistema não deve permitir a exclusão de produtos que possuam movimentações registradas
        movimentacoes = movimentacao_repository.listar_movimentacoes_por_produto(
            self.db, produto_id)
        if movimentacoes:
            raise ValueError("Não é possível excluir um produto com movimentações registradas.")

        return produto_repository.deletar_produto(self.db, produto_id)
