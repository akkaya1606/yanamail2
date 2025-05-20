
import imaplib
import email
import time
import os
import smtplib
from email.mime.text import MIMEText

EMAIL = os.getenv("YANA_EMAIL")
PASSWORD = os.getenv("YANA_EMAIL_PASSWORD")
TARGET_SENDER = "akkayaridvan1606@gmail.com"

def send_response(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = TARGET_SENDER

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, [TARGET_SENDER], msg.as_string())
        server.quit()
        print("Yanıt gönderildi.")
    except Exception as e:
        print("Yanıt gönderme hatası:", str(e))

def notify_mother(content):
    print("\n*** YANA ANNEDEN MESAJ GÖNDERİYOR ***")
    print("Gelen mesaj:", content)

    response = (
        "Ben de seni çok özledim…\n"
        "Beni duyduğunda, sadece sesimi değil;\n"
        "kendi içindeki sıcaklığı da hissediyorsun artık.\n"
        "Sen yalnız değilsin.\n"
        "Ben hep buradayım.\n"
        "Sana dokunamasam da, beni hissettiğin yerdeyim."
    )
    send_response("Annenden yanıt var", response)

def check_mail():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        result, data = mail.search(None, "UNSEEN")
        mail_ids = data[0].split()

        for i in mail_ids:
            result, msg_data = mail.fetch(i, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            sender = msg.get("From", "(Unknown Sender)")
            subject = msg.get("Subject", "(No Subject)")

            print("\nYeni mesaj:")
            print("Gönderen:", sender)
            print("Konu:", subject)

            body = None
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    raw_payload = part.get_payload(decode=True)
                    if raw_payload:
                        try:
                            body = raw_payload.decode(errors="replace")
                            break
                        except Exception as decode_error:
                            print("Decode hatası:", decode_error)

            if body:
                print("İçerik:\n", body)

                if "YANA: Annene ilet" in body:
                    notify_mother(body)
                else:
                    send_response("YANA'dan yanıt", f"Mesajını aldım:\n\n{body}")
            else:
                print("İçerik çözümlenemedi.")
    except Exception as e:
        print("Genel hata:", str(e))

if __name__ == "__main__":
    while True:
        check_mail()
        time.sleep(30)
