
# -*- coding: utf-8 -*-

import os
import csv
import isodate

import google.oauth2.credentials

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

#Old data
#INPUT_FILE = 'D:\\giuly\\Desktop\\Progetto ML3 YouTube\\ML5-MINERVA-EducationaVideosClassifier-master\\dataset.csv'
#OUTPUT_FILE = 'data\\old_data_update.csv'

#New data
INPUT_FILE = 'data\\edu_videos_clean.csv'
OUTPUT_FILE = 'data\\edu_videos_update.csv'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def print_response(response):
  print(response)

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.iteritems():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def videos_list_by_id(client, **kwargs):
  # See full sample for function
  #kwargs = remove_empty_kwargs(**kwargs)

  response = client.videos().list(
    **kwargs
  ).execute()

  videos = response['items']

  with open(OUTPUT_FILE, 'a', newline='', encoding="utf8") as output:
    writer = csv.writer(output)
    for video in videos:
      videoId = video['id']
      title = '' if 'title' not in video['snippet'] else video['snippet']['title']
      author = '' if 'channelTitle' not in video['snippet'] else video['snippet']['channelTitle']
      viewCount = '' if 'viewCount' not in video['statistics'] else video['statistics']['viewCount']
      likes = '' if 'likeCount' not in video['statistics'] else video['statistics']['likeCount']
      dislikes = '' if 'dislikeCount' not in video['statistics'] else video['statistics']['dislikeCount']
      tags = '' if 'tags' not in video['snippet'] else ','.join(video['snippet']['tags'])
      duration = isodate.parse_duration(video['contentDetails']['duration'])
      lengthSeconds = duration.total_seconds()
      writer.writerow([videoId,title,author,viewCount,likes,dislikes,tags,lengthSeconds])

  #return print_response(response['pageInfo'])

def get_videos_id():
  videosID = []
  with open(INPUT_FILE, encoding="utf8") as input:
    for row in csv.reader(input):
      if row:
        #print(row)
        videoId = row[0].replace('/watch?v=','')
        videosID.append(videoId)

  f = lambda A, n=50: [A[i:i+n] for i in range(0, len(A), n)]
  splitted_videos = f(videosID)
  return splitted_videos



if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification. When
  # running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  client = get_authenticated_service()

  with open(OUTPUT_FILE, 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerow(['videoId','title','author','viewCount','likes','dislikes','tags','lengthSeconds'])
    

  splitted_videos = get_videos_id()
  for videos in splitted_videos:
    videosID = ",".join(videos)
    #print(videosID)

    videos_list_by_id(client,
      part='snippet,contentDetails,statistics',
      id=videosID)
  