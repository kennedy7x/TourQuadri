# 🏍️ TourQuadri

Sistema web de agendamento de passeios de quadriciclo em Campos do Jordão - SP.

---

## 📖 Sobre o Projeto

O **TourQuadri** é uma aplicação web completa para gerenciamento de passeios turísticos de quadriciclo. O sistema permite que clientes agendem passeios, escolham roteiros e máquinas, e o administrador gerencia toda a operação (agendamentos, máquinas, roteiros, horários e clientes).

### ✨ Funcionalidades Principais

- **Para Clientes:**
  - Cadastro com verificação de email
  - Agendamento de passeios (data, horário, roteiro e máquinas)
  - Visualização de roteiros e máquinas disponíveis
  - Gerenciamento dos próprios agendamentos
  - Dashboard pessoal com estatísticas e gráficos
  - **Programa de Fidelidade:** a cada 5 passeios, ganha 20% de desconto no próximo

- **Para Administradores:**
  - Painel administrativo completo
  - Gerenciamento de agendamentos (iniciar, finalizar, cancelar, editar)
  - Gerenciamento de máquinas e roteiros
  - Bloqueio de horários e datas
  - Visão geral com gráficos (agendamentos por dia, roteiros, horários, máquinas)
  - Exportação de relatórios em PDF
  - Sistema de logs de todas as ações administrativas
  - Envio de lembretes por email

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.10+, Flask 3.1
- **Banco de Dados:** SQLite + SQLAlchemy
- **Autenticação:** Flask-Bcrypt (senhas criptografadas)
- **Emails:** Flask-Mail (SMTP Gmail)
- **Formulários:** Flask-WTF (proteção CSRF)
- **Relatórios:** ReportLab (PDF)
- **Frontend:** HTML5, CSS3, JavaScript puro
- **Gráficos:** Chart.js
- **Agendador:** APScheduler (email pós-passeio)

---

## 📋 Requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes)
- Conta Gmail com senha de app (para envio de emails)

---

## 🚀 Como Rodar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/tourquadri.git
cd tourquadri

2. Crie e ative o ambiente virtual
Windows (PowerShell):

powershell
python -m venv venv
venv\Scripts\Activate.ps1
Linux/Mac:

bash
python3 -m venv venv
source venv/bin/activate
⚠️ Se o PowerShell bloquear, rode antes:

powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
3. Instale as dependências
bash
pip install -r requirements.txt
4. Configure o arquivo .env
Crie um arquivo .env na raiz do projeto com:

env
SECRET_KEY=sua_chave_secreta_aqui
ADMIN_EMAIL=tourquadri@gmail.com

MAIL_USERNAME=tourquadri@gmail.com
MAIL_PASSWORD=sua_senha_de_app_do_gmail

GOOGLE_REVIEW_LINK=https://g.page/r/SEU_PLACE_ID/review
Como gerar a senha de app do Gmail:

Ative a verificação em duas etapas: https://myaccount.google.com/security

Gere uma senha de app: https://myaccount.google.com/apppasswords

Cole os 16 caracteres no MAIL_PASSWORD

5. Rode a aplicação
bash
python app.py
Acesse no navegador: http://127.0.0.1:5000

🔐 Credenciais Padrão
Ao rodar pela primeira vez, o sistema cria automaticamente:

Admin: tourquadri@gmail.com / senha: admin123

15 máquinas padrão (IDs 0 a 14)

8 roteiros configurados

⚠️ Troque a senha do admin após o primeiro login!

📁 Estrutura do Projeto
text
TourQuadri/
├── app.py                          # Arquivo principal
├── requirements.txt                # Dependências
├── .env                            # Variáveis de ambiente (não subir no Git)
├── .gitignore                      # Arquivos ignorados pelo Git
├── instance/
│   └── tourquadri.db               # Banco de dados SQLite
└── tourquadri/
    ├── __init__.py                 # Factory da aplicação
    ├── models.py                   # Modelos do banco (Usuario, Agendamento, etc.)
    ├── services.py                 # Lógica de negócio
    ├── scheduler.py                # Agendador de emails em background
    ├── decorators.py               # Decorators (@login_required, @admin_required)
    ├── controllers/                # Controllers (rotas)
    │   ├── __init__.py
    │   ├── auth_controller.py
    │   ├── usuario_controller.py
    │   ├── agendamento_controller.py
    │   ├── admin_controller.py
    │   └── roteiro_controller.py
    ├── templates/                  # Templates HTML
    │   ├── base.html
    │   ├── navbar.html
    │   ├── geral/
    │   ├── adm/
    │   └── forms/
    └── static/
        ├── css/
        │   ├── style.css
        │   └── landing.css
        ├── js/
        │   ├── scripts.js
        │   ├── dashboard_admin.js
        │   └── dashboard_cliente.js
        └── images/
            ├── maquinas/
            └── roteiros/
