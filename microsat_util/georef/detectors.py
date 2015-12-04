import cv2


__all__ = ['sift']


class DetectedFeatures():
    keypoints = None
    descriptors = None


def sift(image_path):
    """
    Detects keypoints based on the SIFT detector. To use:

    ```
    results = detect('images/up.google.jpg')

    output_image = results.output_image
    keypoints = results.keypoints
    ...
    ```

    @param image_path: The path to the image to be analyzed
    @type  image_path: string

    @param show: Toggles whether or not to show the marked image in a pop up
                 after detection
    @type  show: boolean

    @return: a named tuple containing results of the surf detection algorithm
    @rtype: <DetectedFeatures> with the following attributes:
       output_image   -- the original image marked with the keypoints found
       keypoints      -- a list of keypoints found by the algorithm
       descriptors    -- a list of descriptors computed by SIFT
    """

    print "Running SIFT on %s" % image_path

    # Convert image to grayscale
    input_image = cv2.imread(image_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    # Extract keypoints and descriptors
    sift = cv2.SIFT()
    keypoints, descriptors = sift.detectAndCompute(input_image, None)

    # Draw keypoints on output image
    output_image = cv2.drawKeypoints(input_image, keypoints, None, (255, 0, 0), 4)

    # Build output
    output = DetectedFeatures()
    output.input_image = input_image
    output.output_image = output_image
    output.keypoints = keypoints
    output.descriptors = descriptors
    return output


def surf(image_path, hessian_threshold=400):
    """
    Detects keypoints based on the SURF detector. To use:

    ```
    results = detect('images/up.google.jpg')

    output_image = results.marked_image
    keypoints = results.keypoints
    ...
    ```

    @param image_path: The path to the image to be analyzed
    @type  image_path: string

    @param hessian_threshold: The hessian threshold to be used by the SURF detector
    @type  hessian_threshold: int

    @param show: Toggles whether or not to show the marked image in a pop up
                 after detection
    @type  show: boolean

    @return: a named tuple containing results of the surf detection algorithm
    @rtype: <DetectedFeatures> with the following attributes:
       output_image   -- the original image marked with the keypoints found
       keypoints      -- a list of keypoints found by the algorithm
       descriptors    -- a list of descriptors computed by SURF
    """

    print "Running SURF on %s | Threshold: %s" % (image_path, hessian_threshold)

    # Convert image to grayscale
    input_image = cv2.imread(image_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    # Extract keypoints and descriptors
    surf = cv2.SURF(hessian_threshold)
    keypoints, descriptors = surf.detectAndCompute(input_image, None)

    # Draw keypoints on output image
    output_image = cv2.drawKeypoints(input_image, keypoints, None, (255, 0, 0), 4)

    # Build output
    output = DetectedFeatures()
    output.input_image = input_image
    output.output_image = output_image
    output.keypoints = keypoints
    output.descriptors = descriptors
    return output
