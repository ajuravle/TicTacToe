from flask import session,request
from flask_socketio import emit, join_room, leave_room
from .. import socketio
players = {}


@socketio.on('connected', namespace='/game')
def joined(message):
    join_room(players[session['name']]['room'])
    emit('create_table', {'msg': players[session['name']]['room']}, room=players[session['name']]['room'])

@socketio.on('move', namespace='/game')
def move(message):
    emit('message', {'msg': [message['msg'],players[session['name']]['simbol']]}, room=players[session['name']]['room'])


@socketio.on('left', namespace='/game')
def left(message):
    leave_room(players[session['name']]['room'])
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=players[session['name']]['room'])

@socketio.on('clearTable', namespace='/game')
def clearTable():

    emit('clearTable2', room=players[session['name']]['room'])


@socketio.on('connected', namespace='/players')
def joined_players(message):
    join_room("players")
    players[session['name']] = {"id":request.sid,"inGame":False}
    filtered_dict = {k: v for k, v in players.iteritems() if not v['inGame']}
    emit('players', {'list': filtered_dict.keys()},room="players")

@socketio.on('disconnect', namespace='/players')
def disconnect():
    leave_room("players")
    players[session['name']]['inGame'] = True
    filtered_dict = {k: v for k, v in players.iteritems() if not v['inGame']}
    emit('players', {'list': filtered_dict.keys()}, room="players")

@socketio.on('choosePl', namespace='/players')
def choosePl(message):
    players[session['name']]['room'] = session['name'] + " - " + message["msg"]
    players[session['name']]['inGame'] = True
    players[session['name']]['simbol'] = "X"
    emit('play', {"msg":session['name']}, room=players[message["msg"]]["id"])
    filtered_dict = {k: v for k, v in players.iteritems() if not v['inGame']}
    emit('players', {'list': filtered_dict.keys()}, room="players")


@socketio.on('play2', namespace='/players')
def play2(message):
    players[session['name']]['room'] = message["msg"]  + " - " + session['name']
    players[session['name']]['inGame'] = True
    players[session['name']]['simbol'] = "O"