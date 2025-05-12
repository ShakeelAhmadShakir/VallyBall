import os
import threading
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from .goal_detector import detect_goals

video_processing_results = {}

def process_video(video_path, result_key):
    output_dir = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'uploaded_clips', result_key)
    clip_name, goal_count = detect_goals(video_path, output_dir)

    clip_url = f"/static/uploaded_clips/{result_key}/{clip_name}" if clip_name else None
    video_processing_results[result_key] = {
        "goal_count": goal_count,
        "clip_url": clip_url
    }

@csrf_exempt
def chat_view(request):
    if request.method == 'POST' and 'video' in request.FILES:
        video = request.FILES['video']
        upload_dir = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'uploaded')
        os.makedirs(upload_dir, exist_ok=True)

        file_key = f"{video.name}_{video.size}"
        video_path = os.path.join(upload_dir, f"{file_key}.mp4")

        with open(video_path, 'wb+') as destination:
            for chunk in video.chunks():
                destination.write(chunk)

        threading.Thread(target=process_video, args=(video_path, file_key)).start()

        return JsonResponse({'message': '✅ File uploaded. Processing started...', 'key': file_key})

    return render(request, 'chat.html', {'title': 'Football Chatbot'})

def get_results(request):
    key = request.GET.get('key')
    print(f"📩 Fetching result for key: {key}")
    result = video_processing_results.get(key)
    if result:
        print(f"✅ Result found: {result}")
        return JsonResponse({
            'status': 'done',
            'goal_count': result['goal_count'],
            'clip_url': result['clip_url']
        })
    else:
        print(f"⏳ Still processing or key not found.")
        return JsonResponse({'status': 'processing'})
