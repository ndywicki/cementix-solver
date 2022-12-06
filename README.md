# Cemantix solver
 Solver to avoid speding to much time on cementix

 https://cemantix.certitudes.org/

It uses a random word from `words-full.txt` until the score is over 30%.
Then searches for better words with the list of synonyms provided by [rimessolides.com](https://www.rimessolides.com/motscles.aspx?m=baguette).

# Install & run

I recommand to create an [virtual env](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) then install dependecies:

```
pip install -r requirements.txt
```

Run the solver:

```
python3 cementix.py
```