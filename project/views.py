from django.shortcuts import render, redirect, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def main(request):
    return redirect('/admin')


def callback(request):
    return HttpResponse('a2bf185b')