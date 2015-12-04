import argparse
from microsat_util import georef
from microsat_util import utils


class MicrosatGeorefError:
    pass


def get_arguments():
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

    # Set defalt values for arguments
    parser.set_defaults(
        detector='surf',
        matcher='flann',
        hessian_threshold=1000,
        output_fileame=None)

    args = parser.parse_args()
    return args


def get_keypoints():
    """
    The entry point for the `georef-keypoints` command
    """
    args = get_arguments()

    if args.detector == 'sift':
        results = georef.detectors.sift(args.input_filename)
    elif args.detector == 'surf':
        results = georef.detectors.surf(args.input_filename, hessian_threshold=args.hessian_threshold)

    if args.output_filename is not None:
        utils.save_image(filename=args.output_filename, output_image=results.output_image)


def get_matches():
    """
    An entry point for the `georef-match` command. Returns
    """
    print georef.matchers.tiff()


def main():
    """
    The entry point for the `georef` command
    """
    args = get_arguments()
    print georef.process(args.input_filename)


if __name__ == '__main__':
    get_keypoints()
