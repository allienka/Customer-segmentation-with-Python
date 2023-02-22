import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def getCSV(file):  
    customers_df=pd.read_csv(file)
    return customers_df

def getModifiedPURCHASE_COUNT_BY_STORE_TYPE(customers_df):
    customers_df['PURCHASE_COUNT_BY_STORE_TYPE'].replace(r'\s+|\\n', ' ', regex=True, inplace=True) 
    customers_df['PURCHASE_COUNT_BY_STORE_TYPE'].replace('}',' ', regex=True)
    customers_df['PURCHASE_COUNT_BY_STORE_TYPE']=customers_df['PURCHASE_COUNT_BY_STORE_TYPE'].replace('{',' ', regex=True)
    return customers_df['PURCHASE_COUNT_BY_STORE_TYPE']

def splitPURCHASE_COUNT_BY_STORE_TYPE(customers_df):
    customers_df[['GENERAL_MERCH','GROCERY','PET SUPPLIES','RESTAURANT','RETAIL STORE']]=customers_df['PURCHASE_COUNT_BY_STORE_TYPE'].str.split(',', 4, expand=True)
    return customers_df[['GENERAL_MERCH','GROCERY','PET SUPPLIES','RESTAURANT','RETAIL STORE']]

def getModifiedGENERAL_MERCH(customers_df):
    customers_df['GENERAL_MERCH'] = customers_df['GENERAL_MERCH'].replace('"General merchandise":','', regex=True)
    return customers_df['GENERAL_MERCH']

def getModifiedGROCERY(customers_df):
    customers_df['GROCERY'] = customers_df['GROCERY'].replace('"Grocery":','', regex=True)
    return customers_df['GROCERY']

def getModifiedPET_SUPPLIES(customers_df):
    customers_df['PET SUPPLIES'] = customers_df['PET SUPPLIES'].replace('"Pet supplies":','', regex=True)
    return customers_df['PET SUPPLIES']

def getModifiedRESTAURANT(customers_df):
    customers_df['RESTAURANT'] = customers_df['RESTAURANT'].replace('"Restaurant":','', regex=True)
    return customers_df['RESTAURANT']

def getModifiedRETAIL_STORE(customers_df):
    customers_df['RETAIL STORE'] = customers_df['RETAIL STORE'].replace('"Retail store":','', regex=True)
    customers_df['RETAIL STORE'] = customers_df['RETAIL STORE'].replace('}','', regex=True)
    return customers_df['RETAIL STORE']

def getModifiedPREFERRED_RESTAURANT_TYPES(customers_df):
    customers_df['PREFERRED_RESTAURANT_TYPES'] = customers_df['PREFERRED_RESTAURANT_TYPES'].apply(eval)
    return customers_df['PREFERRED_RESTAURANT_TYPES']

def toNumeric(customers_df):
    customers_df[['GENERAL_MERCH','GROCERY','PET SUPPLIES','RESTAURANT','RETAIL STORE']] =customers_df[['GENERAL_MERCH','GROCERY','PET SUPPLIES','RESTAURANT','RETAIL STORE']].apply(pd.to_numeric) 
    return customers_df[['GENERAL_MERCH','GROCERY','PET SUPPLIES','RESTAURANT','RETAIL STORE']]


def toTime(customers_df):
    customers_df['MOST_COMMON_HOUR_OF_THE_DAY_TO_PURCHASE'] = pd.to_datetime(customers_df.MOST_COMMON_HOUR_OF_THE_DAY_TO_PURCHASE, format='%H').dt.time
    return customers_df['MOST_COMMON_HOUR_OF_THE_DAY_TO_PURCHASE']

def toDateTime(customers_df,columnName):
    customers_df[columnName] = pd.to_datetime(customers_df[columnName]).dt.date
    return customers_df[columnName] 

def getCountriesDF(customers_df):
    filtered_data=customers_df[['REGISTRATION_COUNTRY','USER_ID']]
    return filtered_data

