# Import Packages
import numpy as np
import pandas as pd

def Date_transformer(abs_list,relative):

    result=[]

    for i in range(int(len(abs_list)/12)):

        for j in range(12):

            result.append(relative+i)


    return result

# Loop through the data 
def Extract_Depths(data_obs,data_sim,date_list,data_depth,data_lon,data_lat):


    list_all=[]

    for i in range(len(data_depth)):
        
        depth=data_depth[i]
        
        depth_list=[]
        
        for j in range(len(data_lon)):
            
            station=[data_lon[j],data_lat[j]]

            station_list=[]
           
            for z in range(0,len(date_list),12):
                
                date_start=date_list[z]

                index=z
                checker1=True
                checker2=True

                # Fills help_list until the next year starts, or there is an unfilled value
                # Then the loop breaks. In the later case the months of that year get discarded
                help_list=[]
                while (index<z+12 and date_start==date_list[index]) and (checker1==True and checker2==True):

                    measurement=data_obs[j][0][i][index]
                    simulation=data_sim[j][i][index]
                    if (measurement < 1000 and simulation < 1000) :
                        help_list.append(
                            [int(date_start),
                             round(station[0],3),
                             round(station[1],3),
                             round(depth,3),
                             round(measurement,3),
                             round(simulation,3)])
                        
                    checker1=bool(measurement < 1000)
                    checker2=bool(simulation  < 1000)

                
                    index=index+1
                        
                    
                if len(help_list)==12:
                    for item in help_list:
                        
                        list_all.append(item)

    

    all_result=pd.DataFrame(np.array(list_all),columns=['year','station_lon','station_lat','depth','measurement','simulation'])
    all_result.to_csv('results.csv',header=False,index=False)
                            
    return all_result
