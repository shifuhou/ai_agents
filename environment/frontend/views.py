import os
import string
import random
import json
from os import listdir
import os
import datetime
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from global_methods import *

import sqlite3



from .models import *



def home(request):
  
  
  conn = sqlite3.connect('aiagents_database.db')
  cursor = conn.cursor()
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS personas (
        id TEXT PRIMARY KEY,
        jsfile TEXT NOT NULL,
        date_posted DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
  conn.commit()
  f_curr_sim_code = "temp_storage/curr_sim_code.json"
  f_curr_step = "temp_storage/curr_step.json"

  if not check_if_file_exists(f_curr_step): 
    context = {}
    template = "home/error_start_backend.html"
    return render(request, template, context)

  with open(f_curr_sim_code) as json_file:  
    sim_code = json.load(json_file)["sim_code"]
  
  with open(f_curr_step) as json_file:  
    step = json.load(json_file)["step"]


  # os.remove(f_curr_step)

  new_persona_names_set =[]
  for i in find_filenames(f"/home/shifu/ai_agents/environment/static/assets/characters/original", ""): 
      x = i.split("/")[-1].strip()
      if x[0] != ".":
          x = x[:-4]
          new_persona_names_set.append(x)

  


  persona_names = {}
  cursor.execute("SELECT * FROM personas")
  rows = cursor.fetchall()
  for row in rows:

    persona = json.loads(row[1])
    persona_names[persona['name']] = persona
  # for i in find_filenames(f"environment/data/personas", ".json"):
  #   x = i.split("/")[-1].strip()
  #   if x[0] != ".":
  #     x = x[:-4]
  #     with open(i) as json_file: 
  #       persona = json.load(json_file)
  #       persona_names[persona['name']] = persona


  # print(persona_names)
  context = {"sim_code": sim_code,
             "step": step, 
             "persona_names": json.dumps(persona_names),
             'new_persona_names_set':new_persona_names_set,
             "mode": "simulate"}
  template = "home.html"
  return render(request, template, context)

def move(request):
  data = json.loads(request.body)
  conn = sqlite3.connect('aiagents_database.db')
  cursor = conn.cursor()
  cursor.execute("UPDATE personas SET jsfile=? WHERE id=?", (json.dumps(data), data['name']))
  conn.commit()
  # with open(f"environment/data/personas/{data['name']}.json", 'w') as file:
  #   json.dump(data,file,indent=4)
  res = {
      "message": "received"
  }
  return JsonResponse(res)

def update_persona(request):
  persona_names = {}
  conn = sqlite3.connect('aiagents_database.db')
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM personas")
  rows = cursor.fetchall()
  for row in rows:
    persona = json.loads(row[1])
    persona_names[persona['name']] = persona

  # for i in find_filenames(f"environment/data/personas", ".json"):
  #   x = i.split("/")[-1].strip()
  #   if x[0] != ".":
  #     x = x[:-4]
  #     with open(i) as json_file: 
  #       try:
  #         persona = json.load(json_file)
  #         persona_names[persona['name']] = persona
  #       except:
  #         print(json_file)
  #         lines = json_file.read()
  #         print(lines)

  return JsonResponse(persona_names)

def new_persona(request):

  data = json.loads(request.body)

  conn = sqlite3.connect('aiagents_database.db')
  cursor = conn.cursor()
  cursor.execute("INSERT INTO personas (id, jsfile) VALUES (?, ?)", (data['name'] , json.dumps(data) ))
  conn.commit()
  # with open(f"environment/data/personas/{data['name']}.json", 'w') as file:
  #   json.dump(data,file,indent=4)
  # print(data)

  res = {
        "message": "received"
    }
  return JsonResponse(res)


def process_environment(request): 
  """
  <FRONTEND to BACKEND> 
  This sends the frontend visual world information to the backend server. 
  It does this by writing the current environment representation to 
  "storage/environment.json" file. 

  ARGS:
    request: Django request
  RETURNS: 
    HttpResponse: string confirmation message. 
  """
  # f_curr_sim_code = "temp_storage/curr_sim_code.json"
  # with open(f_curr_sim_code) as json_file:  
  #   sim_code = json.load(json_file)["sim_code"]

  data = json.loads(request.body)
  step = data["step"]
  sim_code = data["sim_code"]
  environment = data["environment"]

  with open(f"storage/{sim_code}/environment/{step}.json", "w") as outfile:
    outfile.write(json.dumps(environment, indent=2))

  return HttpResponse("received")


def update_environment(request): 
  """
  <BACKEND to FRONTEND> 
  This sends the backend computation of the persona behavior to the frontend
  visual server. 
  It does this by reading the new movement information from 
  "storage/movement.json" file.

  ARGS:
    request: Django request
  RETURNS: 
    HttpResponse
  """
  # f_curr_sim_code = "temp_storage/curr_sim_code.json"
  # with open(f_curr_sim_code) as json_file:  
  #   sim_code = json.load(json_file)["sim_code"]

  data = json.loads(request.body)
  step = data["step"]
  sim_code = data["sim_code"]

  response_data = {"<step>": -1}
  if (check_if_file_exists(f"storage/{sim_code}/movement/{step}.json")):
    with open(f"storage/{sim_code}/movement/{step}.json") as json_file: 
      response_data = json.load(json_file)
      response_data["<step>"] = step

  return JsonResponse(response_data)



def landing(request): 
  context = {}
  template = "landing/landing.html"
  return render(request, template, context)
