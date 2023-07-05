import tkinter as tk
import sqlite3
from confluent_kafka.admin import AdminClient, NewTopic

# Kafka configuration
# Replace with your Kafka bootstrap servers
bootstrap_servers = 'your_bootstrap_servers'


def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf


def create_kafka_topic(topic_code):
    admin_client = AdminClient(read_ccloud_config("client.properties"))
    topic_list = []
    topic_list.append(NewTopic(topic_code, 1, 1))
    admin_client.create_topics(topic_list)
    print("Topic was Created Successfully")


def save_timetable():
    subject = subject_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()
    course_code = course_code_entry.get()
    topic_code = topic_code_entry.get()

    conn = sqlite3.connect('timetable.db')
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS timetable (subject TEXT, start_time TEXT, end_time TEXT, course_code TEXT, topic_code TEXT)')
    c.execute('INSERT INTO timetable VALUES (?, ?, ?, ?, ?)',
              (subject, start_time, end_time, course_code, topic_code))

    conn.commit()
    conn.close()

    subject_entry.delete(0, tk.END)
    start_time_entry.delete(0, tk.END)
    end_time_entry.delete(0, tk.END)
    course_code_entry.delete(0, tk.END)
    topic_code_entry.delete(0, tk.END)

    create_kafka_topic(topic_code)

    status_label.config(text="Timetable saved successfully!", fg="green")


window = tk.Tk()
window.title("Timetable Input")
window.geometry("400x250")

title_label = tk.Label(window, text="Timetable Input", font=("Arial", 16))
title_label.pack(pady=10)

form_frame = tk.Frame(window)
form_frame.pack()

subject_label = tk.Label(form_frame, text="Subject:", font=("Arial", 12))
subject_label.grid(row=0, column=0, padx=5, pady=5)
subject_entry = tk.Entry(form_frame, font=("Arial", 12))
subject_entry.grid(row=0, column=1, padx=5, pady=5)

start_time_label = tk.Label(form_frame, text="Start Time:", font=("Arial", 12))
start_time_label.grid(row=1, column=0, padx=5, pady=5)
start_time_entry = tk.Entry(form_frame, font=("Arial", 12))
start_time_entry.grid(row=1, column=1, padx=5, pady=5)

end_time_label = tk.Label(form_frame, text="End Time:", font=("Arial", 12))
end_time_label.grid(row=2, column=0, padx=5, pady=5)
end_time_entry = tk.Entry(form_frame, font=("Arial", 12))
end_time_entry.grid(row=2, column=1, padx=5, pady=5)

course_code_label = tk.Label(
    form_frame, text="Course Code:", font=("Arial", 12))
course_code_label.grid(row=3, column=0, padx=5, pady=5)
course_code_entry = tk.Entry(form_frame, font=("Arial", 12))
course_code_entry.grid(row=3, column=1, padx=5, pady=5)

topic_code_label = tk.Label(form_frame, text="Topic Code:", font=("Arial", 12))
topic_code_label.grid(row=4, column=0, padx=5, pady=5)
topic_code_entry = tk.Entry(form_frame, font=("Arial", 12))
topic_code_entry.grid(row=4, column=1, padx=5, pady=5)

save_button = tk.Button(window, text="Save", command=save_timetable, font=(
    "Arial", 12), bg="#4CAF50", fg="white")
save_button.pack(pady=10)

status_label = tk.Label(window, text="", font=("Arial", 12))
status_label.pack()

window.mainloop()
