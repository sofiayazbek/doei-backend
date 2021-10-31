
from todo.models import Duvida, Instituicao

from rest_framework import routers, serializers, viewsets

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
class InstituicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituicao
        fields = ['id', 'nome', 'descricao']

# ViewSets define the view behavior.
class InstituicaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instituicao.objects.all()
    serializer_class = InstituicaoSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'duvidas', DuvidaViewSet)
router.register(r'instituicoes', InstituicaoViewSet)