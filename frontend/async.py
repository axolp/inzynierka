import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime
import asyncio
#from sklearn.cluster import KMeans
import keyboard
import math
from scipy.stats import linregress
import json


def ellipse_score(ellipse, prev_center, frame_center):
    (center, axes, angle) = ellipse
    major_axis, minor_axis = max(axes), min(axes)
    circularity = minor_axis / major_axis  # Ratio close to 1 means more circular
    distance_to_center = np.sqrt((center[0] - frame_center[0]) ** 2 + (center[1] - frame_center[1]) ** 2)
    distance_to_prev = np.sqrt((center[0] - prev_center[0]) ** 2 + (center[1] - prev_center[1]) ** 2)
    
    # Area calculation (approximating the ellipse area)
    area = np.pi * (major_axis / 2) * (minor_axis / 2)

    # Score calculation with area reward
    score = (
        -distance_to_center            # Closer to the frame center is better
        -distance_to_prev              # Closer to the previous position is better
        + circularity * 100            # Higher circularity is better
        + area / 100                   # Reward for larger area
    )
    return score, circularity

def get_best_threshold(gray, prev_center, frame_center):
    best_threshold = 80
    best_score = -float('inf')
    test_thresholds = [60, 70, 80, 90]

    for threshold_value in test_thresholds:
        _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 50 and len(contour) >= 5:
                ellipse = cv2.fitEllipse(contour)
                score, circularity = ellipse_score(ellipse, prev_center, frame_center)
                
                # Check if circular enough and update best score
                if circularity >= 0.50 and score > best_score:
                    best_score = score
                    best_threshold = threshold_value
    return best_threshold

def weighted_average_ellipse(history):
    # Weights: previous (70%), second last (25%), third last (5%)
    weights = [0.05, 0.10, 0.85]
    
    # Initialize weighted sums
    weighted_center_x = 0
    weighted_center_y = 0
    weighted_major_axis = 0
    weighted_minor_axis = 0
    
    for i, ellipse in enumerate(history):
        (center, axes, _) = ellipse
        weighted_center_x += center[0] * weights[i]
        weighted_center_y += center[1] * weights[i]
        weighted_major_axis += axes[0] * weights[i]
        weighted_minor_axis += axes[1] * weights[i]

    # Create the weighted average ellipse
    averaged_center = (weighted_center_x, weighted_center_y)
    averaged_axes = (weighted_major_axis, weighted_minor_axis)
    averaged_angle = history[-1][2]  # Use the angle of the most recent ellipse
    
    return (averaged_center, averaged_axes, averaged_angle)

def compute_pupil_adjustment_factor(m, u, r, d, l, x, y, m_y):
    ''' HUMAN EYE ADDUCTION 44, ELEVATION 27, DEPRESSION 8 '''
    phi, theta = None, None
    
    if x < m:
        phi = (x - l) / (m - l) * 44  # Przeskalowanie dla ruchu w lewo
    elif x > m:
        phi = (x - m) / (r - m) * 44  # Przeskalowanie dla ruchu w prawo
    else:
        phi = 0  # Na wprost

    if y < m_y:
        theta = (y - u) / (m_y - u) * 27  # Przeskalowanie dla ruchu w górę
    elif y > m_y:
        theta = (y - m_y) / (d - m_y) * 8  # Przeskalowanie dla ruchu w dół
    else:
        theta = 0  

    adjustment_factor= 1 / ( math.cos(math.radians(phi))**2 * math.cos(math.radians(theta))**2 )

    return adjustment_factor

def check_increasing_area(data):
    # Check if the area has increased in each of the last 4 frames
    
    if len(data) < 4:
        print("Not enough data to perform linear regression.")
        return   # Or handle appropriately if fewer than 4 values

    # Create an array for frame numbers (1, 2, 3, 4 for simplicity)
    x = np.arange(len(data))
    y = np.array(data)
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    
    # Print or return the slope
    #print(f"Slope of the best-fit line: {slope}")
    return slope
    

