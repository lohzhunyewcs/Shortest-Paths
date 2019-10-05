from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from path_finder.path import findpath, getMaxID, getGraph
import base64

import json
import cv2
import numpy as np
import requests

# Create your views here.
def index(request):
    context = {
        'vertices': getGraph().vertices,
    }
    return render(request, "find_path/index.html", context)

@csrf_exempt
def getpath(request):
    
    jsonFile = json.loads((request.body.decode("utf-8")))
    src = int(jsonFile['source'])
    dest = int(jsonFile['dest'])
    # print(f'choice: {choice}')    
    customer = False
    path, dist = findpath(src, dest, customer)
    return JsonResponse(json.dumps(({'path': path, 'dist': dist})), safe=False)
