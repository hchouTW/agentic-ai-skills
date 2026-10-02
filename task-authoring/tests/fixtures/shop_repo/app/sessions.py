_SESSIONS = {}  # in-process session store


def get(sid):
    return _SESSIONS.get(sid)


def put(sid, data):
    _SESSIONS[sid] = data
