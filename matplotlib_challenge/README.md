# Matplotlib Challenge
**Tools: Jupyter, Pandas, Matplotlib**

# Power of Plots

Task 1) Check the data for any mouse ID with duplicate time points and remove any data associated with that mouse ID.
  - Save the cleaned data for remaining steps.

To do this I verify that the data has dupplicate values in it based on mouse ID by using duplicated. Then I drop all duplicates to clean up data.
```
duplicate_mice_all = mouse_study_df[mouse_study_df.duplicated(['Mouse ID'])]
clean_mice_df = mouse_study_df.drop_duplicates('Mouse ID')
```

Task 2) Generate a summary statistics table consisting of the mean, median, variance, standard deviation, and SEM of the tumor volume for each drug regimen.

I went with aggregation in order to run all the functions I needed at once and store that in a df.
```
aggregate_mouse_df = mouse_study_df[['Drug Regimen', 'Tumor Volume (mm3)']].groupby(['Drug Regimen']).aggregate(
    Mean=('Tumor Volume (mm3)', 'mean'),
    Median=('Tumor Volume (mm3)', 'median'),
    Variance=('Tumor Volume (mm3)', 'var'),
    Std_Dev= ('Tumor Volume (mm3)', 'std'),
    SEM=('Tumor Volume (mm3)', 'sem')
)
print(aggregate_mouse_df)
```

Task 3) Generate a bar plot using both Pandas's DataFrame.plot() and Matplotlib's pyplot that shows the total number of timepoints for all mice tested for each drug regimen throughout the course of the study.

For Pandas I went with this:
```
regimen_id = mouse_study_df.groupby('Drug Regimen')['Timepoint'].count()
regimen_id = regimen_id.plot.bar(title='Number of Timepoints per Drug', figsize=(10, 4))
regimen_id.set_xlabel('Drug Regimen')
regimen_id.set_ylabel('Number of Timepoints')
```

For pyplot I went with:
```
drug_axis = mouse_study_df['Drug Regimen'].unique()
timepoints_axis = mouse_study_df['Drug Regimen'].value_counts()
plt.figure(figsize=(10, 4))
plt.bar(drug_axis,timepoints_axis)
plt.xticks(drug_axis, rotation=90)
plt.xlim(-0.6, len(drug_axis)-.4)
plt.ylim(0, max(timepoints_axis)+5)
plt.ylabel('Number of Timepoints')
plt.xlabel('Drug Regimen')
plt.title('Number of Timepoints per Drug')
```

Task 4) Generate a pie plot using both Pandas's DataFrame.plot() and Matplotlib's pyplot that shows the distribution of female or male mice in the study.

This is my pandas pie plot:
```
mouse_gender_count = pd.value_counts(mouse_study_df['Sex'])
plt.figure(figsize=(6,6.5))
mouse_gender_pd = mouse_gender_count.plot(kind='pie', y='sex', startangle = 69, autopct='%1.1f%%', shadow=True)
plt.axis('equal')
plt.title('Mice Male & Female Percentage')
plt.xlabel('')
plt.ylabel('')
plt.legend(loc='best')
```

here is the pyplot pie plot:
```
plt.pie(mouse_gender_count, 
    labels=['Male','Female'],
    autopct='%1.1f%%',
    colors=['magenta','cyan'],
    startangle=100,
    shadow=True,
    explode=(0.1, 0)
)
plt.axis('equal')
plt.title('Mice Male & Female Percentage')
plt.legend(loc='best')
```

Task 5) Calculate the final tumor volume of each mouse across four of the most promising treatment regimens: Capomulin, Ramicane, Infubinol, and Ceftamin. Calculate the quartiles and IQR and quantitatively determine if there are any potential outliers across all four treatment regimens.

