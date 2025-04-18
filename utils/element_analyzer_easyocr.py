import easyocr
import cv2

def detect_text_with_bounding_boxes(image_path, output_path):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en', 'ch_sim'])  # Add languages as needed

    # Read the image
    image = cv2.imread(image_path)

    # Perform text detection
    results = reader.readtext(image_path)

    # Draw bounding boxes around detected text
    # for (bbox, text, prob) in results:
    #     # Extract the bounding box coordinates
    #     (top_left, top_right, bottom_right, bottom_left) = bbox
    #     top_left = tuple(map(int, top_left))
    #     bottom_right = tuple(map(int, bottom_right))

        # Draw the rectangle
        # cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

        # # Put the detected text near the bounding box
        # cv2.putText(image, text, (top_left[0], top_left[1] - 10), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save the output image
    # cv2.imwrite(output_path, image)
    print(f"Output saved to {output_path}")
    return results
    
def get_elements(image_path, output_path, centerx, centery, radius):
    results = detect_text_with_bounding_boxes(image_path, output_path)  # Use a temporary output path
    image = cv2.imread(image_path)
    # Extract elements within the specified range
    elements_in_range = []
    id_count = 0
    for (bbox, text, prob) in results:
        # Extract the bounding box coordinates
        (top_left, top_right, bottom_right, bottom_left) = bbox
        center_x = (top_left[0] + bottom_right[0]) / 2
        center_y = (top_left[1] + bottom_right[1]) / 2

        # Calculate the distance from the center
        distance = ((center_x - centerx) ** 2 + (center_y - centery) ** 2) ** 0.5

        # Check if the element is within the radius
        if distance <= radius:
            id_count += 1
            elements_in_range.append({
                'id': id_count,
                'text': text,
                'probability': prob,
                'bounding_box': bbox,
                'coordinates': {
                    'x': center_x,
                    'y': center_y
                }
            })
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            # Put the detected text near the bounding box
            cv2.putText(image, str(id_count), (top_left[0], top_left[1] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 4)
    
    # Save the output image
    cv2.imwrite(output_path, image)      
    return elements_in_range

# Example usage
# image_path = 'data/input/exception_image/screenshot_history/Image1.png'  # Replace with your input image path
# output_path = 'data/input/exception_image/screenshot_history/Image1_ocr.png'  # Replace with your desired output path
# get_elements(image_path, output_path, 100, 1700, 300)  # Example center and radius