# Wave Propensity Application

This application allows not for profits to upload data and get back propensity scores to target their fundraising / marketing campaigns

#### Running this App Locally
_This has only been tested on OSX._

1. Download Wave

2. Create a python environment in the home app directory and install requirements 
```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

3. Run the app by pointing to the module directory
```bash
./venv/bin/wave run q_propensity.run
```

4. Point your web browswer to http://localhost:10101

In the future, if you want to run this app you can skip step 2 as the environment is already set up
