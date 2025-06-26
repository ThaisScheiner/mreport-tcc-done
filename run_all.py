import subprocess

estagios = [
    ("ESTÁGIO 0", "estagio0.py"),
    ("ESTÁGIO 1", "estagio1.py"),
    ("ESTÁGIO 2", "estagio2.py"),
    ("ESTÁGIO 3", "estagio3.py"),
    ("ESTÁGIO 4", "estagio4.py"),
    ("ESTÁGIO tokenize", "estagio_tokenize.py"),
    ("ESTÁGIO 5", "estagio5.py"),
    ("ESTÁGIO 6", "estagio6.py"),
]

print("\n===== EXECUTANDO TODOS OS ESTÁGIOS =====\n")

for nome, arquivo in estagios:
    print(f"\n===== {nome} =====\n")
    subprocess.run(["python", arquivo], check=True)

print("\nTODOS OS ESTÁGIOS CONCLUÍDOS COM SUCESSO!\n")
