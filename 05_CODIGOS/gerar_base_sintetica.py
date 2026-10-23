#!/usr/bin/env python3
"""Gera base didática sintética para o PT 530/PT 500. Não contém registros reais."""
import csv,gzip,random,os
N=500_000; TARGET=14_095_791_000; SEED=20261023
rng=random.Random(SEED)
weights=[rng.lognormvariate(7.0,1.05) for _ in range(N)]
scale=TARGET/sum(weights); vals=[max(1,int(w*scale)) for w in weights]
diff=TARGET-sum(vals); i=0
while diff:
 j=(i*7919)%N
 if diff>0: vals[j]+=1; diff-=1
 elif vals[j]>1: vals[j]-=1; diff+=1
 i+=1
categories=["Equipamentos e instalações para distribuição de combustíveis","Tanques e vasilhames para GLP","Máquinas e equipamentos","Edificações","Veículos","Empurradores, barcaças e navios","Equipamentos de informática","Obras em andamento","Benfeitorias em imóveis de terceiros","Móveis e utensílios"]
locations=["Ipiranga","Ultragaz","Ultracargo","Hidrovias do Brasil","Holding e demais"]
sites=["BR-SP-01","BR-SP-02","BR-RJ-01","BR-MG-01","BR-PA-01","BR-MS-01","BR-BA-01","BR-PR-01","BR-GO-01","BR-AM-01"]
exceptions={137,1802,12345,98765,123456,234567,345678,456789,499999}
out=os.path.join(os.path.dirname(__file__),"..","base_sintetica","imobilizado_sintetico_500k.csv.gz")
os.makedirs(os.path.dirname(out),exist_ok=True)
with gzip.open(out,"wt",encoding="utf-8",newline="") as f:
 w=csv.writer(f); w.writerow(["registro_id","data_aquisicao","componente_sintetico","unidade_sintetica","local_sintetico","custo_bruto_sintetico_R$","depreciacao_acumulada_sintetica_R$","valor_contabil_liquido_sintetico_R$","vida_util_anos_sintetica","status_teste","observacao"])
 for i,v in enumerate(vals):
  gross=max(v,int(v/(0.35+(i%60)/100))); dep=gross-v; life=[5,8,10,15,20,25,30,40][i%8]; status="NORMAL"; obs="Sintético; não corresponde a bem identificado da companhia."
  if i in exceptions:
   if i%3==0: status="EXCECAO_VIDA_UTIL"; life=0; obs="Exceção didática: vida útil inválida."
   elif i%3==1: status="EXCECAO_DEPRECIACAO"; dep=gross+100; v=gross-dep; obs="Exceção didática: depreciação supera custo bruto."
   else: status="EXCECAO_DOCUMENTACAO"; obs="Exceção didática: suporte documental ausente."
  year=2000+i%26; month=1+i%12; day=1+i%27
  w.writerow([f"SYN-{i+1:06d}",f"{year:04d}-{month:02d}-{day:02d}",categories[i%10],locations[(i*7)%5],sites[(i*3)%10],gross,dep,v,life,status,obs])
print(f"Gerada base com {N:,} registros. Soma inicial de valores líquidos alocados = R$ {TARGET:,}; confira diferenças decorrentes das exceções inseridas.")
