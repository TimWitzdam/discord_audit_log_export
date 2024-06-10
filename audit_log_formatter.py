import tempfile


async def to_json(audit_log, limit=1000):
    logs_json = []

    for log in audit_log:
        log_dict = {
            'target': str(log.target),
            'user_id': str(log.user.id),
            'username': str(log.user.name),
            'action': str(log.action.name),
            'reason': log.reason,
            'created_at': log.created_at.isoformat(),
        }

        """change_dict = {
            'before': log.changes.before,
            'after': log.changes.after
        }
        log_dict['changes'].append(change_dict)
"""
        logs_json.append(log_dict)

    return logs_json


async def to_csv(audit_log, limit=1000):
    audit_log_json = await to_json(audit_log, limit)
    tmp = tempfile.NamedTemporaryFile(mode="w")
    tmp.write(",".join(audit_log_json[0].keys()))
    tmp.write("\n")
    for log_dict in audit_log_json[1:]:
        for value in log_dict.values():
            tmp.write(f"{value},")
        tmp.write("\n")

    return tmp
