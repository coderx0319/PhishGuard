import email
from email import policy
import hashlib

def extract_attachments(msg):
    attachments = []

    for part in msg.walk():
        content_disposition = part.get("Content-Disposition")

        if content_disposition and "attachment" in content_disposition:
            file_data = part.get_payload(decode=True)
            filename = part.get_filename()

            if file_data:
                sha256 = hashlib.sha256(file_data).hexdigest()

                attachments.append({
                    "filename": filename,
                    "sha256": sha256
                })

    return attachments


def parse_email(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        msg = email.message_from_file(f, policy=policy.default)

    headers = dict(msg.items())

    body = ""
    if msg.is_multipart():
     for part in msg.walk():
        content_type = part.get_content_type()

        if content_type == "text/plain":
            try:
                body += part.get_content()
            except:
                pass

        elif content_type == "text/html":
            try:
                body += part.get_content()
            except:
                pass
    else:
        body = msg.get_content()

    return {
        "headers": headers,
        "body": body,
        "attachments": extract_attachments(msg)
    }