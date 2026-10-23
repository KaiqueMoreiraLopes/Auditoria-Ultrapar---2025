"""Testes didáticos reproduzíveis para a base sintética. Não constituem auditoria da Ultrapar."""
import pandas as pd, gzip, os
p=os.path.join(os.path.dirname(__file__),"..","base_sintetica","imobilizado_sintetico_500k.csv.gz")
df=pd.read_csv(p,compression="gzip")
print("Linhas:",len(df)); print("IDs únicos:",df.registro_id.nunique())
print("Vida útil inválida:",(df.vida_util_anos_sintetica<=0).sum())
print("Depreciação > custo:",(df["depreciacao_acumulada_sintetica_R$"] > df["custo_bruto_sintetico_R$"]).sum())
print("Registros com status de exceção:",(df.status_teste!="NORMAL").sum())
print("Valor líquido sintético total R$:",df["valor_contabil_liquido_sintetico_R$"].sum())
