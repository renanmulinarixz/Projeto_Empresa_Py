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
    def __init__(self, id, quantidade, peca, veiculos, tipo, parte, fabricante, data_cadastro):
        super().__init__(quantidade, tipo)
        self.id = id
        self.peca = peca
        self.veiculos = veiculos
        self.parte = parte
        self.fabricante = fabricante
        self.data_cadastro = data_cadastro  # tem q ser dateTime




class Vendas:
    def __init__(self, produto, preco, quantidadeVendida):
        self.produto = produto
        self.preco = preco
        self.quantidadeVendida = quantidadeVendida

    def getPreco(self):
        print(f"O preço da venda é {self.preco}")

class Funcionario:
    def __init__(self, matricula, nome, setor):
        self.matricula = matricula
        self.nome = nome
        self.setor = setor

class Retirada:
    def __init__(self, funcionario, produto, quantidade, data_hora):
        self.funcionario = funcionario
        self.produto = produto
        self.quantidade = quantidade
        self.data_hora = data_hora

def InfoMenu():
    print(" -- Siga as intrucoes --")
    print("0 - para fechar o programa")
    print("1 - Cadastrar Produto")
    print("2 - Registrar Produção")
    print("3 - Buscar produto")
    print("4 - Buscar por veículo")
    print("5 - Registrar retirada de peça por funcionário")
    print("6 - Cadastrar novo funcionário")

