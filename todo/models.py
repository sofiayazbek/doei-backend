from django.db import models

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
  def __str__(self):
    return self.nome
  class Meta:
    verbose_name = "Produto"
    verbose_name_plural = "Produtos"

class Item(models.Model):
  quantidade = models.IntegerField("Quantidade")
  def __str__(self):
    return self.quantidade
  class Meta:
    verbose_name = "Item"
    verbose_name_plural = "Itens"

class Doador(models.Model):
  nome = models.CharField("Nome", max_length = 100)
  sobrenome = models.CharField("Sobrenome", max_length = 100)
  data = models.DateField("Data de nascimento")
  email = models.CharField("E-mail", max_length = 100)
  senha = models.CharField("Senha", max_length = 120, default="")


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


class Cesta(models.Model):
  total = models.IntegerField("Total")
  data = models.DateField("Data de entrega para a Instituição")
  def __str__(self):
      return str(self.total)
  class Meta:
      verbose_name = "Cesta"
      verbose_name_plural = "Cestas"

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
  