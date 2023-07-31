import pandas as pd
import numpy as np


file1 = "/Users/muthuku/Downloads/alan-turing-institute-das-public-5581446_modify/output1_100annotations/correct_labels.csv"
file2 = "/Users/muthuku/Downloads/alan-turing-institute-das-public-5581446_modify/output1_100annotations/Classified_SVM_combined_labels_no-coding-approach1-stopwords-no-uniformprior_yes-stemming_yes-test_no.csv"
file3 = "/Users/muthuku/Downloads/alan-turing-institute-das-public-5581446_modify/output1_150annotations/Classified_SVM_combined_labels_no-coding-approach1-stopwords-no-uniformprior_yes-stemming_yes-test_no.csv"
file4 = "/Users/muthuku/Downloads/alan-turing-institute-das-public-5581446_modify/output1_175annotations/Classified_SVM_combined_labels_no-coding-approach1-stopwords-no-uniformprior_yes-stemming_yes-test_no.csv"

df1 = pd.read_csv(file1)
df1.set_index("Statement", inplace = True)

df2 = pd.read_csv(file4, header = None)
df2.columns = ["Statement", "number175"]

df2.set_index("Statement", inplace = True)
merged_df = pd.merge(df1, df2, left_index = True, right_index = True, how="left")
merged_df.reset_index(inplace=True)

df3= pd.read_csv(file3)
#df3.columns = ["Statement", "number150"]
df3.set_index("Statement", inplace = True)

merged_df2 = pd.merge(df1, df3, left_index=True, right_index = True, how = "left")
merged_df2.reset_index(inplace=True)

print(merged_df)
merged_df.to_csv("175check.csv", encoding = "utf-8")