def getCountriesGraph(customers_df):
    countries=customers_df['REGISTRATION_COUNTRY'].tolist()
    
    arr=[]  
    i=0
    while i<(len(countries)):
        arr.append(countries[i])
        i=i+1

    elements_count = {}
    a={}
    for element in arr:
        if element in elements_count:
            elements_count[element] += 1
        else:
            elements_count[element] = 1
        
    a = dict(sorted(elements_count.items(), key=lambda item: item[1], reverse=True))
    print(a)
    x=[]
    y=[]

    for key, value in a.items():
    #print(f"{key}: {value}")
        x.append(key)
        y.append(value)

    plt.bar(x=x,height=y,width=0.8)
    plt.title('COUNTRIES')
    plt.show()


def getFinData(customers_df):
    fin_data=customers_df[customers_df.REGISTRATION_COUNTRY=='FIN']
    return fin_data

def getDeliveryTakeaway(fin_data):
    data=fin_data[['PURCHASE_COUNT_DELIVERY','PURCHASE_COUNT_TAKEAWAY']].sum()
    return data

def getDeliveryTakeawayGraph(fin_data):
    fin_data[['PURCHASE_COUNT_DELIVERY','PURCHASE_COUNT_TAKEAWAY']].sum().plot.bar (color='GREEN')
    plt.title('DELIVERY vs TAKEAWAY')
    plt.show()
    

def getTypePurchases(fin_data):
    data=fin_data[['BREAKFAST_PURCHASES','LUNCH_PURCHASES','EVENING_PURCHASES','DINNER_PURCHASES','LATE_NIGHT_PURCHASES']].sum()
    return data

def getTypePurchasesGraph(fin_data):
    fin_data[['BREAKFAST_PURCHASES','LUNCH_PURCHASES','EVENING_PURCHASES','DINNER_PURCHASES','LATE_NIGHT_PURCHASES']].sum().plot(kind="pie", autopct='%1.1f%%', ylabel='',title='Types of purchses')
    plt.title('Type of Purchases')
    plt.show()

def getMostCommonHour(fin_data):
    data=fin_data['MOST_COMMON_HOUR_OF_THE_DAY_TO_PURCHASE'].value_counts()[:6]
    return data

def getMostCommonHourGraph(fin_data):
    fin_data['MOST_COMMON_HOUR_OF_THE_DAY_TO_PURCHASE'].value_counts().plot.bar()
    plt.title('MOST COMMON PURCHASE HOURs')
    plt.show()

def getPreferredDevices(fin_data):
    data=fin_data[['IOS_PURCHASES','WEB_PURCHASES','ANDROID_PURCHASES']].sum()
    return data

def getPreferredDevicesGraph(fin_data):
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
    fin_data[['IOS_PURCHASES','WEB_PURCHASES','ANDROID_PURCHASES']].sum().plot(kind="pie", autopct='%1.1f%%',colors=colors, ylabel='',title='Preferred devices')
    plt.show()
   

def getPurchaseValues(fin_data):
    data=fin_data[['USER_ID','TOTAL_PURCHASES_EUR','MIN_PURCHASE_VALUE_EUR','MAX_PURCHASE_VALUE_EUR','AVG_PURCHASE_VALUE_EUR']].dropna()
    return data

def getValidPaymentInfo(fin_data):
    data=fin_data['USER_HAS_VALID_PAYMENT_METHOD'].value_counts() 
    return data

def getValidPaymentGraph(fin_data):
    fin_data['USER_HAS_VALID_PAYMENT_METHOD'].value_counts().plot.bar()
    plt.title('Valid paymend method')
    plt.show()

def dayNameFromWeekday(weekday):
    if weekday == 1.00:
        return "Monday"
    if weekday == 2.00:
        return "Tuesday"
    if weekday == 3.00:
        return "Wednesday"
    if weekday == 4.00:
        return "Thursday"
    if weekday == 5.00:
        return "Friday"
    if weekday == 6.00:
        return "Saturday"
    if weekday == 7.00:
        return "Sunday"
def changeToWeekday(fin_data):
    data=fin_data['MOST_COMMON_WEEKDAY_TO_PURCHASE'].apply(lambda x: dayNameFromWeekday(x))
    return data

def getMostCommonWeekdays(fin_data):
    data=changeToWeekday(fin_data).value_counts()
    return data

