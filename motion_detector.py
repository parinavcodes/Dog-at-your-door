import cv2

# cap = cv2.VideoCapture("opt_Trim.mp4")
# obj_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=30)


def motion_detector(img, prev_img):
    # frame2 = None
    # print(cap.read()[1].shape)
    # while 1:
    # _, frame1 = cap.read()
    # _, frame2 = cap.read()
    frame1 = img
    frame2 = prev_img
    # compare = frame1 == frame2
    # print(compare.all())
    # ret, frame = cap.read()
    # mask = obj_detector.apply(frame)
    diff = cv2.absdiff(frame1, frame2)
    # print(diff.shape)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    # cv2.imshow('obj detect', thresh)
    dilated = cv2.dilate(thresh, None, iterations=3)
    # contours, _ = cv2.findContours(
    #     mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(
        dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    found = 0
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        area = cv2.contourArea(cnt)
        if hierarchy[0, i, 3] == -1:
            if float(w/h) > 1 and area > 1000 and area < 4000:
                # cv2.drawContours(frame, [cnt], -1, (255, 0, 0), 2)
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                found = 1
        i = i+1
    # cv2.imshow('obj detection', frame1)
# cv2.waitKey(1)
    # if cv2.waitKey(1) == ord('q'):
    #     break
    if found == 1:
        print("motion detected")
        return True
    else:
        # print("not found")
        return False

    # cv2.destroyAllWindows()
    # cap.release()


# motion_detector(cap)
