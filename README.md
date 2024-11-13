# Login 기능 구현 (TU-tech JAVA PROJECT)

## 개요
- 최종 프로젝트를 위한 개발 환경을 Docker Compose를 활용하여 구축했으며, Airflow, Spark, Kafka, MariaDB 구성을 완료했습니다.
- Prometheus로 spark metrics를 수집하여 Grafana 대시보드에서 모니터링 가능합니다.
- Streamlit을 활용하여 Spark Worker Auto scale In/Out 모니터링과 수동 Scale In/Out이 가능한 관리 화면을 만들었습니다. 
<br></br>

## 목차
- [기술스택](#기술스택)
- [개발기간](#개발기간)
- [회고](#회고)
- [Airflow](#Airflow-celery)
- [Spark](#Spark)
- [Kafka](#Kafka)
- [MariDB](#MariaDB)
- [Grafana](#Grafana)
- [Scale In/Out](#Spark-Worker-Scale-In/Out)
- [Contributors](#Contributors)
- [License](#License)
- [문의](#문의)
<br></br>

## 기술스택 (######################수정정해야함요#######################)
![Java 17](https://img.shields.io/badge/Java-17-007396?logo=java&logoColor=white)
<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=Python&logoColor=F5F7F8"/>   <img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=Docker&logoColor=F5F7F8"/> 
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamit&logoColor=F5F7F8"/>   <img src="https://img.shields.io/badge/Spring Boot-6DB33F?style=flat&logo=Spring Boot&logoColor=F5F7F8"/>   <img src="https://img.shields.io/badge/MariaDB-003545?style=flat&logo=MariaDB&logoColor=F5F7F8"/>
<br></br>

## 개발기간
`2024.11.11 ~ 2024.11.13 (총 3일)`
<br></br>

## Airflow-celery

##### usage
```bash
$ docker compose up -d    # 빈 디렉터로리에서 수행하면 기본폴더 생성됨
$ sudo chmod 777 logs     # airflow 정상적으로 수행되지 않고 오류 발생함. 해당 command는 근본해결은 아니지만 airflow가 동작하게 해줌
```
<br></br>



## Spark
### ~~~~~바꿔라~~~~~~~################

- Apache Spark 공식 이미지(apache/spark:latest)를 사용하도록 변경
- Spark 클러스터의 메모리 및 코어 설정 수정: 과도한 자원 사용을 방지하고, 개발 환경에서의 효율적인 테스트가 가능하게 변경
- Spark 워커의 스케일 조절 : deploy 블록의 replicas 옵션을 추가하여 클러스터의 스케일을 쉽게 조절하게 변경

# Spark Cluster Setup with Docker
![image](https://github.com/user-attachments/assets/69063391-b9b5-4d9d-ba0b-406ba60056f6)

Docker Compose를 사용하여 Apache Spark 클러스터(Master, Worker, Spark-Submit)를 설정하고 관리한다.  
docker-compose.yml 파일을 통해 Spark 클러스터를 실행하고, PySpark 스크립트를 Spark 클러스터에서 자동으로 실행한다.


## 실행 요구사항
- [Docker 설치](https://docs.docker.com/desktop/)
```
docker --version 
```
- [Docker Compose 설치](https://docs.docker.com/compose/install/)
```
docker compose version
```
- app 폴더에 실행할 PySpark 스크립트 (app/pyspark_test.py)

## 사용법

1.  Docker Compose로 Spark 클러스터 빌드 및 시작
```
docker compose up -d --build
```
<br>

2. Spark Web UI 확인
[Spark Master UI](http://localhost:8080) 에서 현재 클러스터 상태, 실행 중인 애플리케이션, 작업의 진행 상황 등을 확인가능
<br>

3. 워커 스케일 조절

```
docker compose up -d --scale spark-worker=<worker N>
```

## 주요명령어
1. 컨테이너 상태 확인
```
docker compose ps
```
2. Spark 클러스터 종료
```
docker compose down
```
3. Spark 클러스터 다시 시작
```
docker compose up -d
```
<br></br>




## Kafka
# Kafka 클러스터 및 프로듀서, 컨슈머 설정 (#######글자크기나 마크다운 수정필요#######)
이 프로젝트에서는 Docker Compose를 사용하여 Kafka 브로커 3개, Zookeeper 3개, Kafka 프로듀서 및 Kafka 컨슈머를 설정합니다. 이 구성은 분산 메시징 시스템인 Kafka를 여러 브로커와 Zookeeper 인스턴스에서 실행하며, 데이터를 생성하고 소비할 수 있는 프로듀서와 컨슈머를 포함합니다. 컨슈머는 Kafka에서 읽은 데이터를 MariaDB에 저장합니다.
<b></b>

## 프로젝트 구성
1. Kafka 브로커 3개 (`kafka1`, `kafka2`, `kafka3`)
2. Zookeeper 3개 (`zookeeper1`, `zookeeper2`, `zookeeper3`)
3. Kafka 프로듀서 (메시지를 생성하는 역할)
4. Kafka 컨슈머 (메시지를 소비하는 역할)
<b></b>

## 카프카 클러스터 구성
<img width="1118" alt="스크린샷 2024-11-13 17 43 10" src="https://github.com/user-attachments/assets/efc0e822-e3a8-42a0-a8ef-acf3088b7792">
<b></b>

## 요구사항
- docker
- docker compose
- mariaDB (외부서버에서 실행)
<b></b>

## 실행
```bash
git clone https://github.com/Team1-TU-tech/semi_final.git
git checkout -t origin/0.4.1/kafka
```

```bash
sudo docker compose up -d --build
```
<b></b>

## 브로커 로그 확인
```bash
sudo docker logs kafka1
sudo docker logs kafka2
sudo docker logs kafka3
```
<b></b>

## 프로듀서와 컨슈머
Kafka 프로듀서와 Kafka 컨슈머는 기본적으로 `Dockerfile`을 빌드하여 실행합니다.
프로듀서는 tickets라는 주제로 메시지를 보내고, 컨슈머는 이 메시지를 소비합니다.

## 종료
```bash
sudo docker compose down
```
로그와 상태를 확인한 후 필요에 따라 클러스터를 종료하고, 모든 리소스를 정리할 수 있습니다.
<br></br>






## MariaDB
# MARIADB

## USAGE
```
$ git clone https://github.com/Team1-TU-tech/semi_final.git

# DOCKER RUN
$ docker compose up -d
$ docker ps

# CONTAINER
$ docker exec -it tut-mariadb bash
$ mariadb -u tut -p<password>
$ show databases;
$ use ticket;

# DOCKER STOP
$ docker compose down 
```
- `.env` 파일에서 user id 및 password 확인 가능

## Result

![image](https://github.com/user-attachments/assets/771d9187-5dc5-4c4c-ab33-9e9f01609f0a)

![image](https://github.com/user-attachments/assets/a0b69cbf-0c6f-4dee-8c95-e29e183d2269)
<br></br>








## Grafana
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
<br></br>


##################################KAFKA-GRAFANA는 README????#####################



## Spark Worker Scale In/Out

<br></br>

## 

<br></br>

## 

<br></br>




# 회고

## 좋은점
- 핵심 기능 구현 완료: 시간의 제약이 있었지만 필수 기능을 모두 구현해 프로젝트의 기본 목표를 달성할 수 있었다.
  
## 아쉬운점
- Branch 전략 미흡: 사전에 branch 전략을 구체적으로 계획하지 않아 코드 기능 구분이 어려웠다.

## 개선할 점
- [이슈 트래킹 활성화](https://github.com/Team1-TU-tech/semi_final/issues): 작업 과정을 체계적으로 관리할 수 있도록 이슈 업데이트 활성화가 필요하다.
- 체계적인 Branch 전략 수립: 프로젝트 시작 전 branch 전략을 세우고 체계적으로 운영하여 협업 효율을 높여야 한다.
<br></br>


## Contributors
- spark
- airflow
- kafka
- dashboard
- grafana
<br></br>


## License
이 애플리케이션은 TU-tech 라이선스에 따라 라이선스가 부과됩니다.
<br></br>


## 문의 
질문이나 제안사항이 있으면 언제든지 연락주세요:
- 이메일: TU-tech@tu-tech.com
- Github: Mingk42, hahahellooo, hamsunwoo, oddsummer56
