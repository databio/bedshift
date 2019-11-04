#!/usr/bin/python

from bedshift import bedshift

bedshifter = bedshift.Bedshift()

df = bedshifter.readDF('test.bed')
original_rows = df.shape[0]
df = bedshifter.all_perturbations(df, 0.3, 320.0, 20.0, 0.3, -10.0, 120.0, 0.1, 0.11, 0.03)

bedshifter.write_csv(df, 'py_output.bed')