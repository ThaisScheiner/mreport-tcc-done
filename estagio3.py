# estagio3
import spacy
import os
from utilitario import Utilitario

# faz a extração automática de entidades nomeadas usando a biblioteca spaCy, 
# a partir de arquivos .txt em um diretório, e salva os resultados como texto e em um relatório .json

nlp = spacy.load("en_core_web_sm")
ents_dir = "C:/Temp/ents"
os.makedirs(ents_dir, exist_ok=True)

tokenize_dir = "C:/Temp/tokenize"
arquivos = os.listdir(tokenize_dir)
resultado_final = {}

for arquivo in arquivos:
    if not arquivo.endswith(".txt"):
        continue
    with open(os.path.join(tokenize_dir, arquivo), "r", encoding="utf-8") as f:
        saida = []
        for linha in f:
            doc = nlp(linha)
            for ent in doc.ents:
                if str(ent) not in saida:
                    saida.append(str(ent))
    with open(os.path.join(ents_dir, arquivo), "w", encoding="utf-8") as w:
        w.write(",".join(saida))
    resultado_final[arquivo] = saida

Utilitario.salvar("3", resultado_final, "relatorio.json")
print("[OK] Entidades extraídas e salvas.")
