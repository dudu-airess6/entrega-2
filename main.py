from auth_service import AuthService

def demonstrar_autenticacao_segura():
    print("=== ENTREGA 2: DEMONSTRAÇÃO DE HASH E AUTENTICAÇÃO SEGURA ===")
    
    auth = AuthService()

    print("\n[1] Cadastrando usuários no sistema...")
    auth.cadastrar_usuario("eduardo", "SenhaForte@2026")
    auth.cadastrar_usuario("gustavo", "SegurancaInovacao!88")
    print("✓ Usuários cadastrados com sucesso!")

    print("\n[2] Evidência do Armazenamento Protegido (Salt + Hash):")
    reg_eduardo = auth.obter_registro_protegido("eduardo")
    print(f" - Usuário: {reg_eduardo['username']}")
    print(f" - Salt (Hex 16 bytes): {reg_eduardo['salt_hex']}")
    print(f" - Hash Derivado (scrypt 256 bits): {reg_eduardo['hash_hex']}")

    print("\n[3] Teste de Autenticação (Senha Correta):")
    sucesso = auth.autenticar_usuario("eduardo", "SenhaForte@2026")
    if sucesso:
        print("✓ Autenticação BEM-SUCEDIDA! Credenciais válidas.")
    else:
        print("❌ Falha na autenticação.")

    print("\n[4] Teste de Autenticação (Senha Incorreta):")
    falha_senha = auth.autenticar_usuario("eduardo", "SenhaIncorreta123")
    if not falha_senha:
        print("✓ Rejeição CORRETA! Senha incorreta bloqueada pelo sistema.")
    else:
        print("❌ ERRO DE SEGURANÇA: Senha incorreta foi aceita!")

    print("\n[5] Teste de Autenticação (Usuário Inexistente):")
    falha_usuario = auth.autenticar_usuario("usuario_fantasma", "SenhaQualquer")
    if not falha_usuario:
        print("✓ Rejeição CORRETA! Usuário não encontrado no sistema.")

if __name__ == "__main__":
    demonstrar_autenticacao_segura()