class SistemaPY:
    def __init__(self):
        self.produtosCadastro = []
        self.funcionariosCadastro = []
        self.faturamento = 0
        self.banco = self.InitDB()
        self.carregarFuncionarios()

    def InitDB(self): # link banco de dados com classes
        with open("banco.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados
    
    def carregarFuncionarios(self): # carrega os funcionarios do banco.json para o sistema
        for item in self.banco["funcionarios"]:
            funcionario = Funcionario(
                matricula=item["matricula"],
                nome=item["nome"],
                setor=item["setor"]
            )
            self.funcionariosCadastro.append(funcionario)
        print(f"{len(self.funcionariosCadastro)} funcionários carregados.")

    def buscarFuncionario(self, matricula): # busca funcionario por matricula
        for funcionario in self.funcionariosCadastro:
            if funcionario.matricula == matricula:
                return funcionario
        return None
    
    def geradorMatriculaFuncionario(self):
        dados = self.banco["funcionarios"]
        if not dados:
            return "001"
        ultima = max([int(f["matricula"]) for f in dados])
        return str(ultima + 1).zfill(3)
    
    def cadastrarFuncionario(self):
        matricula = self.geradorMatriculaFuncionario()

        nome = input("Nome do funcionário: ")
        setor = input("Setor do funcionário: ")

        novo_funcionario = Funcionario(matricula, nome, setor)
        self.funcionariosCadastro.append(novo_funcionario)

        with open("banco.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        dados["funcionarios"].append({
            "matricula": matricula,
            "nome": nome,
            "setor": setor
        })

        with open("banco.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=2, ensure_ascii=False)

        self.banco = self.InitDB()
        print(f"Funcionário '{nome}' cadastrado! Matrícula: {matricula}")
    
    def registrarRetirada(self): # registra retirada de peças por funcionarios
        matricula = input("Digite a matrícula do funcionário: ")
        funcionario = self.buscarFuncionario(matricula)

        if not funcionario:
            print("Funcionário não encontrado.")
            return

        nome_peca = input("Digite o nome da peça a retirar: ")
        produto = self.buscar_produto(nome_peca)

        if not produto:
            print("Peça não encontrada.")
            return

        if produto.quantidade <= 0:
            print(f"Sem estoque disponível para '{produto.peca}'.")
            return

        quantidade = int(input(f"Quantidade a retirar (estoque atual: {produto.quantidade}): "))

        if quantidade > produto.quantidade:
            print("Quantidade solicitada maior que o estoque disponível.")
            return

        produto.quantidade -= quantidade
        data_hora = datetime.datetime.now()

        retirada = Retirada(funcionario, produto, quantidade, data_hora)

        # salva no banco.json
        with open("banco.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        dados["retiradas"].append({
            "matricula": funcionario.matricula,
            "funcionario": funcionario.nome,
            "peca": produto.peca,
            "quantidade": quantidade,
            "data_hora": data_hora.strftime("%Y-%m-%d %H:%M:%S")
        })

        with open("banco.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=2, ensure_ascii=False)

        print(f"Retirada registrada! {funcionario.nome} retirou {quantidade}x '{produto.peca}' em {data_hora.strftime('%d/%m/%Y %H:%M')}.")

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
                data_cadastro = item["data_cadastro"]
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
            "data_cadastro": produto.data_cadastro.strftime("%Y-%m-%d %H:%M:%S")
        }

        dados["pecas"].append(novo_dado)
        with open("banco.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=2, ensure_ascii=False) # torna um dicionario dentro do meu arquivo json


    def buscar_por_veiculo(self, veiculo): # busca produtos por veiculo (a ser desenvolvido)
        resultados = []
        for produto in self.produtosCadastro:
            if veiculo.lower() in [v.lower() for v in produto.veiculos]:
                resultados.append(produto)
        return resultados


    def cadastrar_produto(self): #cadastra produtos
        veiculos = []
        id_produto = self.geradorId(self.banco)
        
        quantidade = int(input("Quantidade inicial: "))
        peca = input("Nome da peça: ")
        veiculos.append(input("Veículos compatíveis: "))

        self.VerificadorVeiculos(veiculos)

        tipo = input("Tipo da peça: ")
        parte = input("Parte do veículo: ")
        fabricante = input("Fabricante: ")
        data_cadastro = datetime.datetime.now()

        novo_produto = Produtos(id_produto, quantidade, peca, veiculos, tipo, parte, fabricante, data_cadastro)
        self.produtosCadastro.append(novo_produto) #cria novo objeto Produto
        self.escreverBanco(novo_produto)# adiciona no arquivo json
        self.banco = self.InitDB() # resalva o banco na variavel banco (garantir que estara sempre atualizado)
        print("Produto cadastrado com sucesso!")


    def buscar_produto(self, nome): # busca produtos (a ser alterado)
        for produto in self.produtosCadastro:
            if produto.peca.lower() == nome.lower():
                return produto
        return None


    def registrar_producao(self): # registra producao (a desenvolver)
        nome = input("Nome do produto para produção: ")
        produto = self.buscar_produto(nome)

        if produto:
            quantidade = int(input("Quantidade produzida: "))
            produto.quantidade += quantidade
            print(f"Produção registrada. Novo estoque: {produto.quantidade}")
        else:
            print("Produto não encontrado.")



    def menuAbrir(self): # menu
        self.integracaoDados(self.banco) # integra os dados do json com o sistema
        InfoMenu()
        opcao = None
        while opcao != 0:
            try:
                opcao = int(input("\nDigite sua escolha: "))
                if opcao not in [0, 1, 2, 3, 4, 5, 6]:
                    print("\n[!] Opção inválida! Escolha apenas entre 0, 1, 2, 3, 4, 5, 6.")
                    continue
            except ValueError:
                print("\n[!] Erro: Por favor, digite um número inteiro!")
            else:
                if opcao == 1:
                    print("direcionando voce para cadastrar um produto")
                    self.cadastrar_produto()
                elif opcao == 2:
                    print("direcionando voce para registrar na producao")
                    self.registrar_producao()
                elif opcao == 3:
                    print("direcionando voce para buscar um produto")
                    nome = input("Digite o nome do produto: ")
                    produto = self.buscar_produto(nome)
                    if produto:
                        print(f"Produto encontrado: {produto.peca}, Quantidade: {produto.quantidade}, Tipo: {produto.tipo}")
                    else:
                        print("Produto não encontrado.")
                elif opcao == 4:
                    veiculo = input("Digite o nome do veículo para buscar produtos compatíveis: ")
                    resultados = self.buscar_por_veiculo(veiculo)
                    if resultados:
                        print(f"Produtos compatíveis com {veiculo}:")
                        for produto in resultados:
                            print(f"- {produto.peca} (Tipo: {produto.tipo}, Quantidade: {produto.quantidade})")
                    else:
                        print(f"Nenhum produto encontrado para o veículo {veiculo}.")
                elif opcao == 5:
                    print("direcionando voce para registrar retirada de peça por funcionario")
                    self.registrarRetirada()
                elif opcao == 6:
                    print("Direcionando para cadastro de funcionário")
                    self.cadastrarFuncionario()
                elif opcao == 0:
                    print("Sistema encerrado!")
                    break
            InfoMenu()
           