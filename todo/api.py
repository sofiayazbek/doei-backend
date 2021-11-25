from rest_framework import routers, serializers, viewsets, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.permissions import IsAuthenticated

#from django.contrib.auth import authenticate, user_logged_in
from django.contrib.auth import authenticate, login, logout
from todo.models import Duvida, Instituicao, Produto, Doador, Contato, Assunto, Pedido, Item


# Serializers define the API representation.
class DuvidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duvida
        fields = ['pergunta', 'resposta']

# ViewSets define the view behavior.
class DuvidaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Duvida.objects.all()
    serializer_class = DuvidaSerializer

# Serializers define the API representation.
class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

# ViewSets define the view behavior.
class ProdutoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

# Serializers define the API representation.
class InstituicaoSerializer(serializers.ModelSerializer):
    produtos = ProdutoSerializer(many=True, read_only=True)
    class Meta:
        model = Instituicao
        fields = ['id', 'nome', 'descricao', 'sobre','produtos', 'fotoCapa']

# ViewSets define the view behavior.
class InstituicaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instituicao.objects.all()
    serializer_class = InstituicaoSerializer

#Cadastro
class CreateDoadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doador
        fields = ['id', 'nome','sobrenome', 'email', 'data', 'user']

class CreateDoadorViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  serializer_class = CreateDoadorSerializer   
  queryset = Doador.objects.all()

  def perform_create(self, serializer):
    serializer.save(user = self.request.user)


# Serializers define the API representation.
class AssuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assunto
        fields = ['id', 'nome']

# ViewSets define the view behavior.
class AssuntoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Assunto.objects.all().order_by('nome')
    serializer_class = AssuntoSerializer

#Contato
class CreateContatoSerializer(serializers.ModelSerializer):
    assunto: AssuntoSerializer()
    class Meta:
        model = Contato
        fields = ['id', 'nome','sobrenome', 'email']

class CreateContatoViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  serializer_class = CreateContatoSerializer   
  queryset = Contato.objects.all()


# Serializers define the API representation.
class DoadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doador
        fields = ['id', 'nome','sobrenome', 'email']

class DoadorDetailsViewSet(ViewSet):
  serializer_class = DoadorSerializer
  permission_classes = [IsAuthenticated]
  @staticmethod
  def list(request: Request) -> Response:
    doador = Doador.objects.filter(user = request.user)[0]
    serializer = DoadorSerializer(doador, many=False)
    return Response(serializer.data)  


#### Pedidos, Carrinho de compras ###########
class ItemSerializer(serializers.ModelSerializer):
    produto: ProdutoSerializer()
    class Meta:
        model = Item
        depth = 2
        fields = ['id', 'preco', 'produto', 'quantidade']

class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemSerializer(many=True)
    class Meta:
        model = Pedido
        depth = 2
        fields = ['id', 'finalizado', 'valorTotal', 'itens']

class PedidoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PedidoSerializer      
    def get_queryset(self):
      #filtra apenas os pedidos do usuário logado
      return Pedido.objects.filter(doador = Doador.objects.filter(user = self.request.user)[0])    

class CreateItemSerializer(serializers.ModelSerializer):
    produto: ProdutoSerializer()
    class Meta:
        model = Item
        fields = ['id', 'produto', 'pedido']

class CreateItemPedidoViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
  serializer_class = CreateItemSerializer   
  queryset = Item.objects.all()

  def perform_create(self, serializer):
    #procura o pedido aberto
    pedidosAbertos = Pedido.objects.filter(finalizado = False, doador = Doador.objects.filter(user = self.request.user)[0])    
    if(len(pedidosAbertos) > 0):
      pedidoAberto = pedidosAbertos[0]
    else:
      #caso nao exista um pedido aberto ele cria um
      pedidoAberto = Pedido.objects.create(doador = Doador.objects.filter(user = self.request.user)[0], finalizado = False)

    #itensExistente = list(Item.objects.filter(produto=serializer.data['produto'], pedido=pedidoAberto))
    #if len(itensExistente) > 0:
    #  itensExistente[0].quantidade = itensExistente[0].quantidade + 1
    #  itensExistente[0].save()
    #else:
    serializer.save(pedido = pedidoAberto) 
#################  


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'password',
        ]

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance

class UserRegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  serializer_class = UserRegistrationSerializer  



class LoginViewSet(ViewSet):
  @staticmethod
  def create(request: Request) -> Response:
      user = authenticate(
          username=request.data.get('username'),
          password=request.data.get('password'))

      if user is not None:
        login(request, user)
        return JsonResponse({"id": user.id, "username": user.username})
      else:
        return JsonResponse(
            {"detail": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')

class UserDetailsViewSet(ViewSet):
  serializer_class = UserDetailsSerializer
  permission_classes = [IsAuthenticated]
  @staticmethod
  def list(request: Request) -> Response:
    content = {'not_done': 1}
    print(request.user)
    print(content)
    serializer = UserDetailsSerializer(request.user, many=False)
    #return 
    return Response(serializer.data)


class LogoutViewSet(ViewSet):
  permission_classes = [IsAuthenticated]
  @staticmethod
  def list(request: Request) -> Response:
    logout(request)
    content = {'logout': 1}
    return Response(content)    

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'duvidas', DuvidaViewSet)
router.register(r'instituicoes', InstituicaoViewSet)
router.register(r'doadores-create', CreateDoadorViewSet)
router.register(r'contatos-create', CreateContatoViewSet)
router.register(r'assuntos', AssuntoViewSet)
router.register(r'pedidos', PedidoViewSet, basename='Pedidos')
router.register(r'item-pedido-create', CreateItemPedidoViewSet)
router.register(r'currentuser', UserDetailsViewSet, basename="Currentuser")
router.register(r'currentdoador', DoadorDetailsViewSet, basename="Doadorusuario")
router.register(r'login', LoginViewSet, basename="Login")
router.register(r'logout', LogoutViewSet, basename="Logout")
router.register(r'user-registration', UserRegistrationViewSet, basename="User")
  