from django.contrib import admin

# Register your models here.
from .models import Item
from .models import Produto
from .models import Instituicao
from .models import Doador
from .models import Duvida
from .models import Cesta
from .models import Contato
from .models import Assunto

admin.site.register(Item)
admin.site.register(Produto)
admin.site.register(Instituicao)
admin.site.register(Doador)
admin.site.register(Duvida)
admin.site.register(Cesta)
admin.site.register(Contato)
admin.site.register(Assunto)