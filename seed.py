from tourquadri import create_app, db
from tourquadri.models import Agendamento
from datetime import datetime, timedelta
import uuid
import random

app = create_app()

with app.app_context():
    roteiros = ['1', '2', '3', '4', '5', '6', '7', '8']
    horarios = ['09:00', '10:00', '11:00', '13:00', '14:00', '15:00', '16:00']
    nomes = ['João Silva', 'Maria Santos', 'Pedro Costa', 'Ana Lima', 'Carlos Souza',
             'Julia Alves', 'Rafael Pinto', 'Beatriz Rocha', 'Lucas Dias', 'Camila Reis']

    hoje = datetime.now().date()
    criados = 0

    for i in range(50):
        dias_atras = random.randint(0, 29)
        data = hoje - timedelta(days=dias_atras)

        num_maquinas = random.randint(1, 3)
        maquinas = random.sample(range(15), num_maquinas)

        status = random.choice(['agendado', 'agendado', 'finalizado', 'finalizado', 'cancelado'])

        ag = Agendamento(
            id=str(uuid.uuid4()),
            usuario=f"cliente{i}@teste.com",
            nome_usuario=random.choice(nomes),
            nome_cliente=random.choice(nomes),
            telefone_cliente="(11) 99999-9999",
            email_cliente=f"cliente{i}@teste.com",
            data=data.isoformat(),
            horario=random.choice(horarios),
            roteiro=random.choice(roteiros),
            duracao=60,
            data_criacao=datetime.now().isoformat(),
            status=status,
            criado_por_admin=False
        )
        ag.maquinas = maquinas
        db.session.add(ag)
        criados += 1

    db.session.commit()
    print(f"OK - {criados} agendamentos de teste criados!")