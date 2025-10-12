import os
import google.generativeai as genai
from google.genai import types

model_list = genai.list_models()
for m in model_list:
    print(m.name, m.supported_generation_methods)
