from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from app.v2.models.offices_model import Office
from app.v2.models.user_model import User
from app.v2.models.vote_model import Vote
from app.v2.util.validate import response, exists, response_error
from app.v2.blueprints import bp


votes = Vote.votes


@bp.route('/votes/', methods=['POST', 'GET'])
def vote():
    if request.method == 'POST':
        """ Create vote end point """

        data = request.get_json()

        if not data:
            return response_error("No data was provided", 400)

        try:
            created_by = data['createdBy']
            office = data['office']
            candidate = data['candidate']
        except KeyError as e:
            return response_error("{} field is required".format(e.args[0]), 400)

        vote = Vote(created_by, office, candidate)

        if not vote.validate_object():
            return response_error(vote.error_message, vote.error_code)

        if not exists('id', office, Office.offices):
            return response_error('Selected Office does not exist', 404)
        if not exists('id', candidate, User.users):
            return response_error('Selected User does not exist', 404)

        vote.save()

        # return added vote
        return response("Success", 201, [vote.as_json()])

    elif request.method == 'GET':
        """ Get all votes end point """

        return response('Success', 200, votes)


@bp.route('/votes/candidate/<int:id>', methods=['GET'])
def get_candidate_votes(id):
    """ Gets all votes for a specific candidate """

    obtained = [vote for vote in votes if vote['candidate'] == id]

    return vote_response(
        'Success', 200, len(obtained), obtained)


@bp.route('/office/<office-id>/result', methods=['GET'])
def get_office_votes(id):
    """ Gets all votes for a specific office """

    obtained = [vote for vote in votes if vote['office'] == id]

    return vote_response(
        'Success', 200, len(obtained), obtained)


def vote_response(message, code, count, data=None):
    """ Creates a basic reposnse """
    response = {
        "status": code,
        "message": message,
        "data": data,
        "count": count
    }
    return make_response(jsonify(response), code)