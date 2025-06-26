# 🛡️ Malware Report Generator - MReport

Este projeto tem como objetivo automatizar o processamento de notícias relacionadas a ameaças digitais (malwares), realizar a **classificação automática por tipo de malware** com base em palavras-chave, e gerar **relatórios finais em formato PDF e JSON**.

---

## 📌 Objetivo do Projeto

- Automatizar o fluxo de processamento de arquivos `.pdf` contendo notícias e boletins sobre segurança cibernética.
- Extrair de forma inteligente o título e corpo de cada notícia.
- Classificar os textos conforme a presença de termos relacionados a malwares, como: `trojan`, `virus`, `exploit`, `ransomware`, entre outros.
- Gerar relatórios PDF padronizados com:
  - **Título da notícia**
  - **Classificações de malware encontradas**
  - **Corpo da notícia formatado**
  - Tudo isso com **estilo visual limpo e profissional**.

---

## 🧰 Tecnologias Utilizadas

| Tecnologia | Descrição |
|------------|-----------|
| `Python 3.12` | Linguagem principal do projeto |
| [`FPDF`](https://pyfpdf.github.io/fpdf2/) | Biblioteca de geração de PDFs |
| `Regex (re)` | Usado para extração e limpeza de dados |
| `JSON` | Armazenamento de resultados intermediários |
| `OS` | Leitura de arquivos locais e manipulação de diretórios |

---

## 📁 Estrutura de Pastas

mreport/
│
├── relatorios/
│ ├── relatorio_classificado.json # Resultado da classificação
│ ├── relatorio_final.pdf # PDF final com notícias e classificações
│ └── textos_finais/ # Arquivos .txt com notícias formatadas
│
├── estagio4.py # Geração de resumo geral por categoria
├── estagio5.py # Geração do relatório completo final
├── utilitario.py # Funções auxiliares (opcional)
├── estagio_tokenize.py # Tokenização (análise textual por página)
├── ...

---

## ⚙️ Funcionamento da Aplicação

### 🔍 1. Extração e Classificação

O script percorre todos os arquivos `.pdf` da pasta `relatorios/textos_finais/` e executa:

- Extração do **título** e do **corpo da notícia**;
- Limpeza dos textos com regex;
- Busca por **termos-chave de malwares**, agrupando por categorias como:
  - `Exploit`, `Trojan`, `Virus`, `Backdoor`, `Spyware`, etc.
- Armazena os resultados em um `relatorio_classificado.json`.

### 📝 2. Geração de PDF (Estágio 5)

A partir do JSON de classificações, o script `estagio5.py`:

- Cria um relatório visual com:
  - Título de cada notícia
  - Lista de classificações encontradas
  - Origem (nome do arquivo)
  - Corpo do texto completo
- Estilo aplicado no PDF:
  - `Título:` em **negrito preto**
  - `Classificações de Malware:` em **negrito azul**
  - Cada termo classificado é exibido em **preto** (sem bordas ou fundo)
  - Texto justificado e espaçado

---

## 🧪 Exemplo de Classificação

```json
{
  "pagina1.txt": {
    "classificacoes": [
      { "classificacao": "exploit", "categoria": "Exploit" },
      { "classificacao": "trojan", "categoria": "Trojan" }
    ]
  }
}
````
🖨️ Exemplo de Saída PDF
Cada notícia é impressa com o seguinte formato:

Título: Weekly Recap: New Trojan Variants Target Banking Systems

Classificações de Malware:
- trojan (Trojan)
- dropper (Trojan)

Origem: pagina12.txt

Texto:
Cybersecurity researchers discovered a new variant of Trojan malware...
✅ Requisitos
Python 3.10 ou superior

Instalar dependências com:

pip install fpdf
🚀 Como Executar
Coloque os arquivos .txt das notícias na pasta relatorios/textos_finais/.

Execute os scripts em ordem (opcionalmente):

python estagio4.py        # Gera relatorio_classificado.json
python estagio5.py        # Gera relatorio_final.pdf
