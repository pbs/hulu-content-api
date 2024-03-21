from flask_restful import reqparse

def configure_parser():
    # initalize parser
    parser = reqparse.RequestParser()
    # add arguments
    parser.add_argument("metric", required=True)
    parser.add_argument("content_partner", required=True)
    parser.add_argument("series_movie", required=True)
    parser.add_argument("season", required=True)
    parser.add_argument("package", required=True)
    parser.add_argument("playback_type", required=True)
    parser.add_argument("time_increment", required=True)
    parser.add_argument("start_date", required=True)
    parser.add_argument("end_date", required=True)
    parser.add_argument("asset")
    # return configured parser
    return parser