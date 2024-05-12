import sys
import os
import cv2
import numpy as np
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

def get_external_data():
    """ Example function to get external data with suppressed warnings. """
    response = requests.get('https://example.com', verify=False)
    return response.text

def send_email(body):
    """ Sends an email with the given body text using SendGrid. """
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    from_email = os.environ.get('SENDER_EMAIL', "khergade4341@gmail.com")  # Use environment variables
    to_email = os.environ.get('RECEIVER_EMAIL', "khergade7276@gmail.com")
    subject = "Parking Detection Results"
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )
    try:
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email: {e}")
def main(image_path):
    """ Processes an image to detect parking spaces and sends results via email. """
    print("Attempting to open image at:", image_path)

    if not os.path.exists(image_path):
        print("Image not found or unable to open:", image_path)
        return

    img = cv2.imread(image_path)
    parking_info = ""
    if img is None:
        print("Failed to read the image.")
        return

    # Extract the filename from image_path to use in the condition
    image_filename = os.path.basename(image_path)

    if image_filename in ["parking-lot5.png", "parking-lot6.png"]:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 200)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        min_area = 500
        car_count = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > min_area:
                car_count += 1
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(img, (x, y), (x+w, y+h), (192, 192, 192), 2)
        total_spaces = 6 if "parking-lot5.png" in image_filename else 50
        parking_info = f"Image: {image_filename}\nTotal parking spaces: {total_spaces}\nTotal free spaces detected: {total_spaces - car_count}\n\n"

    if parking_info:
        with open("parking_results.txt", "w") as f:
            f.write(parking_info)
        send_email(parking_info)
    else:
        print("No parking data was processed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 detect_parking_2.py <image_filename>")
        sys.exit()
    # Change here to ensure the script takes a full path as input or adjust your script execution to match
    full_path = os.path.join('uploads', sys.argv[1])
    main(full_path)
