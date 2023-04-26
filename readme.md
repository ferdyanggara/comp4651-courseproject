discord bot token
MTEwMDY0MjYwNTUyMTQ1MzExNw.GW_tlr.dJ8OWri3AUqUmjU7vRmTeMhO8zf_n7tz545oHo

deploy openfaas/opennfsw function 

1. download faas-cli on your local machine 
2. run this command `
faas-cli deploy -y stack.yml
`
3. start the gateway and forward gateway port in kubernetes to your localhost using these commands: 

- kubectl rollout status -n openfaas deploy/gateway
- kubectl port-forward -n openfaas svc/gateway 8080:8080 &

connection issue may rises with discord bot, just reconnect your wifi


# comp4651-courseproject
