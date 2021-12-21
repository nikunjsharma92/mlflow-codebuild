import boto3
import os

s3 = boto3.resource('s3') # assumes credentials & configuration are handled outside python in .aws directory or environment variables

def download_s3_folder(bucket_name, s3_folder, local_dir=None):
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=s3_folder):
        target = obj.key if local_dir is None \
            else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        if obj.key[-1] == '/':
            continue
        bucket.download_file(obj.key, target)


if __name__ == '__main__':
	local_dir = "./artifact_downloads"


	if not os.path.exists(local_dir):
	    os.mkdir(local_dir)

	download_s3_folder(os.getenv("MLFLOW_S3_BUCKET", "mlflow-ds-platform"), os.getenv("MLFLOW_ATRIFACT_PATH", "mlflow/artifacts/7/83643edb89e54317a8034ac3a7304fe6/artifacts/eswine4"), local_dir)

# "mlflow/artifacts/7/83643edb89e54317a8034ac3a7304fe6/artifacts/eswine4"
	cmd = '''
FROM ubuntu:21.04
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y wget

WORKDIR app
COPY . .


RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda
ENV PATH=/miniconda/bin:$PATH

RUN conda env create -f artifact_downloads/conda.yaml

RUN pip install -r artifact_downloads/requirements.txt
RUN pip install -r requirements.txt
RUN chmod +x run_server.sh

CMD ['./run_server.sh']
	'''
	with open("Dockerfile", "w") as text_file:
		text_file.write(cmd)
	
	# import subprocess
	# print("Creating Image: ", os.getenv("IMAGE_NAME", '12345'))
	# p = subprocess.Popen('docker build . -t '+os.getenv("IMAGE_NAME", '12345'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	# for line in p.stdout.readlines():
	#     print(line, flush=True)
	# retval = p.wait()

