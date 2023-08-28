import sqlite3

# Conectando ao arquivo do banco de dados
conn = sqlite3.connect('/home/claudio/Documents/ctf_alquymia/forense/validacaodedados/bd.db')
cursor = conn.cursor()

sql_query = """SELECT * FROM users;"""

cursor.execute(sql_query)

names = list(map(lambda x: x[0], cursor.description))
resultados = cursor.fetchall()

print(names)
emails = {}
hashes = {}
for linha in resultados:
	if ('@' in linha[5] and linha[5] in emails):
		emails[linha[5]] += 1
	elif ('@' in linha[5] and linha[5] not in emails):
		emails[linha[5]] = 1
	
	if (len(linha[4]) == 36 and linha[4] in hashes):
		hashes[linha[4]] += 1
	elif (len(linha[4]) == 36 and linha[4] not in hashes):
		hashes[linha[4]] = 1


print(f"Total de registros: {len(resultados)}")
print(f"Total de emails: {len(emails)}")
print(f"Total de hashes: {len(hashes)}")

conn.close()