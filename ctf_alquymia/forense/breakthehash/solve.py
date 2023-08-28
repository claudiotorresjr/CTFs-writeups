
import hashlib

# Hash fornecida
given_hash = "48bb6e862e54f2a795ffc4e541caed4dk"

# Função para gerar um hash com um caractere faltando
def generate_hash_with_missing_char(input_str, missing_index):
    return hashlib.md5(input_str[:missing_index] + input_str[missing_index+1:]).hexdigest()

# Tamanho da hash original
hash_length = len(given_hash)

# Testar todas as combinações de caracteres faltantes
for missing_index in range(hash_length):
    generated_hash = generate_hash_with_missing_char(given_hash, missing_index)
    if generated_hash == given_hash:
        missing_char = given_hash[missing_index]
        print("Caractere faltando:", missing_char)
        break