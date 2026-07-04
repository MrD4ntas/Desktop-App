from __future__ import annotations
from abc import ABC, abstractmethod
import time

class Produto(ABC):
    @property
    @abstractmethod
    def nome(self):
        pass
    @property
    @abstractmethod
    def preco(self):
        pass

#HERANÇA
class Comida(Produto):
    def __init__(self, nome: str, preco: float):
        self._nome = nome
        self._preco = preco

    @property
    def nome(self):
        return self._nome
    @property
    def preco(self):
        return self._preco

class Bebida(Produto):
    def __init__(self, nome: str, preco: float):
        self._nome = nome
        self._preco = preco

    @property
    def nome(self):
        return self._nome
    @property
    def preco(self):
        return self._preco

#ASSOCIAÇÃO com Comida e Bebida
class Cardapio:
    def __init__(self):
        self._lista_comidas = []
        self._lista_bebidas = []

    #Permite adicionar mais de um item na mesma função ↓:
    def adicionar_comidas(self, *comidas: Comida):
        for comida in comidas:
            self._lista_comidas.append(comida)

    def adicionar_bebidas(self, *bebidas: Bebida):
        for bebida in bebidas:
            self._lista_bebidas.append(bebida)

    def mostrar_comidas(self):
        print("Comidas do cardápio:")
        if self._lista_comidas:
            for comida in self._lista_comidas:
                print(f"- {comida.nome} (R$ {comida.preco})") # Acessando a propriedade
        else:
            print("- Nenhuma comida no cardápio.")

    def mostrar_bebidas(self):
        print("Bebidas do cardápio:")
        if self._lista_bebidas:
            for bebida in self._lista_bebidas:
                print(f"- {bebida.nome} (R$ {bebida.preco})") # Acessando a propriedade
        else:
            print("- Nenhuma bebida no cardápio.")

class Pedido:
    def __init__(self):
        self._pedidos = []

    def mostrar_pedidos(self):
        if not self._pedidos:
            print("\nA sacola está vazia.")
        else:
            print("\nItens na sacola:")
            for item in self._pedidos:
                print(f"- {item.nome} (R$ {item.preco})")

    #para fazer o pedido é necessario selecionar o cardápio e o item desse cardápio ↓: DEPENDÊNCIA
    def fazer_pedido_comida(self, cardapio: Cardapio, id_comida: int): 
        comida = cardapio._lista_comidas[id_comida - 1]
        print(f"Pedido realizado: {comida.nome}")
        self._pedidos.append(comida) # Adiciona o objeto inteiro
        
    def fazer_pedido_bebida(self, cardapio: Cardapio, id_bebida: int):
        bebida = cardapio._lista_bebidas[id_bebida - 1]
        print(f"Pedido realizado: {bebida.nome}")
        self._pedidos.append(bebida) # Adiciona o objeto inteiro
        
    def cancelar_pedido(self, id_pedido: int):
        if 1 <= id_pedido <= len(self._pedidos):
            # O ID digitado corresponde ao índice (id_pedido - 1) na nossa lista de objetos
            pedido_encontrado = self._pedidos[id_pedido - 1]
            print(f"Pedido cancelado: {pedido_encontrado.nome}")
            self._pedidos.remove(pedido_encontrado)
        else:
            print(f"Pedido não encontrado: {id_pedido}")

    #POLIMORFISMO: ao usar a função calcular_total, utiliza os preços únicos de cada objeto de Comida e Bebida
    def calcular_total(self):
        total = sum(item.preco for item in self._pedidos)
        return total
    
#COMPOSIÇÃO
class Cliente:
    def __init__(self, nome: str):
        self._nome = nome
        #Cliente instancia Pedido, se Cliente deixar de existir Pedido também deixará de existir ↓:
        self._pedido = Pedido()

    @property
    def nome(self):
        return self._nome
    @property
    def pedido(self):
        return self._pedido

