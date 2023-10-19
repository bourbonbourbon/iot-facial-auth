import cv2
import json
import boto3
import botocore
from datetime import datetime
from dotenv import dotenv_values


def aws_init():
    s3 = boto3.client("s3")
    reko = boto3.client("rekognition")
    return s3, reko


def init_cam():
    cam = cv2.VideoCapture(0)
    print("Starting camera...")
    cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    cam.set(cv2.CAP_PROP_FOCUS, 360)
    cam.set(cv2.CAP_PROP_BRIGHTNESS, 130)
    cam.set(cv2.CAP_PROP_SHARPNESS, 125)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    face_cascade = cv2.CascadeClassifier(
        "./haarcascade/haarcascade_frontalface_default.xml")
    return cam, face_cascade


def destory_cam(cam):
    cv2.destroyAllWindows()
    cam.release()


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


def take_pictures():
    cam, face_cascade = init_cam()
    pic_taken = False
    first_loop = True
    while (True):
        if first_loop:
            print("Detecting faces and taking pictures...")
            print("Try to stay still...")
            first_loop = False
        result, image = cam.read()
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(
            gray_img,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40, 40)
        )
        if result:
            var = variance_of_laplacian(image)
            if var > 30 and len(face) != 0:
                capture_filename = datetime.now().strftime(f"%d-%m-%Y_%H-%M-%S.jpg")
                cv2.imwrite(f"./captured_images/{capture_filename}", image)
                pic_taken = True
                print("Picture taken.")
                break
    destory_cam(cam)
    return capture_filename, pic_taken


def get_config_values():
    config = dotenv_values(".env")
    bucket = config["bucket_name"]
    base_face = config["base_face_file"]
    return bucket, base_face


def upload_image(s3, bucket, capture_filename, pic_taken):
    print(f"Uploading ./captured_images/{capture_filename}...")
    is_uploaded = False
    if pic_taken:
        with open(f"./captured_images/{capture_filename}", "rb") as data:
            try:
                s3.upload_fileobj(
                    data,
                    bucket,
                    capture_filename
                )
                is_uploaded = True
            except botocore.exceptions.ClientError as error:
                print(error)
    if is_uploaded:
        print("Picture file uploaded.")


def print_output(result):
    print("\n")
    for match in result["FaceMatches"]:
        print(
            f"Similarity between compared faces is {result['FaceMatches'][0]['Similarity']}")
    for nomatch in result["UnmatchedFaces"]:
        print("Faces either don't match or are a poor match")
    print("\n")


def log_output(capture_filename):
    print(f"Logging to file ./logs/face_capture_time_log.txt...")
    with open("./logs/face_capture_time_log.txt", "a") as log_file:
        log_file.write(f"{capture_filename.split('.')[0]}\n")
    print("Done logging.")


def compare_face(reko, bucket, capture_filename, base_face, threshold=85):
    print("Comparing picture...")
    success = False
    try:
        response = reko.compare_faces(
            SourceImage={
                "S3Object": {
                    "Bucket": bucket,
                    "Name": base_face
                }
            },
            TargetImage={
                "S3Object": {
                    "Bucket": bucket,
                    "Name": capture_filename
                }
            },
            SimilarityThreshold=threshold,
        )
        success = True
    except botocore.exceptions.ClientError as error:
        print(error)
    if success:
        print("Picture succesfully compared.")
    result = json.loads(json.dumps(response))
    print_output(result)
    log_output(capture_filename)


def upload_log_file(s3, bucket):
    print("Uploading log file...")
    is_uploaded = False
    with open("./logs/face_capture_time_log.txt", "rb") as data:
        try:
            s3.upload_fileobj(
                data,
                bucket,
                "face_capture_time_log.txt"
            )
            is_uploaded = True
        except botocore.exceptions.ClientError as error:
            print(error)
    if is_uploaded:
        print("Log file uploaded.")


if __name__ == "__main__":
    print("Starting application...")

    capture_filename, pic_taken = take_pictures()

    bucket, base_face = get_config_values()
    s3, reko = aws_init()

    upload_image(s3, bucket, capture_filename, pic_taken)
    compare_face(reko, bucket, capture_filename, base_face)
    upload_log_file(s3, bucket)

    print("Exiting application...")