For this task I went a bit overkill for it, but to start I created new dataframes.
```
# Start by getting the last (greatest) timepoint for each mouse
mouse_greatest_tp = pd.DataFrame(mouse_study_df.groupby('Mouse ID').max()['Timepoint'])
# Merge this group df with the original dataframe to get the tumor volume at the last timepoint
merged_mouse_df = pd.merge(mouse_greatest_tp, mouse_study_df, on=('Mouse ID', 'Timepoint'), how='left')
clean_merged_mouse_df = merged_mouse_df[merged_mouse_df["Drug Regimen"].isin(["Capomulin", "Ramicane", "Infubinol", "Ceftamin"])]
```
Then I prepped a list and new class for use in a for loop.
```
# Put treatments into a list for for loop (and later for plot labels)
pills = clean_merged_mouse_df['Drug Regimen'].unique()
# Create class to be used to pull pill name and tumor data from the dataframe.
class pill_data:
    def __init__(self, name: str, data: DataFrame) -> None:
        self.name: str = name
        self.data: DataFrame = data
```
The for loop I chose to go with will store the pill data I need for my boxplot as well as calculate the IQR for this task.
```
# Empty list for boxplot. 
data_list: List[pill_data] = []
# Empty list for math calculations.
tumor_math = []
# Setup the for loop.
for pill in pills:
    # Hold data when drug pill == drug pill
    pill_df = clean_merged_mouse_df.loc[clean_merged_mouse_df['Drug Regimen']==pill]
    # Pull drug & tumor data from the data being held.
    tumor_data: DataFrame = pill_df[['Drug Regimen', 'Tumor Volume (mm3)']]
    # Hold drug & tumor data.
    new_pill = pill_data(pill, tumor_data)
    # Append boxplot list with drug & tumor data.
    data_list.append(new_pill)
    # Mathimatical!
    quartiles = pill_df['Tumor Volume (mm3)'].quantile([.25,.5,.75])
    lowerq = quartiles[0.25]
    upperq = quartiles[0.75]
    iqr = upperq-lowerq
    lower_bound = lowerq - (1.5*iqr)
    upper_bound = upperq + (1.5*iqr)
    # Append tumor list with the new values..
    tumor_math.append([pill, lowerq, upperq, iqr, lower_bound, upper_bound])
# Display IQR and Outliers.
for pill in tumor_math:
    print(pill)
```

Task 6) Using Matplotlib, generate a box and whisker plot of the final tumor volume for all four treatment regimens.

From my for loop Im able to create this boxplot.
```
# Create the boxplot!
bp: plt.boxplot = clean_merged_mouse_df.boxplot(column='Tumor Volume (mm3)', by='Drug Regimen', grid=False)
plt.suptitle('')
plt.show()
```

Task 7) Select a mouse that was treated with Capomulin and generate a line plot of tumor volume vs. time point for that mouse

To do this I made sure to look at only Capomulin data, then group data on Mouse ID, and finally pull mouse "m957" data from the table.
```
capomulin_mouse = mouse_study_df[mouse_study_df['Drug Regimen'] == 'Capomulin'].groupby('Mouse ID').get_group('m957')
capomulin_mouse.plot(x = 'Timepoint', y = 'Tumor Volume (mm3)')
plt.xlabel('Timepoint')
plt.ylabel('Tumor Volume (mm3)')
plt.title('Tumor Volume vs Timepoint (Mouse m957)')
plt.show()
```

Task 8) Generate a scatter plot of tumor volume versus mouse weight for the Capomulin treatment regimen.

To create this graph I needed to just ook at only Capomulin data, then get the mean of the grouped Mouse ID.
```
capomulin_avg = mouse_study_df[mouse_study_df['Drug Regimen'] == 'Capomulin'].groupby('Mouse ID').mean()
capomulin_avg.plot(kind = 'scatter', x = 'Weight (g)', y = 'Tumor Volume (mm3)')
plt.title(' Average Tumor Voume vs Mouse Weight')
plt.show()
```


Task 9) Calculate the correlation coefficient and linear regression model between mouse weight and average tumor volume for the Capomulin treatment. Plot the linear regression model on top of the previous scatter plot.

My chosen method for generating a linear regression model.
```
# Create X & Y values.
x_val = capomulin_avg["Weight (g)"]
y_val = capomulin_avg["Tumor Volume (mm3)"]
# Create function that takes X values and returns estimate for y.
coefficient = np.polyfit(x_val, y_val, 1)
poly_fn = np.poly1d(coefficient)
# Plot liner regression model & format
plt.plot(x_val, y_val, 'yo', x_val, poly_fn(x_val), '--k')
plt.xlabel('Mouse Weight (g)')
plt.ylabel('Tumor Volume (mm3)')
plt.title(' Average Tumor Voume vs Mouse Weight')
plt.show()
```

Task 10) Look across all previously generated figures and tables and write at least three observations or inferences that can be made from the data. 

My observations are included in the top of this jupyter notepad.
