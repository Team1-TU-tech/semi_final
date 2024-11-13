# spark-prometheus-grafana 

## USAGE
```
$ git clone https://github.com/Team1-TU-tech/semi_final.git
$ docker compose up -d

# DOCKER STOP
$ docker compose down
```

## METRICS
spark-master - http://localhost:8080/metrics/master/prometheus/  
spark-submit - http://localhost:4040/metrics/prometheus/

## SPARK

http://localhost:8080/

![image](https://github.com/user-attachments/assets/46440832-2717-4296-ab2b-26da727cc8a9)

## PROMETHEUS

http://localhost:9090/

![image](https://github.com/user-attachments/assets/47c741fa-fbd2-4b48-b972-a9ca835690c7)

## GRAFANA

http://localhost:3000/

필요한 쿼리를 추가하여 spark metrics 확인 가능

![image](https://github.com/user-attachments/assets/e03ed0c3-ce02-438a-ace3-d7ad41fdade5)

