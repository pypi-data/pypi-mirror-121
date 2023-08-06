from django.shortcuts import render
from google.cloud import storage
import os
import zipfile
from dotenv import load_dotenv
import shutil
from django.contrib.auth.forms import UserCreationForm

try:
    import io
    from io import BytesIO
    import pandas as pd
    from google.cloud import storage

except Exception as e:
    print("some modules are missing {}".format(e))

storage_Client = storage.Client.from_service_account_json("deft-melody-321207-aea054bd13bd.json")
# r = requests.get('https://console.cloud.google.com/storage/browser?project=deft-melody-321207&prefix=', timeout=250)

load_dotenv()
SOURCE_DIRECTORY = os.getenv('SOURCE_DIRECTORY')


def index(request):
    return render(request, "petrol/home.html")


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print(uploaded_file.name)
        print(uploaded_file.size)

        # directory = shutil.make_archive("/home/manisha18/blog/filename1", 'zip',"relativePath")
        # print("directory")

        bucket = storage_Client.get_bucket("example_bucketone")
        filename = 'class.zip'  # Store file in gcp with this filename
        blob = bucket.blob(filename)
        with open(uploaded_file.name, 'rb') as f:
            blob.upload_from_file(f)
        print("upload complete")
    return render(request, 'petrol/index.html')


def app(request):
    if request.method == 'POST':
        name1 = request.POST.get('u_name')  # u_name is the name of the input tag
        print(name1)
        if len(name1) != 0:

            directory = shutil.make_archive("/home/manisha18/blog/filename4", 'zip', name1)
            print(directory)

            bucket = storage_Client.get_bucket("example_bucketone")
            filename = 'log.zip'  # Store file in gcp with this filename
            blob = bucket.blob(filename)
            with open(directory, 'rb') as f:
                blob.upload_from_file(f)
            print("upload complete")
            return render(request, 'petrol/ota.html', {"form": UserCreationForm(), "success": "upload complete"})
        else:
            return render(request, 'petrol/ota.html', {"form": UserCreationForm(), "error": "please enther the path"})

    return render(request, 'petrol/ota.html')


def download(request):
    storage_client = storage.Client.from_service_account_json("deft-melody-321207-aea054bd13bd.json")
    bucket = storage_client.get_bucket('example_bucketone')
    blob = bucket.blob("wild.zip")
    blob.download_to_filename('/home/manisha18/blog/dev.zip')
    print("download complete")
    return render(request, 'petrol/index.html')


def example(request):
    if request.method == 'POST':
        name1 = request.POST.get('downloaded_file')  # u_name is the name of the input tag
        print(name1)
        if len(name1) != 0:
            client = storage.Client.from_service_account_json("deft-melody-321207-aea054bd13bd.json")
            object_name = 'wild.zip'
            bucket = client.bucket('example_bucketone')
            blob = storage.Blob(object_name, bucket)
            blob.download_to_filename('cloud.zip')

            with zipfile.ZipFile("cloud.zip", "r") as zip_ref:
                zip_ref.extractall(name1)
                print(name1)
            print("extract complete")
            return render(request, 'petrol/ota.html', {"form": UserCreationForm(), "success": "extract complete"})
        else:
            return render(request, 'petrol/ota.html', {"form": UserCreationForm(), "error": "please enther the path"})

    return render(request, 'petrol/otadownload.html')


