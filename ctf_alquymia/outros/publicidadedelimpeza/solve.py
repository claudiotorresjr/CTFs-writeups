import base64

def decode_message(encoded_string, key):
	# Decodifica a string de base64
	decoded_bytes = base64.b64decode(encoded_string)
	decoded_string = decoded_bytes.decode('utf-8')

	# Converte a chave para bytes
	key_bytes = key.encode('utf-8')

	# Inicializa uma lista para armazenar o resultado da descriptografia
	decrypted_bytes = []

	# Aplica a operação XOR byte a byte
	for i in range(len(decoded_bytes)):
		decrypted_byte = decoded_bytes[i] ^ key_bytes[i % len(key_bytes)]
		decrypted_bytes.append(decrypted_byte)

	# Converte os bytes descriptografados de volta para uma string
	return bytes(decrypted_bytes).decode('utf-8')

messages = {
	"AH1hTw==": "A1048576",
	"K1onVyZdHA==": "C3",
	"JV8qAQ==": "L1",
	"KFQxXCpbOA==": "E5",
}

for message, key in messages.items():
	decoded_string = decode_message(message, key)
	print(decoded_string)

# inf0
# hidden_
# mation}
# ALQ{