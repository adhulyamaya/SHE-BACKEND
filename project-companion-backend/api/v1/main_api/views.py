
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.v1.main_api.serializers import CountrySerializer, StateSerializer
from companion.models import Companion
from main.models import Country, State
from mentor.models import Mentor
from project.models import Project
from django.db.models import Count
from api.v1.pagination.pagination import SetPagination,StandardResultSetPagination

from django.http import HttpResponse, JsonResponse



@api_view(["GET"])
def main_dashboard(request):
    companions = Companion.objects.filter(is_deleted=False,is_blocked=False)
    mentors = Mentor.objects.filter(is_deleted=False,is_blocked=False)
    # Get mentors' ratings and project counts
    mentor_ratings = mentors.values('id', 'rating')
    mentor_project_counts = Project.objects.filter(is_deleted=False).values('mentor').annotate(project_count=Count('id'))

    # Create a dictionary to store combined scores for mentors
    mentor_scores = {mentor['id']: {'rating': mentor['rating'], 'project_count': 0, 'score': 0} for mentor in mentor_ratings}

    # Update the dictionary with project counts
    for mp in mentor_project_counts:
        if mp['mentor'] in mentor_scores:
            mentor_scores[mp['mentor']]['project_count'] = mp['project_count']

    # Normalize ratings and project counts
    max_rating = max(mentor['rating'] for mentor in mentor_scores.values())
    max_project_count = max(mentor['project_count'] for mentor in mentor_scores.values())

    if max_rating == 0:
        max_rating = 1
    if max_project_count == 0:
        max_project_count = 1

    for mentor_id, values in mentor_scores.items():
        normalized_rating = values['rating'] / max_rating
        normalized_project_count = values['project_count'] / max_project_count
        values['score'] = (normalized_rating + normalized_project_count) / 2

    # Get the top mentors based on the combined score
    top_mentors_ids = sorted(mentor_scores, key=lambda k: mentor_scores[k]['score'], reverse=True)[:5]
    top_mentors = [Mentor.objects.get(id=mentor_id) for mentor_id in top_mentors_ids]

    # Get projects with member count, comment count, and mentor involvement
    projects = Project.objects.filter(is_deleted=False)
    project_scores = projects.annotate(
        member_count=Count('team'),
        comment_count=Count('projectcomment'),
        mentor_involvement=Count('mentor'),
    )

    # Normalize member count, comment count, and mentor involvement
    max_member_count = project_scores.aggregate(max_member_count=Count('team'))['max_member_count'] or 1
    max_comment_count = project_scores.aggregate(max_comment_count=Count('projectcomment'))['max_comment_count'] or 1
    max_mentor_involvement = project_scores.aggregate(max_mentor_involvement=Count('mentor'))['max_mentor_involvement'] or 1

    for project in project_scores:
        normalized_member_count = project.member_count / max_member_count
        normalized_comment_count = project.comment_count / max_comment_count
        normalized_mentor_involvement = project.mentor_involvement / max_mentor_involvement
        project.combined_score = (normalized_member_count + normalized_comment_count + normalized_mentor_involvement) / 3

    # Get the top projects based on the combined score
    top_projects = sorted(project_scores, key=lambda p: p.combined_score, reverse=True)[:5]


    response_data = {
        "status": 200,
        "message": "Main Dashboard",
        "data": {
            "companions": companions,
            "mentors": mentors,
            "top_mentors": top_mentors,
            "top_projects": top_projects
        }        
    }    
    return Response(response_data)


@api_view(["GET"])
def countries(request):
    instances = Country.objects.all()
    serializer = CountrySerializer(instances, many=True)    
    response_data = {
        "status": 200,
        "message": "Countries List",
        "data": serializer.data
    }    
    return Response(response_data)


@api_view(["GET"])
def states(request):
    instances = State.objects.all()
    serializer = StateSerializer(instances, many=True)    
    response_data = {
        "status": 200,
        "message": "States List",
        "data": serializer.data
    }    
    return Response(response_data)


@api_view(["GET"])
def get_states(request):
    country_id = request.GET.get('country_id')
    print(country_id)
    if country_id:
        states = State.objects.filter(country_id=country_id)
        state_list = [{'id': state.id, 'name': state.name} for state in states]
        return Response({'states': list(state_list)})
    return Response({'states': []})



