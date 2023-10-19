# IoT Facial Authentication using AWS Rekognition

This is a Python application for capturing images from a camera, comparing them with a reference image, and logging the results. The system utilizes Amazon Web Services (AWS) for image storage and face recognition services.

## Getting Started

Before using this application, please ensure you have the following prerequisites:

- Python 3.10.11 installed in a virtual environment.
- AWS CLI configured with your API keys.

# OpenCV Install on RPi

Installing OpenCV using pip till take a lot of time and may be error prone. This is why it is better to install it using `apt`, which installs the prebuilt wheel

Run this command in the terminal:
```bash
sudo apt install python3-opencv
```

## Installation

1. Clone this repository:

2. Navigate to the project directory:

3. Initialize the python virtual environment:
   ```bash
   python -m venv venv
   ```

4. Install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project directory with the following content and replace `<YOUR_BUCKET_NAME>` and `<YOUR_BASE_FACE_FILE>` with your AWS S3 bucket name and the base face image file:

   ```
   bucket_name=<YOUR_BUCKET_NAME>
   base_face_file=<YOUR_BASE_FACE_FILE>
   ```

## AWS Configuration

Make sure you have configured AWS CLI with your credentials using the following command:

```bash
aws configure
```

Provide your AWS Access Key ID, Secret Access Key, region, and output format. Toggle on `Bucket Versioning` on your S3 bucket.

## Usage

To run the application, execute the `face_auth.py` script from the project directory:

```bash
python face_auth.py
```

Follow the on-screen instructions to allow the application to access your camera and detect faces. The application will capture an image if a face is detected and its quality is sufficient.

## Important Notes

- This application must be run from the project directory to correctly access the `.env` file and directories like `captured_images`, `logs`, `haarcascade` etc.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
