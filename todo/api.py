
from todo.models import Duvida, Instituicao, Produto, Doador

from rest_framework import routers, serializers, viewsets, mixins

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
        fields = ['id', 'nome', 'descricao', 'sobre','produtos']

# ViewSets define the view behavior.
class InstituicaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instituicao.objects.all()
    serializer_class = InstituicaoSerializer

#Cadastro
class CreateDoadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doador
        fields = ['id', 'nome','sobrenome', 'email', 'data', 'senha']

class CreateDoadorViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  serializer_class = CreateDoadorSerializer   
  queryset = Doador.objects.all()

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'duvidas', DuvidaViewSet)
router.register(r'instituicoes', InstituicaoViewSet)
router.register(r'doadores-create', CreateDoadorViewSet)