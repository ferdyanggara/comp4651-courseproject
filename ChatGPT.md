# Discord ChatGPT

## Getting started

### Set up dotenv

Set up .env under root directory

```
API_URL=http://localhost:8080/function
DISCORD_BOT_ID={your discord bot id}
DISCORD_BOT_TOKEN={your discord bot token}
OPENAI_API_KEY={your openai api key}
```

### Set up Discord Bot

1. Create your ChatGPT bot in https://discord.com/developers/applications
2. Check `MESSAGE CONTENT INTENT` under bot setting
3. Generate bot invitation url under OAuth2 setting
4. Invite bot the your channel

### Deploy OpenFaaS to local Kubernetes

Follow this [tutorial](https://docs.openfaas.com/deployment/kubernetes/):

```
0. Enable kubernetes in Docker Desktop

# Get arkade
1. curl -SLsf https://get.arkade.dev/ | sh

# Install OpenFaas
2. arkade install openfaas

# Get faas-cli
3. curl -SLsf https://cli.openfaas.com | sh

# Forward the gateway to your machine
4. kubectl rollout status -n openfaas deploy/gateway
5. kubectl port-forward -n openfaas svc/gateway 8080:8080 &

# If basic auth is enabled, you can now log into your gateway:
6. PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
7. echo -n $PASSWORD | faas-cli login --username admin --password-stdin

# Login Docker
8. docker login --username {docker user name}

# Set up stack.yml
9. Change it to "image: {docker user name}/chatgpt:latest"

# Build Docker images
10. faas-cli template pull https://github.com/openfaas-incubator/python-flask-template
11. faas-cli build stack.yml

# Push Docker images into the registry
12. faas-cli push stack.yml

# Deploys the functions into the OpenFaaS gateway
13. faas-cli deploy stack.yml
```
