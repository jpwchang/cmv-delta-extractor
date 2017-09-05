# r/ChangeMyView Delta Extractor

This is a small Python script for identifying comments on the subreddit
r/ChangeMyView that have received deltas (indicating successful view change).
It is designed for use with the [Cornell CMV Dataset](https://vene.ro/blog/winning-arguments-attitude-change-reddit-cmv.html).
There is a single file, `delta_extractor.py`, which provides a function
`extract_deltas`. This function may be imported into your Python code or
Jupyter notebook, allowing you to get deltas with a single line of code.
The function takes in a JSON object representing a submission (i.e. a
single line from the dataset) and returns a list of comment IDs (the "name"
field) of comments that earned deltas. There are also the following
optional arguments:

  - `return_comment_dict`: if set to True, the function will additionally
    return a dictionary of all comments in this submission indexed by ID,
    allowing for easy lookup of the comments corresponding to the IDs in
    in the returned list.
