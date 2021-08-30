from flask import request, jsonify, current_app

from . import bp, util

@bp.route('/distance_to_mkad', methods=['GET'])
def distance_to_mkad():
    address = request.args.get('address')
    if not address:
        return jsonify(error='You must provide an address'), 400
    api_resp = util.get_distance_between_mkad_and_address(address)
    current_app.logger.info(f"{address}: {api_resp}")

    if not api_resp:
        return jsonify(error='Address not found.'), 400

    return jsonify(data=api_resp), 200