class Sistema:
    def __init__(self, cliente: Cliente, cardapio: Cardapio):
        self._cliente = cliente
        self._cardapio = cardapio

    def rodar_sistema(self):
        """Executa a interface funcional do aplicativo no terminal"""
        while True:
            print("\n" + "-"*30, "MENU PRINCIPAL", "-"*30)
            print("1 - Cardápio de Comidas")
            print("2 - Cardápio de Bebidas")
            print("3 - Remover item da sacola")
            print("4 - Ver pedidos")
            print("5 - Finalizar pedido\n")
            x = input("Escolha uma opção: ")

            # CARDÁPIO COMIDAS
            if x == "1":
                for i in range(len(self._cardapio._lista_comidas)):
                    comida = self._cardapio._lista_comidas[i]
                    print(f"{i+1} - {comida.nome} (R$ {comida.preco})")
                    
                escolha = int(input("\nEscolha um item: "))

                if escolha > len(self._cardapio._lista_comidas) or escolha <= 0:
                    print("Opção inválida. Tente novamente.")
                else:
                    self._cliente.pedido.fazer_pedido_comida(self._cardapio, escolha)
                
            # CARDÁPIO BEBIDAS
            elif x == "2":
                for i in range(len(self._cardapio._lista_bebidas)):
                    bebida = self._cardapio._lista_bebidas[i]
                    print(f"{i+1} - {bebida.nome} (R$ {bebida.preco})")
                    
                escolha = int(input("\nEscolha um item: "))

                if escolha > len(self._cardapio._lista_bebidas) or escolha <= 0:
                    print("Opção inválida. Tente novamente.")
                else:
                    self._cliente.pedido.fazer_pedido_bebida(self._cardapio, escolha)

            # REMOVER ITEM DA SACOLA
            elif x == "3":
                if not self._cliente.pedido._pedidos:
                    print("A sacola está vazia. Não há itens para remover.")
                else:
                    for i in range(len(self._cliente.pedido._pedidos)):
                        item = self._cliente.pedido._pedidos[i]
                        print(f"{i+1} - {item.nome}")
                        
                    escolha = int(input("\nEscolha o item que deseja remover: "))
                    self._cliente.pedido.cancelar_pedido(escolha)

            # VER PEDIDOS
            elif x == "4":
                self._cliente.pedido.mostrar_pedidos()
                print(f"Valor total atual: R$ {self._cliente.pedido.calcular_total()}")

            # FINALIZAR PEDIDO
            elif x == "5":
                print("Você finalizou o pedido")
                break

        # FLUXO DE PAGAMENTO
        total_final = self._cliente.pedido.calcular_total()
        print(f"\nValor total final: R$ {total_final}")

        if total_final == 0:
            print("Não há itens no pedido. Encerrando o aplicativo.")
            return # Sai do método rodar_sistema
        else:
            pagamento = input("\nEscolha a forma de pagamento: \n1 - dinheiro\n2 - cartão\n3 - pix\nOpção: ")

            if pagamento == "1":
                print("\nPagamento em dinheiro selecionado.")
            elif pagamento == "2":
                print("\nPagamento em cartão selecionado.")
            elif pagamento == "3":
                print("\nPagamento via PIX selecionado.")

            print("\nProcessando pagamento...")
            time.sleep(3)
            print("\nPagamento concluído.")
            print(f"\nObrigado por comprar conosco, {self._cliente.nome}! Volte sempre.")


# =====================================================================
# CONFIGURAÇÃO INICIAL (Instanciando os objetos obrigatórios para o menu)
# =====================================================================

# 1. Criando os produtos
lasanha = Comida("Lasanha", 35.00)
batata_frita = Comida("Batata Frita", 15.00)
cachorro_quente = Comida("Cachorro Quente", 20.00)
hamburguer = Comida("Hambúrguer", 25.50)
refrigerante = Bebida("Refrigerante", 6.00)
suco_de_laranja = Bebida("Suco de Laranja", 8.00)
suco_de_acerola = Bebida("Suco de Acerola", 7.00)
refrigerante_zero = Bebida("Refrigerante Zero", 6.50)


# 2. Criando o cardápio único do restaurante e adicionando os itens
cardapio_restaurante = Cardapio()
cardapio_restaurante.adicionar_comidas(lasanha, hamburguer, batata_frita, cachorro_quente)
cardapio_restaurante.adicionar_bebidas(refrigerante,refrigerante_zero, suco_de_laranja, suco_de_acerola)

# 3. Criando o cliente que usará o sistema
cliente1 = Cliente("Fulano")

# Criando o sistema, quem vai usar, e qual o cardápio nele ↓:
app = Sistema(cliente1, cardapio_restaurante)

#rodando o sistema ↓:
app.rodar_sistema()