from django.shortcuts import render
from django.http import JsonResponse
from .serializers import ResumeSerializer
from .models import Resume
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .parse.parse import Parse
import pathlib
import os
from django.conf import settings
# Create your views here.

# List All
@api_view(['GET'])
def ResumeList(request):
    resumes = Resume.objects.all()
    serializer = ResumeSerializer(resumes, many= True)
    return Response(serializer.data)

@api_view(['GET'])
def ResumeDetail(request,pk):
    resume = Resume.objects.get(id=pk)
    serializer = ResumeSerializer(resume, many= False)
    return Response(serializer.data)
# Create Resume
@api_view(['POST'])
@parser_classes([MultiPartParser,FormParser])
def ResumeCreate(request, format=None):
    serializer = ResumeSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
        
    

# Parse(update) Resume
@api_view(['PUT'])
def ResumeParse(request,pk):
    resumeOBJ = Resume.objects.get(id=pk)
    base_dir =settings.MEDIA_ROOT
    file = base_dir + resumeOBJ.resume.url
    print(file)
    file = file.replace('/media/media','/media')
    print(file)
    parsed_data = Parse(file)
    resumeOBJ.text = parsed_data['text']
    resumeOBJ.phone = parsed_data['phone']
    resumeOBJ.email = parsed_data['email']
    resumeOBJ.skills = parsed_data['skills']
    resumeOBJ.designation = parsed_data['designation']
    resumeOBJ.name = parsed_data['name']
    resumeOBJ.degree = parsed_data['degree']
    resumeOBJ.college = parsed_data['college']
    resumeOBJ.experience = parsed_data['experience']
    if resumeOBJ.is_parsed == False:
        resumeOBJ.is_parsed = not resumeOBJ.is_parsed
    serializer = ResumeSerializer(instance=resumeOBJ, data=request.data,many=False)
    if serializer.is_valid():
        serializer.save()
        resumeOBJ.save()
    print(serializer.errors)

    return Response(serializer.data)


@api_view(['DELETE'])
def ResumeDelete(request,pk):
    resume = Resume.objects.get(id=pk)
    resume.delete()
    return Response("Resume Deleted!")