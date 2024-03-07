import flask
from flask import jsonify, make_response, request

import datetime

from . import db_session
from .jobs import Job


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=(
                    "team_leader_id", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished"))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>')
def get_job_by_id(job_id: int):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == job_id).first()

    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)

    return jsonify(
            job.to_dict(only=(
                "team_leader_id", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished"))
    )


@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader_id', 'job', 'work_size', 'start_date', 'end_date', 'is_finished', 'collaborators']):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()
    job = Job()
    job.team_leader_id = request.json['team_leader_id']
    job.job = request.json['job']
    job.work_size = request.json['work_size']
    job.start_date = datetime.datetime.strptime(request.json['start_date'], '%Y-%m-%d %H:%M:%S.%f')
    job.end_date = datetime.datetime.strptime(request.json['end_date'], '%Y-%m-%d %H:%M:%S.%f')
    job.is_finished = request.json['is_finished']
    job.collaborators = request.json['collaborators']

    db_sess.add(job)
    db_sess.commit()

    return jsonify({'id': job.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id: int):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).get(job_id)

    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)

    db_sess.delete(job)
    db_sess.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id: int):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).get(job_id)

    if not job:
        return make_response(jsonify({'error': 'Job not found'}), 404)
    elif not request.json:
        return make_response(jsonify({'error': 'Empty request'}))
    elif not all(
            key in ['team_leader_id', 'job', 'work_size', 'start_date', 'end_date', 'is_finished', 'collaborators']
            for key in request.json):
        return make_response(jsonify({'error': 'Bad request'}), 404)

    for key in request.json:
        if key == 'team_leader_id':
            job.team_leader_id = request.json['team_leader_id']
        elif key == 'job':
            job.job = request.json['job']
        elif key == 'work_size':
            job.work_size = request.json['work_size']
        elif key == 'start_date':
            job.start_date = datetime.datetime.strptime(request.json['start_date'], '%Y-%m-%d %H:%M:%S.%f')
        elif key == 'end_date':
            datetime.datetime.strptime(request.json['end_date'], '%Y-%m-%d %H:%M:%S.%f')
        elif key == 'is_finished':
            job.is_finished = request.json['is_finished']
        elif key == 'collaborators':
            job.collaborators = request.json['collaborators']

    db_sess.add(job)
    db_sess.commit()

    return jsonify({'success': 'OK'})
