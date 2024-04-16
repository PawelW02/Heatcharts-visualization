import pandas as pd
#from matplotlib import 
import time


filepath=r'.\PMB_test.txt'
parameter_list = ['SSB_0_N' , 'SSB_0_P', 'SSB_1_N' , 'SSB_1_P', 'SSB_2_N' , 'SSB_2_P', 'SSB_3_N' , 'SSB_3_P', 'SSB_4_N' , 'SSB_4_P']

def get_parameter_list(file_content):
    file_content = file_content.split('\n')
    for line in file_content:
        values = ''
        if "Index" in line:
            values = line.split('Pos.Az.Norm')[1]
            values = values.split()
            return values

def clear_axis(axis):
    axis = axis.drop_duplicates()
    axis = axis.values.tolist() 
    return axis

def create_parameter_dataframe(parameter, x_axis, y_axis, df):
    parameter_df = pd.DataFrame(columns= x_axis)
    y_elem_nr = len(y_axis)
    x_elem_nr = len(x_axis)
    df_elem_nr = len(df)
    for i in range(y_elem_nr):
        temp_values = []
        for k in range(x_elem_nr):
            for j in range(df_elem_nr):
                if df.iloc[j]['Pos.El.Norm'] == y_axis[i] and df.iloc[j]['Pos.Az.Norm'] == x_axis[k]:
                    temp_values.append(df.iloc[j][parameter])
        parameter_df.loc[len(parameter_df.index)] = temp_values
    parameter_df.index = y_axis

    parameter_df.style.background_gradient(cmap="Blues")
    return parameter_df

def create_dataframes(parameter_list, file_content):
    import numpy as np
    for parameter in parameter_list:
        s = time.time()
        data = "Index " + file_content.split("Index")[1]
        df = pd.DataFrame([x.split() for x in data.split('\n')])
        df = df.dropna()
        df.columns = df.iloc[0]
        df = df[1:]
        df = df.drop(columns=['Index', 'Time'])
        x_axis = clear_axis(df['Pos.Az.Norm'])
        y_axis = clear_axis(df['Pos.El.Norm'])
        y_axis.sort(key=float,reverse=True)
        x_axis.sort(key=float)

        parameter_df = create_parameter_dataframe(parameter, x_axis, y_axis, df)
        file_name= ".\\_results\\" + parameter + ".csv"
        parameter_df.to_csv(file_name)
        print(parameter)
        print(f'table creation took: {time.time() - s} seconds')

def main(filepath, parameter_list=None):
    with open(filepath, "r") as file:
        file_content = file.read()
        if parameter_list is None:
            parameter_list = get_parameter_list(file_content)
        create_dataframes(parameter_list, file_content)

if parameter_list:
    print("Parameter list defined")
    main(filepath, parameter_list)
else:
    main(filepath)
