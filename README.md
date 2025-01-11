

## Setup

* Clone the repository

```bash
git clone https://github.com/your-username/webhook-repo.git
cd webhook-repo
```

* Create a new virtual environment

```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```
* Create the .env file

```bash
touch .env
```
MONGO_URI=mongodb://localhost:27017/github_events
PORT=5000
DEBUG=True

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* install ngrok

```bash
ngrok http 5000
```
