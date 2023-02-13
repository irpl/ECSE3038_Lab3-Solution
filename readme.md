# ECSE3038 Lab 3

when creating a new workspace

```
python -m venv venv
```

activate the venv

```
# windows
. venv/Scripts/activate

# macOS
. venv/bin/activate
```

installing fastAPI and motor

```
pip install "fastapi[all]" motor
```

start your server application

```
uvivorn app:app --reload
```

Front end component to test the lab

https://ecse3038-lab3-tester.netlify.app/
