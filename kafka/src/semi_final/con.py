from kafka import KafkaConsumer, TopicPartition
from json import loads
import os
from db import get_conn
import yaml
from time import sleep

# YAML 설정 파일 불러오기
with open("/app/kafka-config.yaml", 'r') as f:
    config = yaml.safe_load(f)

consumer_config = config['kafka']['consumer']

def create_kafka_consumer(retries=5, delay=5):
    for attempt in range(retries):
        try:
            consumer = KafkaConsumer(
                    consumer_config['topics'][0],
                    bootstrap_servers=consumer_config['bootstrap_servers'],
                    group_id=consumer_config['group_id'],
                    auto_offset_reset=consumer_config['auto_offset_reset'],
                    enable_auto_commit=consumer_config['enable_auto_commit'],
                    value_deserializer=lambda x: loads(x.decode('utf-8'))
                    )
            print("Kafka Consumer 연결 성공")
            return consumer

        except Exception as e:
            print(f"Kafka 브로커가 준비되지 않음. {delay}초 후 다시 시도 ({attempt+1}/{retries})")
            sleep(delay)

    print("Kafka 브로커에 연결할 수 없습니다.")
    return None


# 컨슈머 생성 시도
consumer = create_kafka_consumer()

if consumer:
    print('[Start] get consumer')
    try:
        # 데이터베이스 연결 초기화
        conn = get_conn()
        cursor = conn.cursor()

        # Kafka 메시지 수신 및 데이터베이스 저장 루프
        for message in consumer:
            ticket_data = message.value
            print(f"Received: {ticket_data}")

            # 데이터베이스에 데이터 저장
            try:
                # 연결이 열려 있는지 확인하고, 닫혀 있으면 재연결
                if not conn.open:
                    print("Database connection is closed. Reconnecting...")
                    conn = get_conn()
                    cursor = conn.cursor()

                # 데이터베이스에 데이터 삽입
                cursor.execute(
                    '''
                    INSERT INTO ticket_data (event_name, price, date, location, available_tickets)
                    VALUES (%s, %s, %s, %s, %s)
                    ''',
                    (ticket_data['event_name'], ticket_data['price'], ticket_data['date'], ticket_data['location'], ticket_data['available_tickets'])
                )
                conn.commit()  # 각 메시지 처리 후 커밋하여 DB에 반영
                print("Data saved to database.")

                # 오프셋 수동 커밋
                consumer.commit()  # 메시지가 정상적으로 처리된 후에만 커밋

            except Exception as e:
                print(f"Error occurred while inserting data: {e}")
                conn.rollback()  # 오류 시 롤백하여 데이터 정합성 유지

    except KeyboardInterrupt:
        print("Consumer stopped by user.")
    finally:
        # Consumer와 DB 연결 닫기
        consumer.close()
        if conn.open:  # 연결이 열린 경우에만 닫기
            cursor.close()
            conn.close()
            print("Database connection closed.")

    print('[End] get consumer')

else:
    print("컨슈머 연결 실패로 종료")

