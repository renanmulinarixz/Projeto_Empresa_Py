import json
import datetime


class Producao:
    def __init__(self, quantidade, tipo):
        self.quantidade = quantidade
        self.tipo = tipo

    def getQuantidade(self):
        print(f'a quantidade produzida foi {self.quantidade}')

    def getTipo(self):
        print(f'o tipo é {self.tipo}')


class Produtos(Producao):
    def __init__(self, id, quantidade, peca, veiculos, tipo, parte, fabricante, data_producao):
        super().__init__(quantidade, tipo)
        self.id = id
        self.peca = peca
        self.veiculos = veiculos
        self.parte = parte
        self.fabricante = fabricante
        self.data_producao = data_producao  # tem q ser dateTime




class Vendas:
    def __init__(self, produto, preco, quantidadeVendida):
        self.produto = produto
        self.preco = preco
        self.quantidadeVendida = quantidadeVendida

    def getPreco(self):
        print(f"O preço da venda é {self.preco}")



class SistemaPY:
    def __init__(self):
        self.produtosCadastro = []
        self.faturamento = 0
        self.banco = self.InitDB()

    def InitDB(self): # link banco de dados com classes
        with open("banco.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados

    def integracaoDados(self, dadosDoJson): #instancia todos os dados do json dentro do objeto produtos
        print("Cadastrando produtos")
        for item in dadosDoJson["pecas"]:
            produto = Produtos(
                id = item["id"],
                peca = item["peca"],
                quantidade = 0,
                fabricante = item["fabricante"],
                tipo = item["tipo"],
                veiculos = item["veiculos"],
                parte = item["parte"],
                data_producao = item["data_fabricacao"]
            )
            self.produtosCadastro.append(produto)
        print(f"sucesso {len(self.produtosCadastro)} foram adicionados a produtos")
        return self.produtosCadastro

    def geradorId(self, dados): # gera proximo id ao registrar novo produto
        return max([p['id'] for p in dados['pecas']]) + 1

    def VerificadorVeiculos(self, veiculos): # verifica se a pessoa deseja adicionar mais algum veiculo
        escolha = None
        while (escolha != "n" and escolha != "nao"):
            print("deseja cadastras mais algum veiculo que seja compativel? S or N")
            escolha = input("").lower()
            if escolha in ["n", "nao"]:
                break
            print("coloque o nome do novo veiculo")
            veiculos.append(input(""))
        print("produtos cadastrados")

    def escreverBanco(self, produto): # escreve novo dado dentro do json
        with open("banco.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        
        novo_dado = {
            "id": produto.id,
            "peca": produto.peca,
            "tipo": produto.tipo,
            "parte": produto.parte,
            "veiculos": produto.veiculos,
            "fabricante": produto.fabricante,
            "data_fabricacao": produto.data_producao.strftime("%Y-%m-%d")
        }

        dados["pecas"].append(novo_dado)
        with open("banco.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=2, ensure_ascii=False) # torna um dicionario dentro do meu arquivo json


sistema = SistemaPY() 


def cadastrar_produto(): #cadastra produtos
    veiculos = []
    id_produto = sistema.geradorId(sistema.banco)
    
    quantidade = int(input("Quantidade inicial: "))
    peca = input("Nome da peça: ")
    veiculos.append(input("Veículos compatíveis: "))

    sistema.VerificadorVeiculos(veiculos)

    tipo = input("Tipo da peça: ")
    parte = input("Parte do veículo: ")
    fabricante = input("Fabricante: ")
    data_producao = datetime.date.today()

    novo_produto = Produtos(id_produto, quantidade, peca, veiculos, parte, tipo, fabricante, data_producao)
    sistema.produtosCadastro.append(novo_produto) #cria novo objeto Produto
    sistema.escreverBanco(novo_produto)# adiciona no arquivo json
    sistema.banco = sistema.InitDB() # resalva o banco na variavel banco (garantir que estara sempre atualizado)
    print("Produto cadastrado com sucesso!")


def buscar_produto(nome): # busca produtos (a ser alterado)
    for produto in sistema.produtosCadastro:
        if produto.peca.lower() == nome.lower():
            return produto
    return None


def registrar_producao(): # registra producao (a desenvolver)
    nome = input("Nome do produto para produção: ")
    produto = buscar_produto(nome)

    if produto:
        quantidade = int(input("Quantidade produzida: "))
        produto.quantidade += quantidade
        print(f"Produção registrada. Novo estoque: {produto.quantidade}")
    else:
        print("Produto não encontrado.")


def menuAbrir(): # menu
    print(" -- Siga as intrucoes --")
    print("0 - para fechar o programa")
    print("1 - Cadastrar Produto")
    print("2 - Registrar Produção")

    opcao = None
    while opcao != 0:
        try:
            opcao = int(input("\nDigite sua escolha: "))
            if opcao not in [0, 1, 2]:
                print("\n[!] Opção inválida! Escolha apenas entre 0, 1 ou 2.")
                continue
        except ValueError:
            print("\n[!] Erro: Por favor, digite um número inteiro!")
        else:
            if opcao == 1:
                print("direcionando voce para cadastrar um produto")
                cadastrar_produto()
            elif opcao == 2:
                print("direcionando voce para registrar na producao")
                registrar_producao()
            elif opcao == 0:
                print("Sistema encerrado!")
                break
        print(" -- Siga as intrucoes --")
        print("0 - para fechar o programa")
        print("1 - Cadastrar Produto")
        print("2 - Registrar Produção")