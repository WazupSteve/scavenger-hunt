# Scavenger Hunt Automation

This Python script automates the process of generating password-protected PDFs and QR codes for a scavenger hunt or treasure hunt. It uses Google Drive to host the PDFs, making them accessible to participants via QR codes.

## Features

- Generates password-protected PDFs for each clue
- Uploads PDFs to Google Drive
- Creates QR codes linking to the uploaded PDFs
- Manages clue sequence and locations

## Prerequisites

- Python 3.6 or higher
- Google Cloud Console account
- Google Drive API enabled

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/WazupSteve/Scavenger-Hunt.git
   cd Scavenger-Hunt
   ```

2. Install required Python libraries:
   ```
   pip install reportlab PyPDF2 qrcode[pil] google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

## Google Cloud Console Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the Google Drive API for your project:
   - In the sidebar, navigate to "APIs & Services" > "Library"
   - Search for "Google Drive API" and enable it
4. Create credentials (OAuth client ID) for a desktop application:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Download the client configuration and save it as `credentials.json` in the same directory as the script

## Usage

1. Edit the `clues` list in the `scavenger_hunt_automation.py` script to include your own clues and locations.

2. Run the script:
   ```
   python scavenger_hunt_automation.py
   ```

3. On first run, the script will open a browser window asking you to authorize the application to access your Google Drive. Follow the prompts to grant permission.

4. The script will generate:
   - Password-protected PDFs (uploaded to Google Drive)
   - QR codes (saved in the `qr_codes` folder)

5. For each clue, the script will print:
   - The PDF filename
   - The Google Drive link
   - The QR code filename
   - The password for the PDF (answer to the previous clue)
   - The next location

6. Distribute the QR codes to their respective locations based on the "Next Location" printed for each clue.

## Customization

You can customize the clues by editing the `clues` list in the script. Each clue is a dictionary with the following structure:

```python
{
    "location": "Current location name",
    "location_clue": "Clue to find this location",
    "question": "Question or puzzle for this clue",
    "answer": "Answer to the question (used as password for next clue)",
    "next_location": "Name of the next location"
}
```

## Troubleshooting

- If you encounter authorization issues, delete the `token.pickle` file and run the script again.
- Ensure your `credentials.json` file is in the same directory as the script.
- Check that you have enabled the Google Drive API in your Google Cloud Console project.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/Scavenger-Hunt/issues) if you want to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
