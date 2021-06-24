import cv2


def motion_detector(img, prev_img):
    frame1 = img
    frame2 = prev_img
 
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    
    contours, hierarchy = cv2.findContours(
        dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    i = 0
    found = 0
    
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        area = cv2.contourArea(cnt)
        if hierarchy[0, i, 3] == -1:
            if float(w/h) > 1 and area > 1000 and area < 4000:
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                found = 1
        i = i+1

    if found == 1:
        print("motion detected")
        return True
    else:
        return False
