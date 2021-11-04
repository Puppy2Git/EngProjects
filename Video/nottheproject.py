import cv2
import numpy



image = cv2.imread("lmao.png",-1)
image_eye = cv2.imread("eyelmao.png",-1)

def overlay_image_alpha(img, img_overlay, x, y, alpha_mask):
    """Overlay `img_overlay` onto `img` at (x, y) and blend using `alpha_mask`.

    `alpha_mask` must have same HxW as `img_overlay` and values in range [0, 1].
    """
    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    # Blend overlay within the determined ranges
    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
    alpha = alpha_mask[y1o:y2o, x1o:x2o, numpy.newaxis]
    alpha_inv = 1.0 - alpha

    img_crop[:] = alpha * img_overlay_crop + alpha_inv * img_crop

alpha_mask = image[:, :, 3] / 255.0
img_overlay = image[:, :, :3]

alpha_mask_eye = image_eye[:, :, 3] / 255.0
img_overlay_eye = image_eye[:, :, :3]

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x,y),(x+w,y+h),color,2)
        cv2.putText(img, text, (x,y-4), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x,y,w,h]
    return coords

def detect(img, faceCascade, eyesCascade, mouthCascade):
    color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0)}
    coords = draw_boundary(img, faceCascade, 1.1, 10, color['blue'],"Face")
    if (len(coords) == 4):
        roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
        coords = draw_boundary(roi_img, eyesCascade, 1.1, 14, color["red"],"Eyes")
        coords = draw_boundary(roi_img, mouthCascade, 1.1, 30, color["green"],"Mouth")
    return img

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eyesCascade = cv2.CascadeClassifier("haarcascade_eye.xml")
mouthCascade = cv2.CascadeClassifier("Mouth.xml")

vid = cv2.VideoCapture(0)#Grabs the camera
ret, frame = vid.read()#Grabs the ret and the frame
while True:# yes.
    #for c in range(0,3):
    #    alpha_f[y1:y2, x1:x2, c] = (alpha_i * image[:,:,c] + alpha_f * frame[y1:y2, x1:x2, c])
    #img_result = frame[:, :, :3].copy()
    #frame = detect(frame, faceCascade, eyesCascade, mouthCascade)
    # Capture frame-by-frame
    ret, frame = vid.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    mouth = mouthCascade.detectMultiScale(gray, 1.3, 5)
    faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Draw a rectangle around the faces
        roi_gray_mouth = gray[y+(int(h/2)):y+h, x:x+w]
        roi_color_mouth = frame[y+(int(h/2)):y+h, x:x+w]

        roi_gray_eye = gray[y-(int(h/2)):y+h, x:x+w]
        roi_color_eye = frame[y-(int(h/2)):y+h, x:x+w]

        mouth = mouthCascade.detectMultiScale(roi_gray_mouth)
        eyes = eyesCascade.detectMultiScale(roi_gray_eye)
        for (ex,ey,ew,eh) in mouth:
            #cv2.rectangle(roi_color_mouth, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            overlay_image_alpha(frame, img_overlay, ex+int(x - ew/2), ey+int(y + h/2), alpha_mask)
            

        for (eex,eey,eew,eeh) in eyes:
            d = int(eew / 2)
            overlay_image_alpha(frame, img_overlay_eye, x + (int(eex + eew / 4) + int(d / 2))-15, y+ (int(eey + eeh / 4))-80 , alpha_mask_eye)
            #cv2.circle(roi_color_eye, (int(eex + eew / 4) + int(d / 2), int(eey + eeh / 4) + int(d / 2)), int(d) ,(0,0,255),2)

    # Display the resulting frame
    
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):#Exits if the q key is pressed
        break
    
    #ret, frame = vid.read()#Getting new frame and ret


#Outside of while loop
vid.release()#Releases camera from application
cv2.destroyAllWindows()#Kill all windows
