import cv2
import scipy
from microsat_util import utils


class FeatureMatches(object):
    pass


def draw_matches(image1, image1_keypoints, image2, image2_keypoints, matches):

    h1, w1 = image1.shape[:2]
    h2, w2 = image2.shape[:2]

    output_image = scipy.zeros((max(h1, h2), w1 + w2, 3), scipy.uint8)
    output_image[:h1, :w1, 0] = image1
    output_image[:h2, w1:, 0] = image2
    output_image[:, :, 1] = output_image[:, :, 0]
    output_image[:, :, 2] = output_image[:, :, 0]

    for match in matches:
        color = tuple([scipy.random.randint(0, 255) for _ in xrange(3)])

        cv2.line(output_image,
                 (int(image1_keypoints[match.queryIdx].pt[0]), int(image1_keypoints[match.queryIdx].pt[1])),
                 (int(image2_keypoints[match.trainIdx].pt[0] + w1), int(image2_keypoints[match.trainIdx].pt[1])),
                 color)

    return output_image


def flann(image1, image2):
    """
    @param image1
    @type image1 <microsat_util.georef.detectors.DetectedFeatures>

    @param image2
    @type image2 <microsat_util.georef.detectors.DetectedFeatures>

    @rtype: <microsat_util.georef.matchers.MatchedFeatures>
    """

    # Fast Library for Approximate Nearest Neighbors
    FLANN_INDEX_KDTREE = 0

    # Pass two (2) dictionaries specifying algorithm to be used
    # or algorithms like SIFT, SURF etc. you can pass following:
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)

    # Specifies the number of times the trees in the index should be recursively traversed.
    # Higher values gives better precision,but also takes more time.
    # If you want to change the value, pass search_params = dict(checks=100)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Check if images have enough descriptors
    if image1.descriptors is None or \
       image2.descriptors is None or \
       len(image1.descriptors) == 0 or \
       len(image2.descriptors) == 0:

        raise ValueError("At least one of the images does not contain features. \
                          Tip: Try a lower Hessian Threshold")

    matches = flann.knnMatch(image1.descriptors, image2.descriptors, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    output = FeatureMatches()
    output.matches = good_matches
    return output


def bf(image1, image2):
    bf = cv2.BFMatcher()

    # Check if images have enough descriptors
    if image1.descriptors is None or image2.descriptors is None or \
       len(image1.descriptors) == 0 or len(image2.descriptors) == 0:
        raise ValueError("At least one of the images does not contain features. Tip: Try a lower Hessian Threshold")

    matches = bf.match(image1.descriptors, image2.descriptors)
    dist = [m.distance for m in matches]

    print 'Match Distance -- Min:\t %.3f' % min(dist)
    print 'Match Distance -- Mean:\t %.3f' % (sum(dist) / len(dist))
    print 'Match Distance -- Max:\t %.3f' % max(dist)

    matches = sorted(matches, key=lambda x: x.distance)

    # Threshold: Half the mean
    threshold_distance = (sum(dist) / len(dist)) * 0.50
    selected_matches = [m for m in matches if m.distance < threshold_distance]

    output = FeatureMatches()
    output.matches = selected_matches
    return output
