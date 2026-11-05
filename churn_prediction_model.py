"""Experimento didático com dados sintéticos, sem evidência de eficácia comercial."""
import argparse
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES=['dias_inatividade','volume_tickets_ultimos_60d','valor_medio_transacao','frequencia_uso_mensal']
ROOT=Path(__file__).resolve().parent

def simulate(n=500,seed=42):
    if n<50:raise ValueError('Use pelo menos 50 registros na simulação')
    rng=np.random.default_rng(seed)
    df=pd.DataFrame({'id_cliente':range(1,n+1),'dias_inatividade':rng.integers(0,100,n),'volume_tickets_ultimos_60d':rng.integers(0,5,n),'valor_medio_transacao':rng.uniform(50,500,n),'frequencia_uso_mensal':rng.integers(1,30,n)})
    df['churn']=((df.dias_inatividade>60)&(df.volume_tickets_ultimos_60d>=2)).astype(int)
    df.loc[rng.choice(n,size=int(n*.1),replace=False),'churn']=1
    return df

def evaluate(y,pred,prob):
    return {'accuracy':float(accuracy_score(y,pred)),'precision':float(precision_score(y,pred,zero_division=0)),'recall':float(recall_score(y,pred,zero_division=0)),'f1':float(f1_score(y,pred,zero_division=0)),'roc_auc':float(roc_auc_score(y,prob)),'confusion_matrix':confusion_matrix(y,pred,labels=[0,1]).tolist()}

def run(output=ROOT/'artifacts',seed=42):
    start=time.perf_counter();df=simulate(seed=seed)
    train,test=train_test_split(df,test_size=.2,random_state=seed,stratify=df.churn)
    if set(train.id_cliente)&set(test.id_cliente):raise ValueError('Sobreposição entre treino e teste')
    model=make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),LogisticRegression(solver='liblinear',random_state=seed))
    model.fit(train[FEATURES],train.churn)
    pred=model.predict(test[FEATURES]);prob=model.predict_proba(test[FEATURES])[:,1]
    baseline=DummyClassifier(strategy='prior').fit(train[FEATURES],train.churn)
    bp=baseline.predict(test[FEATURES]);bprob=baseline.predict_proba(test[FEATURES])[:,1]
    metrics={'data_type':'synthetic','seed':seed,'records':len(df),'train_records':len(train),'test_records':len(test),'threshold':.5,'positive_rate_test':float(test.churn.mean()),'model':evaluate(test.churn,pred,prob),'baseline':evaluate(test.churn,bp,bprob),'checks':{'disjoint_train_test':True,'preprocessing_fit_on_train_only':True,'scoring_output_contains_test_only':True},'duration_seconds':round(time.perf_counter()-start,4),'limitation':'O alvo é construído com inatividade e tickets; o resultado reflete a regra sintética e não comprova capacidade preditiva em clientes reais.'}
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    scored=test[['id_cliente','churn']].copy();scored['churn_risk_score']=prob;scored['predicted_churn']=pred;scored.sort_values('churn_risk_score',ascending=False).to_csv(output/'holdout_scores.csv',index=False)
    pd.DataFrame({'feature':FEATURES,'coefficient':model.named_steps['logisticregression'].coef_[0]}).to_csv(output/'coefficients.csv',index=False)
    (output/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(metrics,ensure_ascii=False,indent=2));return metrics,train,test,scored

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'artifacts');p.add_argument('--seed',type=int,default=42);a=p.parse_args();run(a.output,a.seed)
