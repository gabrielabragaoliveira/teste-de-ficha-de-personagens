import os
import shutil
from google.colab import files

pasta_projeto = "creche_vi_streamlit"
pasta_fotos = f"{pasta_projeto}/fotos"

# Limpa tentativas anteriores
if os.path.exists(pasta_projeto):
    shutil.rmtree(pasta_projeto)
os.makedirs(pasta_fotos)

print("=========================================")
print("🚀 GERADOR DEFINITIVO PARA STREAMLIT 🚀")
print("=========================================")

# --- 1. UPLOAD DE FOTOS ---
print("\n📸 Selecione as fotos dos personagens no seu computador (se a janela não abrir, use o atalho Ctrl+Enter no teclado):")
try:
    uploaded = files.upload()
    for filename in uploaded.keys():
        shutil.move(filename, f"{pasta_fotos}/{filename}")
    print(f"✅ {len(uploaded)} fotos guardadas na pasta 'fotos'!")
except Exception as e:
    print("Nenhuma foto enviada.")

# --- 2. CRIANDO O APP.PY (O Cérebro do Streamlit) ---
app_code = """import streamlit as st
import pandas as pd
import urllib.parse
import os
import base64
import mimetypes
import unicodedata

# Configura a página para ocupar o ecrã todo
st.set_page_config(page_title="Creche da Vi - Compass", layout="wide")

# O Streamlit guarda os dados em cache para o site carregar super rápido
@st.cache_data(ttl=600)
def carregar_dados():
    sheet_id = "1u0l2XT5nEXKQc61cfGviOw4lD6RuMqn2iFjIZF2jCKk"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(url).fillna('')

df = carregar_dados()
pasta_fotos = "fotos"
arquivos_na_pasta = os.listdir(pasta_fotos) if os.path.exists(pasta_fotos) else []

def limpar_nome(texto):
    texto = str(texto).lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def embutir_foto(nome_personagem):
    if not arquivos_na_pasta: return None
    primeiro_nome = limpar_nome(nome_personagem).split()[0].replace('(', '').replace(')', '')
    for arquivo in arquivos_na_pasta:
        if primeiro_nome in limpar_nome(arquivo.rsplit('.', 1)[0]):
            caminho = f"{pasta_fotos}/{arquivo}"
            tipo_mime, _ = mimetypes.guess_type(caminho)
            if tipo_mime is None: tipo_mime = 'image/jpeg'
            with open(caminho, "rb") as f:
                b64 = base64.b64encode(f.read()).decode('utf-8')
                return f"data:{tipo_mime};base64,{b64}"
    return None

# Montando o visual do site em HTML/CSS para o Streamlit renderizar
html_content = '''
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f8; color: #333; margin: 0; padding: 20px; }
    h1 { text-align: center; font-size: 2.5rem; margin-bottom: 30px; color: #1a1a1a; }
    .compass-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }
    .card { background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); padding: 25px 20px; display: flex; flex-direction: column; align-items: center; transition: transform 0.2s ease-in-out; }
    .card:hover { transform: translateY(-5px); }
    .avatar-link { display: block; margin-bottom: 20px; transition: opacity 0.2s; }
    .avatar-link:hover { opacity: 0.8; }
    .avatar { width: 130px; height: 130px; border-radius: 50%; object-fit: cover; background-color: #e9ecef; border: 4px solid #f0f0f0; display: block; }
    .info { width: 100%; text-align: center; margin-bottom: 15px; }
    .info p { margin: 8px 0; font-size: 1.1rem; }
    .info strong { color: #000; }
    .summary { width: 100%; font-size: 0.95rem; color: #555; text-align: justify; line-height: 1.5; border-top: 1px solid #eee; padding-top: 15px; margin-top: auto; }
</style>
<h1>Creche da Vi<br>Character Compass</h1>
<div class="compass-container">
'''

for index, row in df.iterrows():
    nome = str(row.get('Nome', 'Desconhecido')).strip()
    apelido = str(row.get('Apelido', '')).strip()
    local = str(row.get('Local', '')).strip()
    ocupacao = str(row.get('Ocupação', '')).strip()
    resumo = str(row.get('Resumo', '')).strip()

    # Formata o nome para exibir o apelido se existir
    exibicao_nome = f"{nome} ({apelido})" if apelido and apelido != '-' else nome
    
    # O Streamlit cria a imagem embutida na memória apenas quando a página é aberta!
    foto_codigo = embutir_foto(nome)

    if not foto_codigo:
        nome_url = urllib.parse.quote(nome)
        foto_codigo = f"https://ui-avatars.com/api/?name={nome_url}&background=random&color=fff&size=150"

    html_content += f'''
        <div class="card">
            <a href="{foto_codigo}" target="_blank" class="avatar-link" title="Ver imagem de {nome}">
                <img class="avatar" src="{foto_codigo}" alt="Foto de {nome}" loading="lazy">
            </a>
            <div class="info">
                <p><strong>Nome:</strong> {exibicao_nome}</p>
                <p><strong>Local:</strong> {local}</p>
                <p><strong>Ocupação:</strong> {ocupacao}</p>
            </div>
            <p class="summary">{resumo}</p>
        </div>
    '''

html_content += "</div>"

# Injeta o HTML diretamente no Streamlit
st.markdown(html_content, unsafe_allow_html=True)
"""

with open(f"{pasta_projeto}/app.py", "w", encoding="utf-8") as file:
    file.write(app_code)

# --- 3. CRIANDO O REQUIREMENTS.TXT ---
# Este ficheiro avisa o Streamlit de quais ferramentas ele precisa instalar no servidor
with open(f"{pasta_projeto}/requirements.txt", "w", encoding="utf-8") as file:
    file.write("pandas\nstreamlit\n")

# --- 4. EXPORTAÇÃO ---
print("\n📦 A zipar o projeto perfeito para o Streamlit...")
shutil.make_archive(pasta_projeto, 'zip', pasta_projeto)

print("🚀 A iniciar a transferência do ficheiro ZIP...")
files.download(f"{pasta_projeto}.zip")
