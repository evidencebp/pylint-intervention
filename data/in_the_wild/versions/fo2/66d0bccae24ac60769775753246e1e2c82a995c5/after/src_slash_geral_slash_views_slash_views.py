import datetime
import yaml
from pprint import pformat, pprint

import django.forms
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import HttpResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import View

from fo2.connections import db_cursor_so

from base.views import O2BaseGetPostView
from utils.functions.format import format_cnpj

from systextil.queries.tabela.deposito import query_deposito

import geral.forms as forms
from geral.dados.fluxo_roteiros import get_roteiros_de_fluxo
from geral.dados.fluxos import dict_fluxo
from geral.functions import (
    config_get_value,
    config_set_value,
    get_empresa,
)
from geral.models import (
    InformacaoModulo,
    Painel,
    PainelModulo,
    Pop,
    PopAssunto,
    UsuarioPainelModulo,
    UsuarioPopAssunto,
)


def index(request):
    if get_empresa(request) == 'agator':
        return render(request, 'geral/index_agator.html')
    else:
        return render(request, 'geral/index.html')


class PainelView(View):

    def get(self, request, *args, **kwargs):
        try:
            painel = Painel.objects.get(slug=kwargs['painel'], habilitado=True)
        except Painel.DoesNotExist:
            return redirect('apoio_ao_erp')

        ultimo_mes = timezone.now() - datetime.timedelta(days=61)

        layout = painel.layout
        config = yaml.load(layout, Loader=yaml.Loader)
        for dado in config['dados']:
            try:
                modulo = PainelModulo.objects.get(slug=dado['modulo'])
            except Exception:
                return redirect('apoio_ao_erp')

            if modulo.tipo == 'I':
                dado['modulo_nome'] = modulo.nome
                dado['dados'] = InformacaoModulo.objects.filter(
                    painel_modulo__slug=dado['modulo'],
                    habilitado=True,
                    data__gt=ultimo_mes,
                ).order_by('-data')

        context = {
            'titulo': painel.nome,
            'config': config,
            }
        return render(
            request, f"geral/{config['template']}.html", context)


class InformativoView(LoginRequiredMixin, View):
    Form_class = forms.InformacaoModuloForm
    template_name = 'geral/informativo.html'
    title_name = 'Informativos'
    context = {}
    informativo_id = None

    def list_informativo(self):
        self.context['informativos'] = InformacaoModulo.objects.filter(
            painel_modulo=self.modulo).order_by('-data')

    def tem_permissao(self, request, **kwargs):
        modulo_slug = kwargs['modulo']
        self.modulo = PainelModulo.objects.get(slug=modulo_slug)
        self.context = {
            'titulo': '{} - {}'.format(self.modulo.nome, self.title_name),
            'modulo_slug': modulo_slug,
            }

        verificacao = UsuarioPainelModulo.objects.filter(
            usuario=request.user, painel_modulo=self.modulo)
        if len(verificacao) == 0:
            self.context['msg_erro'] =\
                'Usuário não tem direito de manter o informativo "{}"'.format(
                    self.modulo.nome
                )
            return False
        return True

    def get_informativo_id(self, **kwargs):
        if 'id' in kwargs:
            self.informativo_id = kwargs['id']

    def get(self, request, *args, **kwargs):
        if not self.tem_permissao(request, **kwargs):
            return render(request, self.template_name, self.context)

        self.get_informativo_id(**kwargs)
        if self.informativo_id == 'add':
            form = self.Form_class()
            self.context['form'] = form
        else:
            informativo_por_id = InformacaoModulo.objects.filter(
                id=self.informativo_id)
            if len(informativo_por_id) == 0:
                self.list_informativo()
            else:
                self.context['informativo_id'] = self.informativo_id
                form = self.Form_class(
                    initial={'chamada': informativo_por_id[0].chamada,
                             'habilitado': informativo_por_id[0].habilitado})
                self.context['form'] = form

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        if not self.tem_permissao(request, **kwargs):
            return render(request, self.template_name, self.context)

        form = None
        self.get_informativo_id(**kwargs)
        if self.informativo_id == 'add':
            form = self.Form_class(request.POST)
        else:
            informativo_por_id = InformacaoModulo.objects.filter(
                id=self.informativo_id)
            if len(informativo_por_id) == 0:
                self.list_informativo()
            else:
                self.context['informativo_id'] = self.informativo_id
                form = self.Form_class(
                    request.POST,
                    initial={'chamada': informativo_por_id[0].chamada,
                             'habilitado': informativo_por_id[0].habilitado})

        if form is not None:
            if form.is_valid():
                chamada = form.cleaned_data['chamada']
                habilitado = form.cleaned_data['habilitado']
                if self.informativo_id == 'add':
                    informativo = InformacaoModulo(
                        usuario=request.user)
                else:
                    informativo = InformacaoModulo.objects.get(
                        id=self.informativo_id)
                informativo.chamada = chamada
                informativo.habilitado = habilitado
                informativo.painel_modulo = self.modulo
                informativo.save()
                self.list_informativo()
            else:
                self.context['form'] = form
        return render(request, self.template_name, self.context)


