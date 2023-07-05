import sqlite3

from datetime import datetime, timedelta

from confluent_kafka import Producer


def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf


def send_message_to_topic(topic, message):
    producer = Producer(read_ccloud_config("client.properties"))
    producer.produce("topic_0", value=message)
    producer.flush()
    print("Message was sent successfully")


def check_course_start_times():
    conn = sqlite3.connect('timetable.db')
    c = conn.cursor()

    current_time = datetime.now()
    notification_time = current_time - timedelta(minutes=45)

    c.execute("SELECT subject, topic_code, start_time FROM timetable")
    rows = c.fetchall()

    for row in rows:
        start_time_tt = datetime.strptime(row[2], '%H:%M')
        start_time = datetime(current_time.year, current_time.month,
                              current_time.day, start_time_tt.hour, start_time_tt.minute)

        notification_datetime = datetime(current_time.year, current_time.month,
                                         current_time.day, start_time.hour, start_time.minute) - timedelta(minutes=11)

        if notification_datetime <= current_time <= start_time:
            if current_time >= notification_datetime:
                topic = row[0]
                message = f'{row[0]} is about to start in 45 minutes!'
                send_message_to_topic(topic, message)

    conn.close()


check_course_start_times()
