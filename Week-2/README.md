
Copy the dev.env to .env file, storing secrets in the .env and making sure the .gitignore includes '.env'.
```bash
cp dev.env .env
```

Update the mage container to the latest vesion
```bash
docker pull mageai/mageai:latest
```


## Mage variables

Environment varaible: System scope: Created in code: {{ env_var() }}
Runtime variable: Pipeline scope: Created in code or UI: kwargs or {{ variables() }}
Block variable: Block scope: Created in code or UI: kwargs['configuration][key]
Secret: Project scope: Created in UI: {{ mage_secret_var() }}: ENCRYPTED.