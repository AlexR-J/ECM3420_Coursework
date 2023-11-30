
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import linear_model 
import pandas as pd
from sklearn import metrics


def preprocess_data() :

    summoner_df = pd.read_json("newData.json")
    summoner_df = pd.concat([
        summoner_df.drop('dataset', axis=1),
        pd.json_normalize(summoner_df['dataset'])])
    summoner_df = summoner_df.fillna(0)

    X = summoner_df[['masteryScore','highestMastery','winrate','wins','losses']]
    y = summoner_df['rankId']

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

    print("LinReg mae, msq:")
    LinReg = LinearRegression()
    LinReg.fit(x_train,y_train)
    predictions = LinReg.predict(x_test)
    mae_linreg = metrics.mean_absolute_error(y_test, predictions)
    msq_linreg = metrics.mean_squared_error(y_test,predictions)
    print(mae_linreg)
    print(msq_linreg)

    print("RidgeReg_highAlpha mae, msq:")
    RidReg = linear_model.Ridge(alpha=100)
    RidReg.fit(x_train, y_train)
    predictions_ridge = RidReg.predict(x_test)
    mae_ridgereg = metrics.mean_absolute_error(y_test, predictions_ridge)
    msq_ridgereg = metrics.mean_squared_error(y_test,predictions_ridge)
    print(mae_ridgereg)
    print(msq_ridgereg)

    print("RidgeReg_lowAlpha mae, msq:")
    RidRegLA = linear_model.Ridge(alpha=0.5)
    RidRegLA.fit(x_train, y_train)
    predictions_ridgeLA = RidRegLA.predict(x_test)
    mae_ridgeregLA = metrics.mean_absolute_error(y_test, predictions_ridgeLA)
    msq_ridgeregLA = metrics.mean_squared_error(y_test,predictions_ridgeLA)
    print(mae_ridgeregLA)
    print(msq_ridgeregLA)

    print("LassoReg_highAlpha mae, msq:")
    lassoReg = linear_model.Lasso(alpha=100)
    lassoReg.fit(x_train, y_train)
    predictions_lasso = lassoReg.predict(x_test)
    mae_lassoreg = metrics.mean_absolute_error(y_test, predictions_lasso)
    msq_lassoreg = metrics.mean_squared_error(y_test,predictions_lasso)
    print(mae_lassoreg)
    print(msq_lassoreg)

    print("LassoReg_lowAlpha mae, msq:")
    lassoRegLA = linear_model.Lasso(alpha=0.5)
    lassoRegLA.fit(x_train, y_train)
    predictions_lassoLA = lassoRegLA.predict(x_test)
    mae_lassoregLA = metrics.mean_absolute_error(y_test, predictions_lassoLA)
    msq_lassoregLA = metrics.mean_squared_error(y_test,predictions_lassoLA)
    print(mae_lassoregLA)
    print(msq_lassoregLA)

    x_axis = ['Linear','Ridge High Lambda', 'Ridge Low Lambda', 'Lasso High Lambda','Lasso Low Lambda']
    msq_values = [msq_linreg,msq_ridgereg,msq_ridgeregLA,msq_lassoreg,msq_lassoregLA]
    mae_values = [mae_linreg,mae_ridgereg,mae_ridgeregLA,mae_lassoreg,mae_lassoregLA]
    colors = ['mediumorchid','violet','violet','purple','purple']

    plt.bar(x_axis, msq_values, color=colors)
    plt.title('Mean Squared Error of Different Models')
    plt.xlabel('MSQ')
    plt.ylabel('Models')
    plt.ylim(15,33)
    plt.show()

    plt.bar(x_axis, mae_values, color=colors)
    plt.title('Mean Absolute Error of Different Models')
    plt.xlabel('MSQ')
    plt.ylabel('Models')
    plt.show()
 
if __name__ == "__main__":
    preprocess_data();