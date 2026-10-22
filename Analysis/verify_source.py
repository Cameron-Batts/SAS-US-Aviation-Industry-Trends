"""Recompute descriptive checks from the bundled SAS CSV exports."""
import csv, json, pathlib
root=pathlib.Path(__file__).resolve().parents[1]
def rows(n):return list(csv.DictReader(open(root/'Data'/('table_'+n+'.csv'),encoding='utf-8-sig')))
def num(v):
 v=v.strip().replace(',','').replace('$','');return None if v=='.' else float(v)
e=rows('ENPLANEMENTS');f=rows('FTES');d=rows('FINANCIALSDETAILED')
a={r['Date']:r for r in e}
metrics={'passenger_rows':len(e),'fte_rows':len(f),'tables':{n:len(rows(n)) for n in ['ENPLANEMENTS','FTES','FINANCIALSDETAILED','AIRLINEFINANCIALSALL','TOPAIRLINES']}}
for col in ['Domestic_Passengers','International_Passengers']:
 metrics[col]={'april_2019':num(a['04/01/2019'][col]),'april_2020':num(a['04/01/2020'][col]),'april_yoy_percent':(num(a['04/01/2020'][col])/num(a['04/01/2019'][col])-1)*100,'missing_months':[r['Date'] for r in e if num(r[col]) is None]}
metrics['fte_change_dec2019_oct2020_percent']=(num(f[-3]['U_S__FTEs'])/num(next(r for r in f if r['Date']=='12/01/2019')['U_S__FTEs'])-1)*100
rr=next(r for r in d if r['Group']=='All Routes' and r['Category']=='Operating Revenue | Total')
metrics['q3_revenue_yoy_percent']=(num(rr['Q3_2020'])/num(rr['Q3_2019'])-1)*100

out=pathlib.Path(__file__).resolve().parents[1]/'Reports/source_verification.json'
out.write_text(json.dumps(metrics,indent=2)+'\n')
print(json.dumps(metrics,indent=2))
