import cv2
from ultralytics import YOLO
import os
from datetime import datetime

def detect_goals(video_path, output_dir):
    model = YOLO("models/goal_detector_final3.pt")
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"❌ Error opening video: {video_path}")
        return None, 0

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    combined_name = f"all_goals_{timestamp}.mp4"
    combined_path = os.path.join(output_dir, combined_name)
    out = cv2.VideoWriter(combined_path, fourcc, fps, (width, height))

    goal_count = 0
    buffer = []
    buffer_size = fps * 4  # 4 seconds before goal
    goal_pending = False
    ball_last_y = None
    rim_box = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        buffer.append(frame.copy())
        if len(buffer) > buffer_size:
            buffer.pop(0)

        results = model(frame)[0]
        current_rim = None
        current_ball = None

        for box in results.boxes:
            label = model.names[int(box.cls)].lower()
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            if label == "rim":
                current_rim = (x1, y1, x2, y2)
            elif label == "basketball":
                current_ball = ((x1 + x2) // 2, (y1 + y2) // 2)

        if current_rim:
            rim_box = current_rim

        if rim_box and current_ball:
            rim_top, rim_bottom = rim_box[1], rim_box[3]
            ball_y = current_ball[1]

            if ball_last_y is not None:
                if ball_last_y < rim_top and ball_y > rim_bottom and not goal_pending:
                    goal_count += 1
                    goal_pending = True
                    for f in buffer:
                        out.write(f)
                    for _ in range(fps * 2):  # 2 seconds after goal
                        ret, pf = cap.read()
                        if not ret:
                            break
                        out.write(pf)
                    buffer.clear()

                if ball_y > rim_bottom + 50:
                    goal_pending = False

            ball_last_y = ball_y

    cap.release()
    out.release()

    if goal_count == 0:
        os.remove(combined_path)
        return None, 0

    return combined_name, goal_count
