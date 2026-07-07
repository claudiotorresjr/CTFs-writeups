from django.http import HttpResponse, JsonResponse
from django.template import engines
from django.views.decorators.http import require_GET

from surveys.models import Survey


@require_GET
def index(request):
    engine = engines["django"]
    template = engine.from_string(INDEX_TEMPLATE)
    html = template.render(request=request)
    return HttpResponse(html)


@require_GET
def survey_search(request):
    filters = request.GET.dict()

    if not filters:
        surveys = Survey.objects.filter(is_public=True)
    else:
        try:
            surveys = Survey.objects.filter(**filters)
        except Exception:
            return JsonResponse(
                {"error": "Invalid filter parameters"},
                status=400,
            )

    results = [
        {
            "id": s.id,
            "title": s.title,
            "category": s.category,
            "author": s.author,
            "description": s.description,
        }
        for s in surveys[:50]
    ]
    return JsonResponse({"count": len(results), "results": results})


@require_GET
def health(request):
    return JsonResponse({"status": "ok"})


INDEX_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SurveyHub</title>
</head>
<body>
  <h1>SurveyHub — Survey Management Platform</h1>
  <p>Use the API at <code>/api/surveys/</code> to search.</p>
</body>
</html>"""
