#! / usr / bin / python3.6
# -- coding: UTF-8 --
import os, sys

import numpy as np
import matplotlib.pyplot as plt

import ffmpeg as ff
import imageio as ie
import ffprobe as fp
import time
import boto3

import pydub as pyd

#from pydub import AudioSegment

#librerias instaladas con pip3:
#ffmpeg
#imageio
#imageio-ffmpeg
#matplotlib
#numpy
#Pydub


location = "/home/rasmus/Documentos/Dataset/VideosProvisionales/"
file = "Qbit.mp4"

#objeto de lectura
vid_reader= ie.get_reader(location+file)
#metadata del video
metaData= vid_reader.get_meta_data()

print(metaData)

#Conversión de Video a Array

frames = vid_reader.count_frames()
dimensions = (frames, metaData['source_size'][1], metaData['source_size'][0],3)

v = location+file

pyd.AudioSegment.from_file(v).export("/home/rasmus/Documentos/Dataset/Audios/audio.mp3", format="mp3")

#Definicón para la conexión y traducción del audio a texto
def transcribe_file(job_name, file_uri, transcribe_client):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='wav',
        LanguageCode='es-ES'
    )

    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            if job_status == 'COMPLETED':
                print(
                    f"\tDownload the transcript from\n"
                    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}.")
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)

# Definición de los procesos
def main():
    transcribe_client = boto3.client('transcribe')
    file_uri = 's3://anniqteams/Prueba.wav'
    transcribe_file('Example-job', file_uri, transcribe_client)


if __name__ == '__main__':
    main()