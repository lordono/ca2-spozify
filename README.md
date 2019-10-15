# Spozify

Spozify is a Python library that utilize [scikit-fuzzy](https://pythonhosted.org/scikit-fuzzy/overview.html) to find recommended songs from [Spotify Dataset](https://www.kaggle.com/tomigelo/spotify-audio-features).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install spozify.

```bash
python -m venv venv
.\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Run Flask App

For Windows

```bash
set FLASK_APP=app.py
flask run
```

For Linux

```bash
export FLASK_APP=app.py
flask run
```

### Browse in Chrome

Go to [Dashboard](http://localhost:5000) and try the application out!

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
