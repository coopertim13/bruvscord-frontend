import tkinter as tk
import requests
import json
import threading

window = tk.Tk(className='Bruvscord')
window.geometry("1000x500")

labels = []
for i in range(6):
    labels.append(tk.Label(window, font=("Courier", 14),
                  width=1000, padx=20, pady=10, fg="white"))


def getMessagesReverse():
    messages = requests.get(
        "https://bruvscord.herokuapp.com/messages?order=desc&num=6")
    return json.loads(messages.content.decode())


def sendMessage(name, message):
    data = {"message": message}
    addMessage = requests.post(
        f"http://bruvscord.herokuapp.com/messages/add/{name}", data=data)
    return addMessage.content.decode()


def getUsers():
    users = requests.get("https://bruvscord.herokuapp.com/users")
    return json.loads(users.content.decode())


def fillContent():
    allMessages = getMessagesReverse()
    users = getUsers()
    for i in range(6):
        labels[i]["text"] = f"{allMessages[i]['sender']} says: {allMessages[i]['content']}"
        found = False
        for user in users:
            if user["name"] == allMessages[i]["sender"]:
                labels[i]["bg"] = user["color"]
                found = True
        if not found:
            labels[i]["bg"] = "#abc123"


T = tk.Text(window, height=5, width=52)
T.pack()


def sendMessagePrepare():
    content = T.get("1.0", "end").strip()
    sender = "callan"
    sendMessage(sender, content)


b1 = tk.Button(window, text="Send Message", command=sendMessagePrepare)
b1.pack()

for each in labels:
    each.pack(padx=10, pady=10)


def f(f_stop):
    fillContent()
    if not f_stop.is_set():
        t = threading.Timer(0.1, f, [f_stop])
        t.daemon = True
        t.start()


f_stop = threading.Event()
f(f_stop)

window.mainloop()