def pupil_capture(after_calibration, m, u, r, d, l, m_y):
    eye_video = cv2.VideoCapture(0)
   
    x, y = [], [] # do wykresow
    i = 0
    prev_center = (0, 0)  # Initialize previous center
    frame_center = (150, 150)  # Center of the ROI
    threshold_value = 80  # Initial threshold value
    frame_count = 0
    ellipse_history = []  # Store the last three best ellipses
    area_history = []  # Track the last few pupil areas
    pupil_x= []
    pupil_y= []

    while eye_video.isOpened():
        ret, frame = eye_video.read()
        if not ret:
            break

        frame = cv2.flip(frame, 0)
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        start_x, start_y = center_x - 150, center_y - 150
        roi = frame[start_y:start_y + 300, start_x:start_x + 300]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S.%f")[:-3]  # Odcinamy ostatnie 3 cyfry mikrosekund, zostawiając milisekundy
        #print(f"Current Time: {formatted_time}")

        # Every 20 frames, determine the best threshold value
        if frame_count % 20 == 0:
            threshold_value = get_best_threshold(gray, prev_center, frame_center)
            #print("Selected threshold:", threshold_value)

        # Apply the selected threshold value
        _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        best_ellipse = None
        best_score = -float('inf')
        pupil_diameter = 0

        for contour in contours:
            area= None
            if cv2.contourArea(contour) > 50 and len(contour) >= 5:
                ellipse = cv2.fitEllipse(contour)
                (center, axes, angle) = ellipse
                diameter = max(axes)
                score, circularity = ellipse_score(ellipse, prev_center, frame_center)
                
                # Reject ellipses that are not circular enough (circularity threshold 0.60)
                if circularity < 0.60:
                    continue
                
                if 15 <= diameter <= 50 and score > best_score:
                    best_score = score
                    best_ellipse = ellipse
                    pupil_diameter = diameter

        if best_ellipse:
            ellipse_history.append(best_ellipse)
            if len(ellipse_history) > 3:
                ellipse_history.pop(0)  # Keep only the last 3 ellipses

            # Calculate weighted average if we have at least 3 ellipses
            if len(ellipse_history) == 3:
                averaged_ellipse = weighted_average_ellipse(ellipse_history)
                pupil_x.append(averaged_ellipse[0][0]) # zrzucam koordynaty kazdej xrenicy 
                pupil_y.append(averaged_ellipse[0][1]) # zrzucam koordynaty kazdej xrenicy
                cv2.ellipse(roi, averaged_ellipse, (0, 255, 0), 2)
                prev_center = averaged_ellipse[0]  # Update previous center with averaged center
                # Calculate area for the averaged ellipse
                major_axis, minor_axis = averaged_ellipse[1]
              
                area = np.pi * (major_axis / 2) * (minor_axis / 2) 
               # print(f"elipse area: {area}")
                if after_calibration:
                    area*= compute_pupil_adjustment_factor(m,u,r,d,l, averaged_ellipse[0][0], averaged_ellipse[0][1], m_y)
                    cv2.line(roi, (int(l), int(m_y)), (int(r), int(m_y)), (255, 0, 0), 2)
                    cv2.line(roi, (int(m), int(u)), (int(m), int(d)), (255, 0, 0), 2)
               # print(f"pupil real area: {3.14*((max(minor_axis, major_axis)/2)**2)}{area}")
                area_history.append(3.14*((max(minor_axis, major_axis)/2)**2))
           
               # print(f"Averaged Ellipse - Center: {averaged_ellipse[0]}, Axes: {averaged_ellipse[1]}, Angle: {averaged_ellipse[2]}, Area: {area}")
            else:
                # Draw the best ellipse if not enough history for averaging
                cv2.ellipse(roi, best_ellipse, (0, 255, 0), 2)
                if after_calibration:
                    #print(l, m_y)
                    cv2.line(roi, (int(l), int(m_y)), (int(m), int(m_y)), (255, 0, 0), 2)
    
                    # Put the label near each point
                   # cv2.putText(roi, label, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
               
                prev_center = best_ellipse[0]
                # Calculate area for the best ellipse
                major_axis, minor_axis = best_ellipse[1]
                area = np.pi * (major_axis / 2) * (minor_axis / 2) 
                area_history.append(3.14*((max(minor_axis, major_axis)/2)**2))
               # print("real area:", area)
                #print(f"Best Ellipse - Center: {best_ellipse[0]}, Axes: {best_ellipse[1]}, Angle: {best_ellipse[2]}, Area: {area}")

            # Check for consistently increasing area over the last 4 frames
            
            # Keep only the last 4 areas in history for checking
      
            if len(area_history) > 4 and after_calibration:

                slope=check_increasing_area(area_history[-13:]) # 2 sekundy nagrania
            
                timestamp = datetime.now().strftime("%H-%M-%S-%f")[:-3]  # Format to hour-minute-second-millisecond
                #filename = f"pupil_capture_{timestamp}_axis_{3.14*((max(minor_axis, major_axis)/2)**2)}slope_{slope:.2f}.png"
                #cv2.imwrite(filename, roi)
                
                area_history.pop(0)
                print(json.dumps({"slope":slope, "timestamp": timestamp}))

        cv2.imshow("Thresholded Image (Pupil Detection)", thresh)
        cv2.imshow("ROI with Detected Ellipse", roi)
        # if keyboard.is_pressed('q') and not after_calibration:
        #     return pupil_x, pupil_y
        
        # if keyboard.is_pressed('q') and after_calibration:
        #     return pupil_x, pupil_y


        #DO WYKRESOW
        x.append(i)
        y.append(area)
        i += 1
        frame_count += 1
        x_last_15 = x[-15:]
        y_last_15 = y[-15:]

     
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return pupil_x, pupil_y
            break

    eye_video.release()
    cv2.destroyAllWindows()
    return pupil_x, pupil_y
  
   

def clasterization(data):
    sorted_data = sorted(data)
    l = np.mean(sorted_data[:10])  
    m = np.mean(sorted_data[len(sorted_data)//2 - 5:len(sorted_data)//2 + 5])  
    r = np.mean(sorted_data[-10:]) 
    return l, m, r

def calibration():
    # Placeholder for asynchronous calibration logic
    #TAK NAPRAWDE NIE POTRZEBUJE KLASTERYCACJI MOGE SORTOWAC I WYBRAX MAX MEAN MIDDLE ITP
    print("CALIBRATION")
    print("please look straight to the camera, as far left as you can, as far up as you can, as far right as you can, as far down as you can")
    x, y= pupil_capture(False, None, None, None, None, None, None)
    l, m, r = clasterization(x)
    u, m_y, d= clasterization(y)
   
    print(l, m, r)

    print(u)
    print(m_y)
    print(d)

    #print("korekta")
    #print(compute_pupil_adjustment_factor(m,u,r,d,l,x[0],y[0],m_y))

    return m, u, r, d, l, m_y

def main():
    m, u, r, d, l, m_y = calibration()
    print("TERAZ PROGRAM PO KALIBRACJI")
    x, y = pupil_capture(True, m, u, r, d, l, m_y)
    print("KONIEC DZIALANIA")
    

asyncio.run(main())