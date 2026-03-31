def get_camera_detections(results_left, results_right, model):
    l_class, r_class, mid_class = "empty", "empty", "empty"
    pos1, pos2 = "empty", "empty"

    if results_left and len(results_left) > 0:
        for box in results_left[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            xc, yc = (x1 + x2) // 2, (y1 + y2) // 2
            lbl = model.names[int(box.cls[0])]
            
            if 160 <= yc <= 320:
                if 0 <= xc < 320:
                    l_class = lbl
                elif 320 <= xc <= 640:
                    pos1 = lbl

    if results_right and len(results_right) > 0:
        for box in results_right[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            xc, yc = (x1 + x2) // 2, (y1 + y2) // 2
            lbl = model.names[int(box.cls[0])]
            
            if 160 <= yc <= 320:
                if 320 <= xc <= 640:
                    r_class = lbl
                elif 0 <= xc < 320:
                    pos2 = lbl

    if pos1 != "empty" and pos2 != "empty":
        mid_class = pos1 if pos1 == pos2 else pos1
    elif pos1 != "empty":
        mid_class = pos1
    elif pos2 != "empty":
        mid_class = pos2
    
    return l_class, mid_class, r_class