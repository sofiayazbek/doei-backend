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
from todo.models import Duvida, Instituicao, Produto, Doador, Contato, Assunto


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
    serializer.save(user = self.request.user


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
        fields = ['id', 'nome', 'email', 'telefone', 'mensagem', 'assunto']

class CreateContatoViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  serializer_class = CreateContatoSerializer   
  queryset = Contato.objects.all()


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
        return JsonResponse({"detail": "Success"})
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
router.register(r'currentuser', UserDetailsViewSet, basename="Currentuser")
router.register(r'login', LoginViewSet, basename="Login")
router.register(r'logout', LogoutViewSet, basename="Logout")
router.register(r'user-registration', UserRegistrationViewSet, basename="User")
  