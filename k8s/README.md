### Как запустить
Заполнить .env записями POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD  
Создать секрет kubectl create secret generic webapp-secrets --from-env-file=.env  
kubectl apply -f ./configmap.yml  
kubectl apply -f ./pg  
kubectl apply -f ./users_reader  
kubectl apply -f ./users_writer  
kubectl apply -f ./webapp  
kubectl apply -f ./filldb.yml