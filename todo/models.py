from django.db import models
from django.contrib.auth import get_user_model
from functools import reduce

User = get_user_model()

# Create your models here.
class TodoItem(models.Model):
  content = models.TextField()

class Instituicao(models.Model):
  nome = models.CharField("Nome", max_length = 100)
  descricao = models.CharField("Descrição", max_length = 500)
  sobre = models.CharField("Sobre", max_length = 1000, default="")
  email = models.CharField("E-mail", max_length = 100, default="")
  produtos = models.ManyToManyField("Produto", verbose_name="Produtos")
  fotoCapa = models.ImageField(upload_to='instituicoes', max_length=255, null=True)
  def __str__(self):
    return self.nome
  class Meta:
    verbose_name = "Instituição"
    verbose_name_plural = "Instituições"

class Produto(models.Model):
  nome = models.CharField("Nome do produto", max_length = 100)
  descricao = models.TextField("Descrição")
  preco = models.IntegerField("Preço")
  disponivel = models.CharField("Disponível", max_length = 50)
  fotoCapa = models.ImageField(upload_to='produtos', max_length=255, null=True)
  def __str__(self):
    return self.nome
  class Meta:
    verbose_name = "Produto"
    verbose_name_plural = "Produtos"



class Doador(models.Model):
  nome = models.CharField("Nome", max_length = 100)
  sobrenome = models.CharField("Sobrenome", max_length = 100)
  data = models.DateField("Data de nascimento")
  email = models.CharField("E-mail", max_length = 100)
  user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuário logado", null=True)


  def __str__(self):
    return f"{self.nome} - {self.email} - {self.data}"
  class Meta:
    verbose_name = "Doador"
    verbose_name_plural = "Doadores"


class Duvida(models.Model):
  pergunta = models.TextField("Pergunta")
  resposta = models.TextField("Resposta")
  def __str__(self):
      return str(self.pergunta)
  class Meta:
      verbose_name = "Dúvida frequente"
      verbose_name_plural = "Dúvidas frequentes"


class Pedido(models.Model):
  doador = models.ForeignKey(Doador, on_delete=models.PROTECT, verbose_name="Doador", null=True)
  finalizado = models.BooleanField()

  def __str__(self):
      return "Pedido N " + str(self.id)

  @property
  def itens(self):
    return Item.objects.filter(pedido=self)

  @property
  def valorTotal(self):
    #busca os itens deste pedido
    itens = list(Item.objects.filter(pedido=self))

    #soma os valores dos itens no pedido
    return reduce(lambda x, y: x + y, list(map(lambda item: item.preco, itens)), 0)

class Item(models.Model):
  pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, verbose_name="Pedido", null=True)
  instituicao = models.ForeignKey(Instituicao, on_delete=models.PROTECT, verbose_name="Instituicao", null=True)
  produto = models.ForeignKey(Produto, on_delete=models.PROTECT, verbose_name="Produto", null=True)
  quantidade = models.IntegerField(default=1)

  @property
  def preco(self):
    return self.produto.preco * self.quantidade


class Contato(models.Model):
  nome = models.CharField("Nome", max_length = 100)
  email = models.CharField("E-mail", max_length = 100)
  telefone = models.CharField("Telefone", max_length=100)
  assunto = models.ForeignKey('Assunto', on_delete=models.PROTECT, verbose_name="Assunto", null=True)
  mensagem = models.CharField("Mensagem", max_length = 1000)

  def __str__(self):
    return f"{self.nome} - {self.email} - {self.telefone}"
  class Meta:
    verbose_name = "Contato"
    verbose_name_plural = "Contatos"

class Assunto(models.Model):
  nome = models.CharField("Nome", max_length=255)
  
  def __str__(self):
      return self.nome
  class Meta:
      verbose_name = "Assunto"
      verbose_name_plural = "Assuntos" 


