import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

#read file species_info.csv
species = pd.read_csv('species_info.csv')
print(species.head())

#different number of species - 5541
species_count = species['scientific_name'].nunique()
print(species_count)

#different values of category in DF species - 7
species_type = species['category'].unique()
print(len(species_type))

#different values of conservation_status - 5
conservation_statuses = species['conservation_status'].unique()
print(len(conservation_statuses))

#replaces NaN in species DF with 'No Intervention'
species.fillna('No Intervention', inplace = True)

#count how many scientific_name falls into conservation_status criteria
conservation_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index()
print(conservation_counts)

#count how many scientific_name falls into conservation_status criteria with NaN fixed
conservation_counts_fixed = species.groupby('conservation_status').scientific_name.nunique().reset_index()
print(conservation_counts_fixed)

# Are certain types of species more likely to be endangered?
#new column in species called is_protected, which is True if conservation_status is not equal to 'No Intervention', and False otherwise
species['is_protected'] = species.conservation_status != 'No Intervention'

#group by both category and is_protected.
category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()

print(category_counts.head())

#Using pivot, rearrange category_counts so that:
# columns is is_protected
# index is category
# values is scientific_name

category_pivot = category_counts.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()
  
print category_pivot

#are certain types of species more likely to be endangered?

  
category_pivot.columns = ['category', 'not_protected', 'protected']

# find the percentage of species protected
category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)

print(category_pivot)

# Inspecting the DataFrame
species_count = len(species)

species_type = species.category.unique()

conservation_statuses = species.conservation_status.unique()

# Analyze Species Conservation Status
conservation_counts = species.groupby('conservation_status').scientific_name.count().reset_index()

# print conservation_counts

# Analyze Species Conservation Status II
species.fillna('No Intervention', inplace = True)

conservation_counts_fixed = species.groupby('conservation_status').scientific_name.count().reset_index()

# Plotting Conservation Status by Species
protection_counts = species.groupby('conservation_status').scientific_name.count().reset_index().sort_values(by='scientific_name')
    
plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)), protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
labels = [e.get_text() for e in ax.get_xticklabels()]
plt.show()
plt.close()

#find p-value comparing those of birds and mammals

contingency = [[30, 146],[75, 413]]

print(chi2_contingency(contingency))

_, pval, _, _ = chi2_contingency(contingency)

#find p-value comparing reptiles and mammals
contingency_rep_mam = [[5, 73],[30, 146]]

_, pval_reptile_mammal, _, _ = chi2_contingency(contingency_rep_mam)

print(pval)
print(pval_reptile_mammal)

