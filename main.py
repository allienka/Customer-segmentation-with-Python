from functions import *

customers_df=getCSV('wolt.csv')

#modify, split to new columns and remove the old column PURCHASE_COUNT_BY_STORE_TYPE
getModifiedPURCHASE_COUNT_BY_STORE_TYPE(customers_df)
splitPURCHASE_COUNT_BY_STORE_TYPE(customers_df)
customers_df['GENERAL_MERCH']=getModifiedGENERAL_MERCH(customers_df)
customers_df['GROCERY']=getModifiedGROCERY(customers_df)
customers_df['PET SUPPLIES']=getModifiedPET_SUPPLIES(customers_df)
customers_df['RESTAURANT']=getModifiedRESTAURANT(customers_df)
customers_df['RETAIL STORE']=getModifiedRETAIL_STORE(customers_df)
customers_df = customers_df.drop('PURCHASE_COUNT_BY_STORE_TYPE', axis=1)

customers_df.dropna(how='any', inplace=True)
#PREFERRED_RESTAURANT_TYPES values were in list

getModifiedPREFERRED_RESTAURANT_TYPES(customers_df)

# changing the datatypes
#format floats to 2 decimal (it was causing discrepancies in counting of AVG, MIN, MAX)
pd.options.display.float_format = '{:,.2f}'.format

customers_df[['GENERAL_MERCH','GROCERY','PET SUPPLIES','RESTAURANT','RETAIL STORE']]=toNumeric(customers_df)
customers_df['REGISTRATION_DATE']=toDateTime(customers_df,'REGISTRATION_DATE')
customers_df['FIRST_PURCHASE_DAY']=toDateTime(customers_df,'FIRST_PURCHASE_DAY')
customers_df['LAST_PURCHASE_DAY']=toDateTime(customers_df,'LAST_PURCHASE_DAY')
customers_df['MOST_COMMON_HOUR_OF_THE_DAY_TO_PURCHASE']=toTime(customers_df)

# check the countries
getCountriesDF(customers_df)
getCountriesGraph(customers_df)

#filter data only for Finland

fin_data=getFinData(customers_df)

#analysing customers preferences in Finland

print(fin_data.describe())
print()
#the way of purchase customers prefare more
print('DELIVERY vs. TAKEAWAY: ')
print(getDeliveryTakeaway)
getDeliveryTakeawayGraph(fin_data)
print()

# most purchases are done for lunch and then dinner, there is no late night purchases
print('TYPE OF PURCHASES: ')
print(getTypePurchases(fin_data))
getTypePurchasesGraph(fin_data)
print()

#prefered ordering time
print('ORDERING TIME')
print(getMostCommonHour(fin_data))
getMostCommonHourGraph(fin_data) 
print()


#PREFERRED DEVICES customers use for orders
print('DEVICES:')
print(getPreferredDevices(fin_data))
getPreferredDevicesGraph(fin_data)
print()

#purchase values by customers
print('PURCHASE VALUES: ')
print(getPurchaseValues(fin_data) )
print() 

#more users didnt have valid payment method
print('VALID PAYMENT: ')
print(getValidPaymentInfo(fin_data))
getValidPaymentGraph(fin_data)
print()

#most common weekdays
print('MOST COMMON WEEEKDAY TO PURCHASE:')
print(getMostCommonWeekdays(fin_data))
getWeekdaysGraph(fin_data)
print()

#preferred restaurant types
print('PREFERRED_RESTAURANT_TYPES')
print(getRestaurantTypes(fin_data))
getRestaurantGraph(fin_data)
print()


#avg purchase distanse
print('AVG PURCHASE DISTANCE: ')
print(getAvgDistance(fin_data))
print()

#purchase count by store type
print('PURCHASE COUNT BY STORE TYPE:')
print(getPurchasesByStore(fin_data))
getPurchasesByStoreGraph(fin_data)
print()

#RFM ANALYSIS
print ('RFM ANALYSIS: ')
fin_data=fin_data[['USER_ID','PURCHASE_COUNT','FIRST_PURCHASE_DAY','LAST_PURCHASE_DAY','TOTAL_PURCHASES_EUR']]
recent_date = fin_data['LAST_PURCHASE_DAY'].max()
# Aggregate at user level
# Calculate recency, relative recency and relative frequency
# Take the maximum purchase date as today
rfm=getRFM(fin_data,recent_date)

#renaming columns
rfm.columns=['recency','frequency','monetary', 'FIRST_PURCHASE_DAY']
#removing missing values
rfm=rfm.dropna()
print('MONTHLY CUSTOMER INTAKES:')
getMonthlyCustomerIntakes(rfm)
#Ranking Customer’s based upon their recency, frequency, and monetary score Here we are normalizing the rank of the customers within a company to analyze the ranking.
# normalizing the rank of the customers
rfm['R_rank_norm'] = getNormR_rank(rfm)
rfm['F_rank_norm'] = getNormF_rank(rfm)
rfm['M_rank_norm'] = getNormM_rank(rfm)
 
rfm.drop(columns=['R_rank', 'F_rank', 'M_rank'], inplace=True)
print(rfm.head())

#RFM score is calculated based upon recency, frequency, monetary value normalize ranks. Based upon this score we divide our customers. Here we rate them on a scale of 5. Formula used for calculating rfm score is : 0.15Recency score + 0.28Frequency score + 0.57 *Monetary score
rfm['RFM_Score']=getRFMScore(rfm)
rfm = rfm.round(2)

#Rating Customer based upon the RFM score 
# rfm score >4.5 : Top Customer 
# 4.5 > rfm score > 4 : High Value Customer 
# 4>rfm score >3 : Medium value customer 
# 3>rfm score>1.6 : Low-value customers 
# rfm score<1.6 :Lost Customer

rfm['Customer_segment']=getCustomerSegment(rfm)
print(rfm[['RFM_Score', 'Customer_segment']].head()) 

getCustomerSegmentGraph(rfm)
