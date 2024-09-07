import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO
import qrcode
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']

clues = [
    {
        #add your clues here 
        #make sure you add /n for new line at the right places to format the pdf correctly
        "location": " ", #location goes here
        "location_clue": " ", #location clue goes here
        "question": " ", #question goes here
        "answer": " ",#password for the pdf goes here
        "next_location": " " #next location goes here
    }
]

def create_pdf(clue, password):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Location Clue:")
    y = 730
    for line in clue['location_clue'].split('\n'):
        c.drawString(120, y, line)
        y -= 20
    c.drawString(100, y-20, f"Question:")
    y -= 40
    for line in clue['question'].split('\n'):
        c.drawString(120, y, line)
        y -= 20
    c.save()

    buffer.seek(0)
    new_pdf = PdfReader(buffer)
    pdf_writer = PdfWriter()
    pdf_writer.add_page(new_pdf.pages[0])
    pdf_writer.encrypt(password)

    return pdf_writer

def generate_qr_code(data, filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

def get_google_drive_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def upload_to_drive(service, filename, mimetype):
    file_metadata = {'name': os.path.basename(filename)}
    media = MediaIoBaseUpload(BytesIO(open(filename, 'rb').read()), 
                              mimetype=mimetype, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, 
                                  fields='id, webViewLink').execute()
#edit it if u want to make it private
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(fileId=file['id'], body=permission).execute()
    
    return file.get('webViewLink')

def main():
    if not os.path.exists("qr_codes"):
        os.makedirs("qr_codes")

    service = get_google_drive_service()

    for i, clue in enumerate(clues):
        pdf_filename = f"clue_{i+1}.pdf"
        qr_filename = f"qr_codes/qr_clue_{i+1}.png"

        try:
            pdf = create_pdf(clue, clue['answer'])
            with open(pdf_filename, "wb") as output_file:
                pdf.write(output_file)

            #upload pdf to drive
            drive_link = upload_to_drive(service, pdf_filename, 'application/pdf')

            #generate qr code
            generate_qr_code(drive_link, qr_filename)

            print(f"Created PDF: {pdf_filename}")
            print(f"Uploaded to Google Drive: {drive_link}")
            print(f"Created QR code: {qr_filename}")
            print(f"Password for {pdf_filename}: {clue['answer']}")
            print(f"Next Location: {clue['next_location']}")
            print("---")

            # delete pdf local filename
            os.remove(pdf_filename)

        except Exception as e:
            print(f"Error processing clue {i+1}: {str(e)}")

    print("\nScavenger Hunt Setup Complete!")
    print("Remember to test all QR codes and PDFs before the event.")

if __name__ == "__main__":
    main()