def getWeekdaysGraph(fin_data):
    changeToWeekday(fin_data).value_counts().plot.bar()
    plt.title('MOST COMMON WEEKDAY')
    plt.show()

def to_1D(series):
 return pd.Series([x for _list in series for x in _list])

def getRestaurantTypes(fin_data):
    data=to_1D(fin_data['PREFERRED_RESTAURANT_TYPES']).value_counts()
    return data

def getRestaurantGraph(fin_data):
    to_1D(fin_data['PREFERRED_RESTAURANT_TYPES']).value_counts().plot(kind='bar',color='GREEN')
    plt.title('PREFERRED RESTAURANT TYPES')
    plt.show()

def getAvgDistance(fin_data):
    data=fin_data['AVERAGE_DELIVERY_DISTANCE_KMS'].value_counts()
    return data

def getPurchasesByStore(fin_data):
    data=fin_data[['GENERAL_MERCH','GROCERY','PET SUPPLIES','RESTAURANT','RETAIL STORE']].sum()
    return data

def getPurchasesByStoreGraph(fin_data):
    fin_data[['GENERAL_MERCH','GROCERY','PET SUPPLIES','RESTAURANT','RETAIL STORE']].sum().plot(kind='bar')
    plt.title('Purchases by store types')
    plt.show()

def getRFM(fin_data,recent_date):
    data=fin_data.groupby('USER_ID').agg({'LAST_PURCHASE_DAY': lambda date: (recent_date - date.max()).days,
                                        'PURCHASE_COUNT': lambda num: num*1,
                                        'TOTAL_PURCHASES_EUR': lambda price: price*1,
                                    'FIRST_PURCHASE_DAY':lambda date:date })
    return data

def getMonthlyCustomerIntakes(rfm):
    rfm["FIRST_PURCHASE_MONTH"] = rfm["FIRST_PURCHASE_DAY"].apply(lambda x: x.replace(day=1))
    rfm.groupby(["FIRST_PURCHASE_MONTH"]).count()["FIRST_PURCHASE_DAY"].plot(kind="bar")
    plt.title("Monthly Customer Intakes")
    plt.show()

def getR_rank(rfm):
    rfm['R_rank'] = rfm['recency'].rank(ascending=False)
    return rfm['R_rank']
def getF_rank(rfm):
    rfm['F_rank'] = rfm['frequency'].rank(ascending=True)
    return rfm['F_rank']
def getM_rank(rfm):
    rfm['M_rank'] = rfm['monetary'].rank(ascending=True)
    return rfm['M_rank']

def getNormR_rank(rfm):
    data=(getR_rank(rfm)/getR_rank(rfm).max())*100
    return data

def getNormF_rank(rfm):
    data=(getF_rank(rfm)/getF_rank(rfm).max())*100
    return data

def getNormM_rank(rfm):
    data=(getM_rank(rfm)/getM_rank(rfm).max())*100
    return data


def getRFMScore(rfm):
    rfm['RFM_Score'] = 0.15*rfm['R_rank_norm']+0.28 * \
    rfm['F_rank_norm']+0.57*rfm['M_rank_norm']
    rfm['RFM_Score'] *= 0.05
    return rfm['RFM_Score']


# rfm score >4.5 : Top Customer 
# 4.5 > rfm score > 4 : High Value Customer 
# 4>rfm score >3 : Medium value customer 
# 3>rfm score>1.6 : Low-value customers 
# rfm score<1.6 :Lost Customer
def getCustomerSegment(rfm):
    rfm["Customer_segment"] = np.where(getRFMScore(rfm) >
                                      4.5, "Top Customers",
                                      (np.where(
                                        getRFMScore(rfm) > 4,
                                        "High value Customer",
                                        (np.where(getRFMScore(rfm)> 3,
                             "Medium Value Customer",
                             np.where(getRFMScore(rfm) > 1.6,
                            'Low Value Customers', 'Lost Customers'))))))
    return rfm["Customer_segment"]


def getCustomerSegmentGraph(rfm):
        plt.pie(rfm.Customer_segment.value_counts(),
        labels=rfm.Customer_segment.value_counts().index,
        autopct='%.0f%%')
        plt.title('Customer segmentation')
        plt.show()