from app import create_app, db, bcrypt
from app.models import Usuario

app = create_app()

with app.app_context():
    print("Criando tabelas no banco de dados...")
    db.create_all()
    
    admin_email = 'admin@coloniaprev.com.br'
    admin_user = Usuario.query.filter_by(email=admin_email).first()
    
    if not admin_user:
        print(f"Criando usuário administrador padrão: {admin_email} / 123456")
        hashed_pw = bcrypt.generate_password_hash('123456').decode('utf-8')
        novo_admin = Usuario(
            nome='Administrador Geral',
            email=admin_email,
            senha=hashed_pw,
            tipo='admin'
        )
        db.session.add(novo_admin)
        db.session.commit()
        print("Administrador criado com sucesso!")
    else:
        print("Usuário administrador já existe.")
        
    print("Configuração concluída!")