🎯 Principais Rotas
Públicas
Rota	Descrição
/	Landing page
/login	Página de login
/register	Cadastro de cliente
/esqueci_senha	Recuperação de senha
Cliente
Rota	Descrição
/dashboard	Dashboard com agendamento
/meus_agendamentos	Lista dos próprios agendamentos
/conta	Dados da conta
/minhas_estatisticas	Gráficos pessoais
/minha_fidelidade	Programa de fidelidade
/roteiros	Lista de roteiros
/maquinas	Lista de máquinas
Admin
Rota	Descrição
/admin	Painel administrativo
/admin/agendamentos	Gerenciar agendamentos
/admin/maquinas	Gerenciar máquinas
/admin/roteiros	Gerenciar roteiros
/admin/gerenciar_horarios	Bloquear/desbloquear horários
/admin/visao_geral	Gráficos e estatísticas
/admin/logs	Histórico de ações
API
Rota	Descrição
/api/verificar_maquinas	Verifica disponibilidade de máquinas
/api/verificar_bloqueios	Verifica bloqueios de horário
/api/dashboard_cliente	Dados dos gráficos do cliente
/api/dashboard_admin	Dados dos gráficos do admin
🔄 Como Funciona
Agendamento
Cliente escolhe data, horário, roteiro e máquinas

Sistema verifica disponibilidade em tempo real

Máquinas ocupadas ficam bloqueadas por todo o período do passeio

Agendamento criado com status agendado

Passeio
Admin inicia o passeio → status em_andamento

Admin finaliza o passeio → status finalizado

30 min depois da finalização, cliente recebe email pedindo avaliação no Google

Programa de Fidelidade
Cada passeio finalizado soma +1 no contador do cliente

Ao atingir 5 passeios → desconto de 20% liberado

Cliente aplica o desconto no próximo agendamento

Após usar → contador zera

Se cancelar o agendamento com desconto → desconto volta a ficar disponível

🗄️ Banco de Dados
Modelos principais:

Usuario: nome, email, telefone, senha (bcrypt), admin, email_verificado, passeios_realizados, desconto_disponivel

Maquina: nome_maquina, modelo, cc

Agendamento: data, horário, cliente, máquinas (JSON), roteiro, status, desconto_aplicado

Bloqueio: data + horário bloqueado pelo admin

EstatisticaMaquina: contador de uso por máquina

CodigoVerificacao: códigos de verificação (cadastro e recuperação de senha)

LogAdmin: histórico de ações administrativas

📊 Gráficos
Admin (/admin/visao_geral):

Agendamentos nos últimos 30 dias

Roteiros mais procurados

Horários mais procurados

Top 10 máquinas mais usadas

Cliente (/minhas_estatisticas):

Passeios por mês (últimos 6 meses)

Roteiros que mais fez

Status dos passeios

📧 Configuração de Emails
O sistema envia 3 tipos de email:

Confirmação de cadastro — código de 6 dígitos

Recuperação de senha — código de 6 dígitos

Pós-passeio — link para avaliação no Google (30 min após finalizar)

Para funcionar, precisa configurar a Senha de App do Gmail no .env.

🎨 Personalização
Cores da marca: #2563eb (azul) e #f4a261 (laranja)

Roteiros: editáveis em tourquadri/models.py (dicionário ROTEIROS)

Máquinas padrão: definidas em tourquadri/__init__.py (função _criar_maquinas_padrao)

⚠️ Observações
O projeto usa SQLite (bom para desenvolvimento, mas para produção recomenda-se PostgreSQL)

Emails só funcionam com a senha de app do Gmail configurada

O link do Google Reviews precisa ser configurado no .env

Imagens de máquinas e roteiros devem ser colocadas em static/images/

📝 Licença
Projeto acadêmico desenvolvido para a disciplina de Programação Web Dinâmica e Programação Orientada a Objetos com Serviços.

👨‍💻 Autor
Desenvolvido por Kennedy Vieira Teixeira