# Rossmann Store - Forecasting Sales

![](img/rossmann.jpg)

#

# 1. Context

Rossmann's is a big European drugstore. It operates over 3,000 drug stores in 7 European countries. Currently, Rossmann store managers are tasked by the CFO with predicting their daily sales for up to six weeks in advance. Store sales are influenced by many factors, including promotions, competition nearby, school and state holidays, seasonality, and locality. With thousands of individual managers predicting sales based on their unique circumstances, the accuracy of results can be quite varied. The dataset used is this project can be found at a kaggle competition: https://www.kaggle.com/c/rossmann-store-sales/data.

#

# 2. Business Problem

* **What is the context like?**

    * At a meeting with the leads of each department, the Rossmann's CFO made a proposal to renovate all of their store.

* **What is the root cause of the problem?**

    * The Rossmann's CFO wants to predict the next 6 weeks sales for each store, so he can bring forward part of this revenue to renovate them.

* **Who is the Stakeholder of the problem?**

    * The CFO, who directly requested the answer for the problem.

* **How will the solution be?**

    * Granularity \\(\rightarrow\\) daily sales for 6 weeks / store

    * Problem type \\(\rightarrow\\) sales forecasting, regression problem

    * How will the solution be delivered? \\(\rightarrow\\) Telegram API (via cellphone)

# 

# 3. Data available

To forecast the sales, some informations for each store are given. Most of the fields are self-explanatory. The following are descriptions for those that aren't:

* **Id** - an Id that represents a (Store, Date) duple within the test set
* **Store** - a unique Id for each store
* **Sales** - the turnover for any given day (this is what you are predicting)
* **Customers** - the number of customers on a given day
* **Open** - an indicator for whether the store was open: 0 = closed, 1 = open
* **StateHoliday** - indicates a state holiday. Normally all stores, with few exceptions, are closed on state holidays. Note that all schools are closed on public holidays and weekends. a = public holiday, b = Easter holiday, c = Christmas, 0 = None
* **SchoolHoliday** - indicates if the (Store, Date) was affected by the closure of public schools
* **StoreType** - differentiates between 4 different store models: a, b, c, d
* **Assortment** - describes an assortment level: a = basic, b = extra, c = extended
* **CompetitionDistance** - distance in meters to the nearest competitor store
* **CompetitionOpenSince[Month/Year]** - gives the approximate year and month of the time the nearest competitor was opened
* **Promo** - indicates whether a store is running a promo on that day
* **Promo2** - Promo2 is a continuing and consecutive promotion for some stores: 0 = store is not participating, 1 = store is participating
* **Promo2Since[Year/Week]** - describes the year and calendar week when the store started participating in Promo2
* **PromoInterval** - describes the consecutive intervals Promo2 is started, naming the months the promotion is started anew. E.g. "Feb,May,Aug,Nov" means each round starts in February, May, August, November of any given year for that store

#

# 4. Business Assumptions

All data was taken from the company's internal sales base of the last 30 months. Any data coming from before this period would be seriously affected by external events (biased).
Several details were provided, such as type of store, variety of products offered and the competition proximity. Other variable info such as customers per day and sales per day, holidays, marketing promotions were available too.

However, it was necessary to take some assumptions, for the problem solution. As it can seen down below:

- **CompetitionDistance**: It is expressed in meters but, sometimes it was zero. So, 'Zero Competition Distance' was the same as 'No Competition Proximity'. But, for ML Algorithms this input is a bias. In this case, I assumed a fixed value (200,000 m) higher than the highest value in the dataset.
- **Assortment**: I assumed that there is a hierarchy between types. So, stores with Assortment Type C must offer Types A and B too.
- **Open**: I removed all the lines that indicate Store Closed, as those stores had zero sales on the same day. For ML purposes, this will be reviewed in future CRISP cycle.

My strategy to solve this challenge was based in CRISP-DM Cycle:

**01. Understand the Problem:** _The most important step for correct plan entire solution_.

**02. Data Description:** My goal is to use statistics metrics to identify data outside the scope of business.

