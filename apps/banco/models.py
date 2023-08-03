# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AmostraFoto(models.Model):
    id_amostra = models.CharField(max_length=36, blank=True, null=True)
    id_foto = models.CharField(max_length=25, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    caminho = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amostra_foto'


class Amostras(models.Model):
    id_amostra = models.CharField(max_length=36)
    dt_amostra = models.DateTimeField(blank=True, null=True)
    id_sensor = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dt_auditoria = models.DateTimeField(blank=True, null=True)
    auditor = models.IntegerField(blank=True, null=True)
    id_localizacao = models.CharField(max_length=36, blank=True, null=True)
    id_cliente = models.IntegerField(blank=True, null=True)
    downloaded = models.BooleanField(blank=True, null=True)
    deletado = models.BooleanField(blank=True, null=True)
    classificacao = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    confianca = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    auditoria = models.CharField(max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    seq = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    lat = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    usuario_coleta = models.IntegerField(blank=True, null=True)
    obs = models.CharField(max_length=4000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    classificacao_original = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    obs_admin = models.CharField(max_length=5000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    endereco = models.CharField(max_length=2000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    fit = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    chave_externa = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    precisao = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    dt_upload = models.DateTimeField(blank=True, null=True)
    classificacao_matlab = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    classificacao_1 = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    classificacao_2 = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    classificador_1 = models.IntegerField(blank=True, null=True)
    classificador_2 = models.IntegerField(blank=True, null=True)
    vista = models.BooleanField(blank=True, null=True)
    review = models.BooleanField(blank=True, null=True)
    id_usuario_review = models.IntegerField(blank=True, null=True)
    dt_review = models.DateTimeField(blank=True, null=True)
    dt_vista = models.DateTimeField(blank=True, null=True)
    id_usuario_vista = models.IntegerField(blank=True, null=True)
    classificador = models.IntegerField(blank=True, null=True)
    dt_classificacao = models.DateTimeField(blank=True, null=True)
    classificacao_temp = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    classificacao_original_temp = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    pressao = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    classificacao_cliente = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dt_classificacao_cliente = models.DateTimeField(blank=True, null=True)
    id_usuario_cliente_classificador = models.IntegerField(blank=True, null=True)
    obs_app = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    id_usuario = models.IntegerField(blank=True, null=True)
    classificacao_api = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    retorno_api = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    fit_api = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    confianca_api = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    vista_discordo = models.BooleanField(blank=True, null=True)
    token = models.CharField(max_length=36, blank=True, null=True)
    coletor = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    inspecao = models.BooleanField(blank=True, null=True)
    dt_inspecao = models.DateTimeField(blank=True, null=True)
    ruido_api = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    espec = models.BooleanField(blank=True, null=True)
    classificacao_br = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    predicao = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    decisao = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    id_inspecionar = models.IntegerField(blank=True, null=True)
    id_inspecionar2 = models.IntegerField(blank=True, null=True)
    id_inspecionar3 = models.IntegerField(blank=True, null=True)
    url_image = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    pre_classificacao = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    v3 = models.BooleanField(blank=True, null=True)
    img = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amostras'


class BlobStorage(models.Model):
    filename = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    dt_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'blob_storage'


class ClassificacaoAmostra(models.Model):
    id_classificacao = models.IntegerField()
    id_amostra = models.CharField(max_length=64, db_collation='SQL_Latin1_General_CP1_CI_AS')
    classificacao = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')
    id_usuario = models.IntegerField()
    dt_classificacao = models.DateTimeField()
    qualidade_audio = models.IntegerField()
    certeza = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'classificacao_amostra'


class Classificacoes(models.Model):
    id_classificacao = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')
    descricao = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classificacoes'


class ClienteFilial(models.Model):
    id_cliente = models.IntegerField()
    id_filial = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cliente_filial'


class Clientes(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    razao_social = models.CharField(max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS')
    endereco = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    numero = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    complemento = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cidade = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    estado = models.CharField(max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cep = models.CharField(db_column='CEP', max_length=8, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    observacoes = models.CharField(max_length=2000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    contato = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    telefone = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    id_timezone = models.IntegerField(blank=True, null=True)
    matlab = models.BooleanField(blank=True, null=True)
    id_cliente_master = models.IntegerField(blank=True, null=True)
    lat = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    zoom = models.IntegerField(blank=True, null=True)
    cnpj = models.CharField(max_length=18, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    logo = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # This field type is a guess.
    ativo = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientes'


class DiametroTubulacao(models.Model):
    id_diametro = models.IntegerField()
    descricao = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ordem = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diametro_tubulacao'


class DistanciaPercorrida(models.Model):
    id_cliente = models.IntegerField()
    operador = models.IntegerField()
    data_hora = models.DateTimeField()
    distancia = models.FloatField()

    class Meta:
        managed = False
        db_table = 'distancia_percorrida'


class EquipamentoLocalizacao(models.Model):
    id_equipamento = models.IntegerField()
    descricao = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipamento_localizacao'


class EquipamentosRelatorio(models.Model):
    id_relatorio = models.IntegerField()
    id_equipamento = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'equipamentos_relatorio'


class Historico(models.Model):
    id_amostra = models.CharField(max_length=36, blank=True, null=True)
    data = models.DateTimeField()
    dados = models.CharField(max_length=4000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tipo_acao = models.SmallIntegerField(blank=True, null=True)
    id_usuario = models.IntegerField(blank=True, null=True)
    origem = models.SmallIntegerField(blank=True, null=True)
    id_cliente = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historico'


class HistoricoAmostras(models.Model):
    id_historico = models.CharField(max_length=36)
    id_amostra = models.CharField(max_length=36, blank=True, null=True)
    dt_alteracao = models.DateTimeField(blank=True, null=True)
    id_usuario = models.IntegerField(blank=True, null=True)
    classificacao = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historico_amostras'


class HistoricoAmostrasAuditoria(models.Model):
    id_historico = models.CharField(max_length=36)
    id_usuario = models.IntegerField(blank=True, null=True)
    dt_alteracao = models.DateTimeField(blank=True, null=True)
    classificacao = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    id_amostra = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historico_amostras_auditoria'


class HistoricoDescricao(models.Model):
    descricao = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'historico_descricao'


class HistoricoSensores(models.Model):
    id_historico = models.CharField(max_length=36)
    id_sensor = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    id_cliente = models.IntegerField(blank=True, null=True)
    observacao = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    data_registro = models.DateTimeField()
    amplificacao = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    ganho = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    tensao = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    fuel = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historico_sensores'


class Localizacoes(models.Model):
    id_localizacao = models.CharField(max_length=36)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    endereco = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    numero = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    complemento = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cidade = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    estado = models.CharField(max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    contato = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    id_sensor = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cep = models.CharField(db_column='CEP', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'localizacoes'


class LogAmostrasDupli(models.Model):
    id_amostra = models.CharField(max_length=36)
    id_cliente = models.IntegerField(blank=True, null=True)
    id_usuario = models.IntegerField(blank=True, null=True)
    seq = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    seq_new = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dt_ajuste = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_amostras_dupli'


class Ping(models.Model):
    id_ping = models.IntegerField()
    dt_ping = models.DateTimeField(blank=True, null=True)
    cod_status = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ping'


class PosicaoVazamento(models.Model):
    id_posicao = models.IntegerField()
    descricao = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posicao_vazamento'


class RelatorioAmostras(models.Model):
    id_relatorio = models.IntegerField()
    id_amostra = models.CharField(max_length=36)
    dt_delete = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relatorio_amostras'


class RelatorioFoto(models.Model):
    id_foto = models.CharField(max_length=36)
    id_relatorio = models.IntegerField(blank=True, null=True)
    dt_registro = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ext = models.CharField(max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relatorio_foto'


class RelatorioVazamento(models.Model):
    id_relatorio = models.AutoField(primary_key=True)
    dt_relatorio = models.DateTimeField(blank=True, null=True)
    dt_envio = models.DateTimeField(blank=True, null=True)
    token = models.CharField(max_length=36, blank=True, null=True)
    id_usuario = models.IntegerField(blank=True, null=True)
    id_status_relatorio = models.IntegerField(blank=True, null=True)
    id_usuario_aprovacao = models.IntegerField(blank=True, null=True)
    endereco = models.CharField(max_length=2000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    obs = models.CharField(max_length=5000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    obs_aprovacao = models.CharField(max_length=5000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    pressao = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    nro_hidrometro = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    diametro = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tipo_tubulacao = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    posicao = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tipo_vazamento = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dt_alteracao_status = models.DateTimeField(blank=True, null=True)
    equipamentos = models.CharField(max_length=5000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tipo_pavimentacao = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    obs_tipo_vazamento = models.CharField(max_length=5000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    nro_os = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    obs_inspecao = models.CharField(max_length=5000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dt_delete = models.DateTimeField(blank=True, null=True)
    latitude = models.CharField(max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    longitude = models.CharField(max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    numero = models.CharField(max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relatorio_vazamento'


class SalvadoresAguaDiario(models.Model):
    id_cliente = models.IntegerField(primary_key=True)  # The composite primary key (id_cliente, id_coletor, data) found, that is not supported. The first column is selected.
    id_coletor = models.IntegerField()
    data = models.DateField()
    tipo_salvador = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    coletas_realizadas = models.IntegerField(blank=True, null=True)
    fraudes_encontradas = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salvadores_agua_diario'
        unique_together = (('id_cliente', 'id_coletor', 'data'),)


class SalvadoresAguaTotal(models.Model):
    id_cliente = models.IntegerField(primary_key=True)  # The composite primary key (id_cliente, id_usuario, tipo_salvador) found, that is not supported. The first column is selected.
    id_usuario = models.IntegerField()
    tipo_salvador = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')
    metros_cubicos_salvos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_coletas = models.IntegerField(blank=True, null=True)
    total_fraudes = models.IntegerField(blank=True, null=True)
    total_pontos_nao_confirmados = models.IntegerField(blank=True, null=True)
    total_pontos_suspeitos_confirmados = models.IntegerField(blank=True, null=True)
    total_vazamento_rede = models.IntegerField(blank=True, null=True)
    total_vazamento_ramal = models.IntegerField(blank=True, null=True)
    ultima_atualizacao = models.DateTimeField()
    consecutividade_acuracia_mensal = models.IntegerField(blank=True, null=True)
    consecutividade_coletas_inspecao_mensal = models.IntegerField(blank=True, null=True)
    pontuacao_experiencia = models.IntegerField(blank=True, null=True)
    pontuacao_conquista = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salvadores_agua_total'
        unique_together = (('id_cliente', 'id_usuario', 'tipo_salvador'),)


class Sensores(models.Model):
    id_sensor = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')
    descricao = models.CharField(max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dt_cadastro = models.DateTimeField(blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)
    dt_desativacao = models.DateTimeField(blank=True, null=True)
    id_cliente = models.IntegerField(blank=True, null=True)
    observacao = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    id_tipo = models.IntegerField(blank=True, null=True)
    localizacao_atual = models.CharField(max_length=36, blank=True, null=True)
    amplificacao = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    ganho = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    tensao = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    fuel = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensores'


class Sequencias(models.Model):
    id_cliente = models.IntegerField()
    seq = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sequencias'


class StatusPing(models.Model):
    codigo = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS')
    descricao = models.CharField(max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status_ping'


class StatusRelatorioVazamento(models.Model):
    id_status_relatorio = models.IntegerField()
    descricao = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status_relatorio_vazamento'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)


class Tagamostra(models.Model):
    id_amostra = models.CharField(max_length=36)
    tag = models.CharField(max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'tagAmostra'


class Tags(models.Model):
    id_tag = models.CharField(max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')
    descricao = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'


class TempoAmostraClassificacao(models.Model):
    id_tempo_amostra = models.IntegerField()
    id_usuario = models.IntegerField()
    id_amostra = models.CharField(max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    tempo_init = models.DateTimeField()
    tempo_final = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tempo_amostra_classificacao'


class TimerBr(models.Model):
    id_timer_br = models.IntegerField()
    tempo_inicial = models.DateTimeField(blank=True, null=True)
    tempo_final = models.DateTimeField(blank=True, null=True)
    total = models.DecimalField(max_digits=16, decimal_places=9, blank=True, null=True)
    id_usuario = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timer_br'


class Timezones(models.Model):
    id_timezone = models.IntegerField()
    valor = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timezones'


class TipoImpacto(models.Model):
    pool = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    truck = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    water_tank = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_impacto'


class TipoPavimentacao(models.Model):
    id_tipo_pavimentacao = models.IntegerField()
    descricao = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_pavimentacao'


class TipoPressao(models.Model):
    pressao = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    ramal_metro_cubico = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    rede_metro_cubico = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_pressao'


class TipoRamalPressao(models.Model):
    valor = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_ramal_pressao'


class TipoTubulacao(models.Model):
    id_tipo_tubulacao = models.IntegerField()
    descricao = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_tubulacao'


class TipoUsuario(models.Model):
    id_tipo_usuario = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')
    descricao = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_usuario'


class TipoVazamento(models.Model):
    id_tipo_vazamento = models.IntegerField()
    descricao = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_vazamento'


class TiposRota(models.Model):
    id_tipo = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS')
    descricao = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_rota'


class TiposSensor(models.Model):
    id_tipo = models.IntegerField()
    descricao = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_sensor'


class TokenPwd(models.Model):
    id_token = models.CharField(max_length=36)
    id_usuario = models.IntegerField(blank=True, null=True)
    dt_token = models.DateTimeField(blank=True, null=True)
    dt_validade = models.DateTimeField(blank=True, null=True)
    usado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'token_pwd'


class Tokens(models.Model):
    id_token = models.CharField(max_length=36)
    dt_last_update = models.DateTimeField(blank=True, null=True)
    id_usuario = models.IntegerField(blank=True, null=True)
    id_cliente = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tokens'


class UsuarioCliente(models.Model):
    id_usuario = models.IntegerField()
    id_cliente = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'usuario_cliente'


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    email = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')
    senha = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    nome = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    telefone = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    id_cliente = models.IntegerField(blank=True, null=True)
    administrador = models.BooleanField(blank=True, null=True)
    administrador_cliente = models.BooleanField(blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)
    auditor = models.BooleanField(blank=True, null=True)
    id_tipo_usuario = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    gerar_senha = models.BooleanField(blank=True, null=True)
    exibir_inspecao = models.BooleanField(blank=True, null=True)
    id_mail_chimp = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tour = models.BooleanField(blank=True, null=True)
    master = models.BooleanField(blank=True, null=True)
    operacao = models.BooleanField(blank=True, null=True)
    funcao_dupla = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'
