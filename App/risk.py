import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import pickle



class Risk:
    def __init__(self,data,feature_file='features.txt'):
        self.data=data
        with open(feature_file) as fp:
            self.features=fp.read() 
            self.features=self.features.split('\n')
        self.model=pickle.load(open('xgbmodel.sav','rb'))
        self.risk={1:'None',2:'Very Low',3:'Low',4:'Medium Low',5:'Medium',6:'Medium High',7:'High',8:'Very high'}

    def load_and_preprocess(self):
        data=pd.read_csv(self.data)
        data=data[self.features]
        data=data.fillna(-1)
        Id=np.array(data['Id'])
        data['Product_Info_2']=pd.factorize(data['Product_Info_2'])[0]
        return Id, data

    def get_prediction(self,preprocessed_data):
        predictions=self.model.predict(preprocessed_data.drop('Id',axis=1))
        result=[]
        for val in predictions:
            result.append(self.risk[val])
        return result

    def save(self,Id,result):
        df=pd.DataFrame(columns=['Id','Response'])
        df['Id']=Id
        df['Response']=result
        val=df['Response'].value_counts()
        a=sns.barplot(x=val.index,y=val.values)
        a.set_xticklabels(a.get_xticklabels(), rotation=20)
        a.set_xlabel("Risk Levels")
        a.set_ylabel("No.of.customers")
        a.set_title("RISK ANALYSIS REPORT")
        plt.savefig('App/static/output/barplot.png')
        df.to_csv('App/static/output/risk.csv',sep=',',index=False)