def gera_fluxo(request, destino, id):
    fluxo = dict_fluxo(id)
    if fluxo is None:
        return HttpResponse("Fluxo {} não encontrado".format(id))

    if destino in ['a', 'f']:
        filename = \
            'roteiros_alt{id}_{versao_num}_{versao_sufixo}' \
            '.dot'.format(**fluxo)
        templ = loader.get_template(fluxo['template_base'])
        http_resp = HttpResponse(
            templ.render(fluxo, request), content_type='text/plain')
        http_resp['Content-Disposition'] = \
            'attachment; filename="{filename}"'.format(filename=filename)
        return http_resp

    else:
        return render(
            request, fluxo['template_base'], fluxo,
            content_type='text/plain')


class ExecGeraFluxo(O2BaseGetPostView):
    def __init__(self, *args, **kwargs):
        super(ExecGeraFluxo, self).__init__(*args, **kwargs)
        self.Form_class = forms.ExecGeraFluxoForm
        self.template_name = 'geral/exec_gera_fluxo.html'
        self.title_name = 'Gera fluxo'
        self.get_args = ['destino', 'id']

    def mount_context(self):
        destino = self.form.cleaned_data['destino']
        id = self.form.cleaned_data['id']
        self.context.update({
            'destino': destino,
            'id': id,
        })
        fluxo = dict_fluxo(id)
        if fluxo is None:
            self.context.update({
                'erro': "Fluxo {} não encontrado".format(id),
            })


def roteiros_de_fluxo(request, id):
    roteiros = get_roteiros_de_fluxo(id)
    return HttpResponse(
        pformat(roteiros, indent=4),
        content_type='text/plain')


class Configuracao(PermissionRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        self.permission_required = 'geral.change_config'
        self.Form_class = forms.ConfigForm
        self.template_name = 'geral/config.html'
        self.title_name = 'Configuração'

    def get_values(self, request):
        values = {}
        for field in self.Form_class.field_param:
            param = self.Form_class.field_param[field]
            if request.user.is_superuser:
                values[field] = config_get_value(param)
            else:
                values[field] = config_get_value(param, request.user)
        return values

    def set_values(self, request, values):
        if request.user.is_superuser:
            usuario = None
        else:
            usuario = request.user
        ok = True
        for field in self.Form_class.field_param:
            param = self.Form_class.field_param[field]
            ok = ok and config_set_value(param, values[field], usuario=usuario)
        return ok

    def get(self, request, *args, **kwargs):
        context = {'titulo': self.title_name}
        form = self.Form_class()
        values = self.get_values(request)
        form.fields["op_unidade"].initial = values['op_unidade']
        form.fields["dias_alem_lead"].initial = values['dias_alem_lead']
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {'titulo': self.title_name}
        form = self.Form_class(request.POST)
        if form.is_valid():
            values = {}
            values['op_unidade'] = form.cleaned_data['op_unidade']
            values['dias_alem_lead'] = form.cleaned_data['dias_alem_lead']
            if self.set_values(request, values):
                context['msg'] = 'Valores salvos!'
            else:
                context['msg'] = 'Houve algum erro ao salvar os valores!'
        context['form'] = form
        return render(request, self.template_name, context)
