import requests
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer

# --- Scrape and save jobs ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def scrape_and_save_jobs(request):
    url = "https://www.python.org/jobs/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    job_list = soup.find("ol", class_="list-recent-jobs")
    added_jobs = []

    for job_item in job_list.find_all("li"):
        title_tag = job_item.find("h2", class_="listing-company")
        location_tag = job_item.find("span", class_="listing-location")
        date_tag = job_item.find("time")
        link_tag = job_item.find("a")

        title = title_tag.text.strip() if title_tag else ""
        location = location_tag.text.strip() if location_tag else ""
        publish_date = date_tag.text.strip() if date_tag else ""
        detail_link = "https://www.python.org" + link_tag['href'] if link_tag else ""

        # Avoid duplicate entries based on detail_link
        if not Job.objects.filter(detail_link=detail_link).exists():
            job = Job.objects.create(
                title=title,
                location=location,
                publish_date=publish_date,
                detail_link=detail_link
            )
            added_jobs.append(job)

    serializer = JobSerializer(added_jobs, many=True)
    return Response({
        "message": f"{len(added_jobs)} new jobs added.",
        "new_jobs": serializer.data
    })


# --- View saved jobs ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_saved_jobs(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)
