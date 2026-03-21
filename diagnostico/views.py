import json
import urllib.request
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Report


def index(request):
    return render(request, 'diagnostico/index.html')


@csrf_exempt
@require_POST
def save_report(request):
    try:
        data = json.loads(request.body)
        report = Report(data=data)
        report.save()
        return JsonResponse({'uid': report.uid})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def view_report(request, uid):
    report = get_object_or_404(Report, uid=uid)
   return render(request, 'diagnostico/report.html', {'report_data': report.data})


@csrf_exempt
@require_POST
def claude_proxy(request):
    try:
        body = json.loads(request.body)
        prompt = body.get("prompt", "")
        json_mode = body.get("jsonMode", False)
        api_key = body.get("apiKey", "").strip()

        if not api_key:
            return JsonResponse({"error": "Chave da API não informada."}, status=400)

        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}],
        }
        if json_mode:
            payload["system"] = (
                "You are a JSON-only API. Respond ONLY with valid JSON. "
                "No explanations, no markdown, no text before or after the JSON object."
            )

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        text = next((b["text"] for b in result.get("content", []) if b.get("type") == "text"), "")
        return JsonResponse({"text": text})

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
            msg = error_json.get("error", {}).get("message", str(e))
        except Exception:
            msg = error_body
        return JsonResponse({"error": msg}, status=e.code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
