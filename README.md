## Example Service
###### Repo: `up.aws-lambda-rest.template`

### Description
This Lambda implements the Example Service.

Below is the structure of the project:

```
.
├── README.md                      <-- This instructions file
├── example                        <-- Business logic module for this lambda
├── template.yaml                  <-- SAM Template
├── buildspec.yaml                 <-- CodeBuild specification
└── tests                          <-- Unit tests
    └── unit
    └── resources                  <-- Test resources
```

### Chalice
This Lambda uses the [Chalice Serverless Microframework](https://chalice.readthedocs.io/en/latest/) for routing.

### Requirements

* Python3.7+

### Local development

* Create a virtual env: `python -mvenv .venv/`
* Activate virtual env: `source venv/bin/activate` or `source venv/Scripts/activate`
* Install dependencies: `pip install -r requirements.txt`
* Build:                `sam build`
* Run local API:        `sam local start-api`

### Local quickstart

```
./bin/sam-build-run
```

### Testing

This project uses nose tests. Simply run

```
python -m nose tests/unit
```

### Deployment

* Local SAM validation:

```
./bin/pre-commit
```
* Setup AWS configuration (~/.aws/config) and assign the profile (AWS_DEFAULT_PROFILE)

* Package and deploy to custom environment:
```
./bin/sam-package-deploy
```
