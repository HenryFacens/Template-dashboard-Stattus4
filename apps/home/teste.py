from apps.banco.models_sql_server import Amostras

def print_first_five():
    try:
        # Tentamos pegar os cinco primeiros objetos do banco de dados
        first_five_objects = Amostras.objects.using('sql_server').all()[:5]

        if len(first_five_objects) != 0:
            for obj in first_five_objects:
                print(f"ID da Amostra: {obj.id_amostra}, Data da Amostra: {obj.dt_amostra}")
        else:
            print("A tabela está vazia.")

    except Exception as e:
        print("Erro ao acessar os dados da tabela 'Amostras'.")
        print("Detalhes do erro:", e)
