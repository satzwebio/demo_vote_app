# demo_vote_app
kubectl port-forward svc/vote 32000:8080

docker build -t satzweb/examplevotingapp_vote:v5 .

docker push satzweb/examplevotingapp_vote:v5