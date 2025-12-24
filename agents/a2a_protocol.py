def send_message(sender, receiver, payload):
    message = {
        "from": sender,
        "to": receiver,
        "payload": payload
    }
    print("[A2A]", message)
    return message
