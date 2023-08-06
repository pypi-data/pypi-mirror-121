# ML_Classification_model_selector





## Functions available
a) Model_Selector --> it is a class
- You can import his  by 'from select_classifier.select_model import Model_Selector'
- initialise the Model_Selector
- eg: v=Model_Selector()

b) model_performances
- Here you need to provide dataframe and the name of the target column
- Dataframe should be free of missing values and categorical features
- This method results the performance of mentioned models in terms of accuracy,precision,recall,f1_score and roc_auc_score
- eg: v.model_performances(dataframe,'target')

c)select_best_model
- This method results the name of the model which performs best in mentioned metrics
- eg: v.model_performances(based_on='accuracy')

d)plot_model_performance
- This method results the line plot of performances of all models
- eg: v.plot_model_performance()

