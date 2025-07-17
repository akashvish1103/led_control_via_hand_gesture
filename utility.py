def get_gesture(results, frame, lst, idx_lst):
    import cv2
    gesture = ""
    if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                frame_height, frame_width, _ = frame.shape
                landmarks = hand_landmarks.landmark


                # Thumb check (compare Y of tip and IP)
                thumb_tip_y = landmarks[4].y
                thumb_ip_y = landmarks[3].y 
                is_thumb_up = thumb_tip_y < thumb_ip_y  # thumb pointing up
                is_thumb_down = thumb_tip_y > thumb_ip_y  # is thump pointing downward

                # Other fingers (index, middle, ring, pinky)  (checking y cordinate)
                is_index_up = landmarks[8].y < landmarks[6].y
                is_middle_up = landmarks[12].y < landmarks[10].y
                is_ring_up = landmarks[16].y < landmarks[14].y
                is_pinky_up = landmarks[20].y < landmarks[18].y
                
                # checking if x ordinates of all the finger tipes is greater than its DIP for cosidering fist close and thumbs up
                is_index_x_greater = landmarks[8].x > landmarks[7].x
                is_middle_x_greater = landmarks[12].x > landmarks[11].x
                is_ring_x_greater = landmarks[16].x > landmarks[15].x
                is_pinky_x_greater = landmarks[20].x > landmarks[19].x

                # checking if x ordinates of all the finger tipes is less than its DIP for cosider
                is_index_x_smaller = landmarks[8].x < landmarks[7].x
                is_middle_x_smaller = landmarks[12].x < landmarks[11].x
                is_ring_x_smaller = landmarks[16].x < landmarks[15].x
                is_pinky_x_smaller = landmarks[20].x < landmarks[19].x

                # checking if all the finger tipes is greater than its DIP for cosidering fist close (vertical y) for fist close
                is_index_down = landmarks[8].y > landmarks[7].y
                is_middle_down = landmarks[12].y > landmarks[11].y
                is_ring_down = landmarks[16].y > landmarks[15].y
                is_pinky_down = landmarks[20].y > landmarks[19].y

                is_index_extended = landmarks[8].y < landmarks[7].y
                is_middle_extended = landmarks[12].y < landmarks[11].y
                is_ring_extended = landmarks[16].y < landmarks[15].y
                is_pinky_extended = landmarks[20].y < landmarks[19].y

                
                # params = [thumbup, thumpdown, finger closed, finger opened ]
                params = []

                def thumb_up():
                    return is_thumb_up

                def thumb_down():
                    return is_thumb_down
                
                def finger_closed():
                    result = is_index_x_greater and is_middle_x_greater and is_ring_x_greater and is_pinky_x_greater
                    return result 

                def finger_opened():
                    result = is_index_x_smaller and is_middle_x_smaller and is_ring_x_smaller and is_pinky_x_smaller
                    return result
                
                def finger_extended():
                    result1 = is_index_extended and is_middle_extended and is_ring_extended and is_pinky_extended
                    result2 = is_index_x_greater and is_middle_x_greater and is_ring_x_greater and is_pinky_x_greater
                    result3 = is_index_x_smaller and is_middle_x_smaller and is_ring_x_smaller and is_pinky_x_smaller
                    return result1 or result2 or result3
                
                def finger_extended_closed():
                    result1 = is_index_x_greater and is_middle_x_greater and is_ring_x_greater and is_pinky_x_greater
                    result2 = is_index_down and is_middle_down and is_ring_down and is_pinky_down
                    return result1 or result2

                # result_lst = [thumb_up(), thumb_down(), finger_closed(), finger_opened()]

                # if result_lst == [True, False, True, False] :
                #     gesture = "Thumb up"
                # elif result_lst == [False, True, True, False]:
                #     gesture = "Thumb Down"
                # elif result_lst == [False, False, True, False]:
                #     gesture = "Fist Closed"
                # elif result_lst == [False, False, False, True]:
                #     gesture = 'Fist Closed'


                if is_thumb_up and finger_closed() and thumb_tip_y < landmarks[0].y and thumb_tip_y < landmarks[6].y:
                    gesture = "Thumb Up"
                elif is_thumb_down and finger_closed() and thumb_tip_y > landmarks[0].y :
                    gesture = "Thumb Down"
                elif finger_extended_closed() and landmarks[8].y > thumb_tip_y and landmarks[12].y > thumb_tip_y and landmarks[16].y > thumb_tip_y and landmarks[20].y > thumb_tip_y:
                    gesture = "Fist Closed"

                elif finger_extended(): 
                    gesture = "Fist Open" 

                cv2.putText(frame, f"{gesture}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

                for idx, lm in enumerate(hand_landmarks.landmark):
                    lst.append((int((lm.x*frame_width)), int(lm.y*frame_height)))   # de-normalizing the xoordinated from 0-1 to frame dimesnions of cv2
                    idx_lst.append(idx)

                
                answer_lst = [gesture, lst, idx_lst]
                return answer_lst