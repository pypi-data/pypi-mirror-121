
===================================================================
-----------------------  larkinlab 0.0.18  ------------------------
===================================================================


This library contains the functions I have created or come accross that I find myself using often. 

I will be adding things as I see fit, so be sure to update to the latest version.

Check the CHANGELOG for release info.


========  In The Future  ========

- v0.1 in the works

========================================================================================
-------------------------  Code Descriptions  ------------------------------------------
========================================================================================


-----  to install/update  ------

pip3 install larkinlab
pip3 install --upgrade larkinlab

---------  Subpackages  --------

larkinlab.explore
larkinlab.machinelearning

--------------------------------

=========================  ll.explore  =============================

This is built for exploring data. Contains functions that help you get an understanding of the data at hand quickly.

Import
> from larkinlab import explore as llex
> import larkinlab.explore as llex

Dependencies
> pandas
> numpy
> matplotlib.pyplot
> seaborn

--------------------------------
-- functions --
--------------------------------

-------------------------------------
* llex.df_ex(df, head_val) *

The df_ex (dataframe explore) function takes a dataframe and returns a few basic things
- The number of rows, columns, and total data points
- The names of the columns, limited to the first 60 if more than 60 exist
- Displays up to the first n rows of the dataframe via the df.head method, set by head parameter.

Parameter Default Values
> df  ::  pandas DataFrame
> head_val =5  ::  Sets the number of rown to display in the dataframe preview. Works via the pandas .head method. Set to 'all' for all rows

------------------------------------- 
* llex.vcount_ex(df, print_count) *

The vcount_ex function returns the value counts and normalized value counts for all of columns in the dataframe passed through it.
        
Parameter Default Values
> df  ::  pandas DataFrame
> print_count =5  ::  sets the number of value counts to print for each column. Set to 'all' for all of them, for example - (df, print_count='all') 

-------------------------------------
* llex.missing_ex(df) *
        
The missing_ex function prints the number of missing values in each column of the dataframe passed through it.

Parameter Default Values
> df  ::  pandas DataFrame

-------------------------------------
* llex.scat_ex(df) *
        
The scat_ex function returns a scatterplot representing the value counts and thier respective occurances for each column in the dataframe passed through it. 

Parameter Default Values
> df  ::  pandas DataFrame

-------------------------------------
* llex.corr_ex(df, min_corr, min_count, fig_size, colors) *
        
The corr_ex function returns either a pearson correlation values chart and a heatmap of said correlation values, or only the heatmap, for all of the columns in the dataframe passed through it. 

Parameter Default Values
> df  ::  pandas DataFrame
> min_corr =0.2  ::  minimum correlation value to appear on heatmap
> min_count =1  ::  minimum number of observations required per pair of columns to have a valid result(pandas.df.corr(min_periods) argument)
> fig_size =(8, 10)  ::  heatmap size, 2 numbers
> colors ='Reds'  ::  color of the heatmap. Heatmap from seaborn, so uses thier color codes

-------------------------------------
* llex.help(desc=False) *

A function to list all of the functions in the subpackage, with a description of them an optional argument

Parameter Default Values
> desc =False  ::  Description. A True value will list function along with description and perameters

-------------------------------------
*  *


-------------------------------------



=========================  ll.machinelearning  =============================

This package contains streamlined machine learning models and evaluation tools

Import 
> from larkinlab import machinelearning as llml
> import larkinlab.machinelearning as llml

Dependencies 
> pandas
> numpy
> matplotlib.pyplot 

--------------------------------
-- functions --
--------------------------------

-------------------------------------
*  *


-------------------------------------
*  *


-------------------------------------
*  *


-------------------------------------



=========================================================================================================================
-------------------------------------------------------------------------------------------------------------------------
=========================================================================================================================


Created By: Conor E. Larkin

email: conor.larkin16@gmail.com
GitHub: github.com/clarkin16
LinkedIn: linkedin.com/in/clarkin16

Thanks for checking this out!
