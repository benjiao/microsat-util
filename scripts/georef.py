import argparse
from microsat_util import georef
from microsat_util import utils


class MicrosatGeorefError:
    pass


def main():
    """
    The entry point for the `georef` command
    """
    parser = argparse.ArgumentParser(description="Geo Reference an Image")

    parser.add_argument(
        'input_filename',
        help='The file to be processed')

    parser.add_argument(
        '-d', '--detector',
        help='the feature detection algorithm to use on the input image',
        choices=['surf', 'sift'])

    parser.add_argument(
        '-t', '--threshold',
        dest='hessian_threshold',
        type=int,
        help='the hessian threshold to be used on the input image. \
              Disregarded if not using the SURF detector')

    parser.add_argument(
        '-o', '--output-file',
        dest='output_filename',
        help='the path and filename of the output image. \
              if set, output image will be saved.')

    parser.set_defaults(
        detector='surf',
        matcher='flann',
        hessian_threshold=1000,
        output_fileame=None)

    args = parser.parse_args()
    print georef.process(args.input_filename)


def get_keypoints():
    """
    The entry point for the `georef-keypoints` command
    """
    parser = argparse.ArgumentParser(description="Geo Reference an Image")

    parser.add_argument('input_filename', help='The file to be processed')

    parser.add_argument('-d', '--detector',
                        help='the feature detection algorithm to use on the input image', choices=['surf', 'sift'])

    parser.add_argument('-t', '--threshold', dest='hessian_threshold', type=int,
                        help='the hessian threshold to be used on the input image. \
                              Disregarded if not using the SURF detector')

    parser.add_argument('-o', '--output-file', dest='output_filename',
                        help='the path and filename of the output image. \
                              if set, output image will be saved.')

    parser.set_defaults(
        detector='surf',
        hessian_threshold=1000,
        output_fileame=None)

    args = parser.parse_args()

    if args.detector == 'sift':
        results = georef.detectors.sift(args.input_filename)

    elif args.detector == 'surf':
        results = georef.detectors.surf(args.input_filename, hessian_threshold=args.hessian_threshold)

    if args.output_filename is not None:
        output_image = georef.detectors.draw_keypoints(input_image=results.input_image, keypoints=results.keypoints)
        utils.save_image(filename=args.output_filename, output_image=output_image)


def get_matches():
    """
    An entry point for the `georef-match` command. Returns
    """
    parser = argparse.ArgumentParser(description='Find keypoint matches between two images')

    parser.add_argument('image1',
                        help='the first file to be processed')

    parser.add_argument('image2',
                        help='the seconde file to be processed and matched with the first one')

    parser.add_argument('-o', '--output', dest='output_filename',
                        help='the directory in where results are saved')

    parser.add_argument('-d', '--detector', dest='detector',
                        help='the feature detector to use on the image',
                        choices=['surf', 'sift'])

    parser.add_argument('-t', '--threshold', dest='hessian_threshold', type=int,
                        help='the hessian threshold to be used by both detectors')

    parser.add_argument('-t1', '--threshold1', dest='image1_threshold', type=int,
                        help='the hessian threshold to be used on the first image')

    parser.add_argument('-t2', '--threshold2', dest='image2_threshold', type=int,
                        help='the hessian threshold to be used on the second image')

    parser.add_argument('-m', '--matcher', dest='matcher',
                        help='the matching algorithm to use', choices=['bf', 'flann'])

    parser.set_defaults(
        detector='surf',
        matcher='flann',
        hessian_threshold=None,
        image1_threshold=100,
        image2_threshold=100,
        popup=True)

    args = parser.parse_args()

    # If hessian_threshold (-t) has been set,
    # override image1 and image2 options
    if args.hessian_threshold is not None:
        image1_threshold = args.hessian_threshold
        image2_threshold = args.hessian_threshold
    else:
        image1_threshold = args.image1_threshold
        image2_threshold = args.image2_threshold

    """
    Run feature detection algorithm
    """
    if args.detector == "surf":
        image1 = georef.detectors.surf(image_path=args.image1, hessian_threshold=image1_threshold)
        image2 = georef.detectors.surf(image_path=args.image2, hessian_threshold=image2_threshold)

    elif args.detector == "sift":
        image1 = georef.detectors.sift(image_path=args.image1)
        image2 = georef.detectors.sift(image_path=args.image2)

    """
    Run matching algorithm
    """
    if args.matcher == "bf":
        matcher_results = georef.matchers.bf(image1=image1, image2=image2)

    elif args.matcher == "flann":
        matcher_results = georef.matchers.flann(image1=image1, image2=image2)

    # keep only the reasonable matches
    output_image = georef.matchers.draw_matches(
        image1=image1.input_image, image1_keypoints=image1.keypoints,
        image2=image2.input_image, image2_keypoints=image2.keypoints,
        matches=matcher_results.matches)

    utils.save_image(filename=args.output_filename, output_image=output_image)