**03. Data Filtering:** Filter rows and select columns that do not contain pertinent information for modeling or that do not match the scope of the business.

**04. Feature Engineering:** Derive new attributes based on the original variables to better describe the phenomenon that will be modeled.

**05. Exploratory Data Analysis:** Explore the data to find insights and better understand the impact of variables on model learning.

**06. Data Preparation:** Prepare the data so that the Machine Learning models can learn the specific behavior.

**07. Feature Selection:** Selection of the most significant attributes for training the model, based on Occam's Razor premise.

**08. Machine Learning Modeling:** Machine Learning model training.

**09. Hyperparameter Fine Tunning:** Choose the best values for each of the hyperparameters of the model selected from the previous step.

**10. Convert Model Performance to Business Values:** Convert the performance of the Machine Learning model into a business result.

**11. Deploy Model to Production:** Publish the model to a cloud environment so other people or services can use the results to improve the business decision. __In this particular case, the model can be accessible via a Telegram Bot__.

#

# 5. Machine Learning Metrics

For the problem solution, it was evaluated four machine learning algorithms: Linear Regression, Lasso Regression, Random Forest Regressor and XGBoost Regressor.

A cross-validation was made for each model, evaluating the Mean Absolute Error (MAE), the Mean Absolute Percentage Error (MAPE) and the Root Mean Squared Error (RMSE). The average cross-validation error as well their respective standard deviation are ilustrated in the table below:

|       Model Name          |        MAE CV       |    MAPE CV    |      RMSE CV       |
|:-------------------------:|:-------------------:|:-------------:|:------------------:|
| Linear Regression         |  2081.73 +/- 295.63 | 0.30 +/- 0.02 | 2952.52 +/- 468.37 |
| Lasso Regression          |  2116.38 +/- 341.50 | 0.29 +/- 0.01 | 3057.75 +/- 504.26 |
| Random Forest Regressor   |  838.23 +/- 218.10  | 0.12 +/- 0.02 | 1257.07 +/- 318.2  |
| XGBoost Regressor         |  1038.4 +/- 195.37  | 0.14 +/- 0.02 | 1494.1 +/- 273.16  |

Although the Random Forest Regressor returned best results in this step, it was seen that its file occupies a significantly more space when compared to the XGBoost Regressor model's file. In this way, in order not to extrapolate the company's budget, the XGBoost Regressor model, which has a smaller file, will be deployed. The minor difference in metrics between the algorithms is compensated by this server usage cost saving.

After tunning the hyperparameters of the XGBoost model, the following metrics were obtained:

|    Model Name        |     MAE      |    MAPE    |     RMSE       |
|:--------------------:|:------------:|:----------:|:--------------:|
|  XGBoost Regressor   |   681.94    |   0.0984   |   989.65       |

As it can be seen, a better hyperparameter selection can improve the model's score significantly.

# 

# 6. Business Performance

In terms of business, MAE means how much the prediction is wrong, defining upper and lower bounds. MAPE means the percentage that predicted values are different when compared to the target values, thus, being an easy-to-interpret metric. 

The table below shows the worst store predictions, explaining that some stores are more difficult to predict sales. The worst_scenario field is calculated by subtracting the MAE from the predictions field and the best_scenario field is calculated by adding the MAE field.


|   store |   predictions |   worst_scenario |   best_scenario |      MAE |     MAPE |
|--------:|--------------:|-----------------:|----------------:|---------:|---------:|
|     292 |        106565 |           103268 |          109862 | 3297.37  | 0.569281 |
|     909 |        244182 |           236583 |          251781 | 7599.03  | 0.52865  |
|     876 |        208512 |           204377 |          212646 | 4134.56  | 0.316803 |
|     274 |        196566 |           195245 |          197887 | 1321.07  | 0.225985 |
|     610 |        177417 |           176601 |          178234 |  816.744 | 0.214994 |

Finally, the table below shows the sum for all stores, as well as the worst and best scenarios:

| Scenario       | Values           |
|:---------------|:-----------------|
| predictions    | R$283,690,432.00 |
| worst_scenario | R$282,926,582.14 |
| best_scenario  | R$284,454,331.65 |
