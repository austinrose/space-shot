import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from numpy import linalg

my_path = "/Users/austinrose/development/python/stats-3670"

def stats_main():
    train_path = my_path + "/data/zillowcleanedup_train.csv"
    test_path = my_path + "/data/zillowcleanedup_test.csv"

    df_train = pd.read_csv(train_path)

    def average_finder(unique, col):
        output = []
        for value in unique:
            value_rows = df_train[df_train[col] == value]
            average_price = value_rows['Selling price'].sum() / len(value_rows)
            running_avg = [value, average_price]
            output.append(running_avg)
        return output

    def simple_regression(y,x):
        n=len(x) # n is the length of the vector x
        vec_ones=np.ones(n)# we make a vector of ones of same length than y and x
        X=np.array((vec_ones,x))
        [a,b]=np.linalg.solve(np.dot(X,np.transpose(X)),np.dot(X,y)) # the equation for solution of least square
        #regression is solved her by the numpy function linalg.solve
                                                                
        #next we calculate the median prediction error
        relative_error_vec=np.abs(y-(a+b*x))/y  # we first determine the vector of relative errors, 
        median_relative_error= np.median(relative_error_vec)   
        return[a,b,median_relative_error]


    # (1) find average selling price for each neighborhood
    neighborhoods = df_train['Zip code'].unique()
    neighborhood_average = average_finder(neighborhoods, 'Zip code')

    # (2) find average selling price for each house type
    house_types = df_train['House type'].unique()
    housetype_average = average_finder(house_types, 'House type')

    # (3) find average selling price for number of rooms
    num_rooms = df_train['beds'].unique()
    room_average = average_finder(num_rooms, 'beds')

    # (4) plot sqft vs house price with different colors for each neighborhood and find regression for each neighborhood
    all_price = df_train['Selling price']
    all_sqft = df_train['sqft']
    a,b,median_error = simple_regression(all_price, all_sqft)
    plot_data = []
    regression = [['all', a, b, median_error]]

    for place in neighborhoods:
        sqft_vals = df_train[df_train['Zip code'] == place]['sqft']
        price_vals = df_train[df_train['Zip code'] == place]['Selling price']

        a,b,median_error = simple_regression(price_vals, sqft_vals)
        add_data = [place, a, b, median_error]
        
        plot_add = [sqft_vals, price_vals, place]

        plot_data.append(plot_add)
        regression.append(add_data)

    plt.scatter(plot_data[0][0], plot_data[0][1], label=plot_data[0][2])
    plt.scatter(plot_data[1][0], plot_data[1][1], label=plot_data[1][2]) 
    plt.scatter(plot_data[2][0], plot_data[2][1], label=plot_data[2][2])
    plt.xlabel("Square Footage")
    plt.ylabel("Price (USD)")
    plt.title("House Cost vs. Square Footage by Neighborhood")
    plt.legend()
    plt.savefig(my_path + "/price_sqft_plot.png")           

    # (5) Find the best predictor of house price based on train data and find mean relative error - compare results to Zillow's predicted accuracy
    # (6) Predict selling price of houses in test data set
    df_test = pd.read_csv(test_path)
    test_check = [df_test['House #'].tolist(), df_test['Zip code'].tolist(), df_test['sqft'].tolist()]
    test_predictions = []

    for house in test_check[0]:
        test_ind = test_check[0].index(house)
        test_zip = test_check[1][test_ind]
        test_sqft = test_check[2][test_ind]
        for row in regression:
            if row[0] == test_zip:
                guess_price = test_sqft * row[2] + row[1]
                test_predictions.append([house, guess_price])

    return [neighborhood_average, housetype_average, room_average, regression, test_predictions] 

stats_main()