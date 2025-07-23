# OCR to Web

OCR to Web is a project designed to take images or PDFs containing text and convert them into structured, readable markdown or JSON formats, leveraging image and PDF analysis with OCR capabilities.

## Features

- Process images and PDFs to extract and convert text content.
- Outputs converted data as JSON for easy parsing and integration.
- Supports PDF and common image formats: PNG, JPG, JPEG.
- Utilizes the Typhoon API for OCR processing.

## Installation

To set up the project, you'll need to have Python installed along with the required libraries.

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd ocr_to_web
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure `poppler` is installed on your system for PDF processing:

   - **Windows**: [Download here](https://github.com/oschwartz10612/poppler-windows/releases/)
   - **macOS**: Run `brew install poppler`
   - **Linux**: Run `sudo apt-get install poppler-utils`

## Usage

1. Modify `filename` in `ocr.py` to point to your desired file for processing.
2. Run the OCR process:

   ```bash
   python ocr.py
   ```

3. The output will be displayed in the console.

## Configuration

- **API Key**: Add your Typhoon API Key in `ocr.py`.
- **Task Type**: Choose the task type (`"default"` or `"structure"`) based on your OCR needs.

## Requirements

- Python 3.x
- Flask, Flask-Cors, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- Pillow for image processing
- PyPDF2 for PDF processing
- OpenAI, Google Generative AI, pymongo, bcrypt, PyJWT for additional functionalities

## License

This project is licensed under the MIT License.

