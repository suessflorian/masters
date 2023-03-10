# Question 3.1

Needed to have [graphviz](https://graphviz.org/) to render the trees involved. [Download how you'd like here](https://graphviz.org/download/).

I like to use the project VE manager `pipenv`. [See here](https://pipenv.pypa.io/en/latest/).

## Running
```
pipenv install
pipenv run python main.py
```

Output diagram produced in `model.pdf`. Will need an explanation as it's mostly opaque without one.

> However, the scikit-learn implementation does not support categorical variables for now. Hence the need for translation from categorical fields to an index'd numerical representation.
