import os
import json
from openai import OpenAI

# Inicializa o cliente da OpenAI pegando a chave segura do GitHub
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Lista de clínicas de exemplo para prospecção (Nicho: Estética)
clinicas_alvo = [
    {"nome": "Estética Advanced", "instagram": "@estetica_advanced", "site_atual": "Não possui"},
    {"nome": "Clínica Bella Pele", "instagram": "@bellapele_estetica", "site_atual": "http://bellapeleantigo.com.br"},
    {"nome": "Viver Bem Estética", "instagram": "@viverbem_sp", "site_atual": "Não possui"}
]

def analisar_clinica(clinica):
    print(f"\n[Robó] Analisando {clinica['nome']} ({clinica['instagram']})...")
    
    prompt = f"""
    Você é um especialista em marketing digital e estruturação de negócios.
    Analise o seguinte lead de clínica de estética para criar uma proposta de site personalizado:
    Nome: {clinica['nome']}
    Instagram: {clinica['instagram']}
    Site Atual: {clinica['site_atual']}
    
    Gere um relatório rápido em JSON contendo:
    1. "pontos_fracos": O que eles estão perdendo comercialmente por não ter um site moderno.
    2. "proposta_valor": Uma ideia central de site focada em conversão para esta clínica.
    3. "paleta_cores": 3 cores hexadecimais sugeridas com base no nome/nicho para usarmos no design.
    
    Responda APENAS o JSON puro, sem formatações markdown (sem ```json).
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        resultado = response.choices[0].message.content.strip()
        return json.loads(resultado)
    except Exception as e:
        print(f"Erro ao analisar com GPT-4o mini: {e}")
        return None

# Executa a varredura e salva os dados mapeados para o Script 2 usar
dados_prospeccao = []

for item in clinicas_alvo:
    analise = analisar_clinica(item)
    if analise:
        item["analise_ia"] = analise
        dados_prospeccao.append(item)

# Salva o relatório de leads qualificados para o próximo passo do fluxo
with open("leads_qualificados.json", "w", encoding="utf-8") as f:
    json.dump(dados_prospeccao, f, indent=4, ensure_ascii=False)

print("\n[Sucesso] Varredura concluída! Arquivo leads_qualificados.json gerado.")
