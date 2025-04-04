import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

def extrair_texto_imagem(caminho_imagem):
    # Configuração do cliente (substitua do ambiente)
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
    
    cliente = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))
    
    with open(caminho_imagem, "rb") as arquivo:
        poller = cliente.begin_analyze_document("prebuilt-read", arquivo)
        resultado = poller.result()
    
    texto_extraido = ""
    for pagina in resultado.pages:
        for linha in pagina.lines:
            texto_extraido += linha.content + "\n"
    
    return texto_extraido

def salvar_resultado(texto, caminho_saida):
    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)

if __name__ == "__main__":
   
    for arquivo in os.listdir("../inputs"):
        if arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
            caminho_entrada = os.path.join("../inputs", arquivo)
            caminho_saida = os.path.join("../outputs", f"{os.path.splitext(arquivo)[0]}.txt")
            
            texto = extrair_texto_imagem(caminho_entrada)
            salvar_resultado(texto, caminho_saida)
            print(f"Processado: {arquivo} → {caminho_saida}")
