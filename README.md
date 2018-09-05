# MahaRERA-bulk-search
Get consolidaated list of MahaRERA Search Results, given a list of Project Names.

## Features
+ For multiple results against a project hame, results sorted by fuzzy matching against names.

## Usage
+ Rename the csv file containing your project names in the first column to 'mmr_noresult.csv' and place in the "data" folder.
+ Execute MH_POST.PY

## Advanced Usage
+ To include all results, and not just the one with the highest Fuzzy Match score, set includeHighest to 'False' in the call to 'searchResults' method call. (MH_POST: Line 51)
+ To skip fuzzy matching altogether (faster), set includeScores to 'False' in the call to 'searchResults' method call. (MH_POST: Line 51)
