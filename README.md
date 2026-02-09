
### Setup
To install required dependencies, first create a new environment

```
conda create -n "myenv"
conda activate myenv
conda install --file requirements.txt
```




### Tests
To run tests, run

`pytest -o log_cli=true --log-cli-level=DEBUG`
