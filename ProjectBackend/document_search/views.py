from django.shortcuts import render
from resource_contribution.models import RESOURCE_METADATA
from django.db.models import Q

def resourceSearch(request):
    # Get search parameters from the request (e.g., from a form or query parameters)
    subject = request.GET.get('subject', '').strip()  # Get the subject from the query parameters
    keywords = request.GET.get('keywords', '').strip()  # Get the keywords from the query parameters

    # Initialize the queryset for RESOURCE_METADATA
    resources = RESOURCE_METADATA.objects.all()

    # Filter by subject if provided
    if subject:
        resources = resources.filter(subject__icontains=subject)

    # Filter by keywords if provided
    if keywords:
        # Split keywords by space or comma and search each keyword
        keywords_list = keywords.split(',')
        for keyword in keywords_list:
            resources = resources.filter(Q(keywords__icontains=keyword.strip()))

    # Render the results in a template (you will need to create this template)
    return render(request, 'resource_search.html', {'resources': resources})
