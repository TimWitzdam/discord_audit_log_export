import tempfile


async def to_json(audit_log):
    logs_json = []

    for log in audit_log:
        log_dict = {
            'user_id': str(log.user.id),
            'username': str(log.user.name),
            'action': str(log.action.name),
            'reason': log.reason,
            'created_at': log.created_at.isoformat(),
        }
        if log.target:
            log_dict["target"] = f"{str(log.target)} ({str(log.target.id)})" if log.target.id else str(log.target),

        logs_json.append(log_dict)

    return logs_json


async def to_csv(audit_log):
    audit_log_json = await to_json(audit_log)
    tmp = tempfile.NamedTemporaryFile(mode="w")
    tmp.write(",".join(audit_log_json[0].keys()))
    tmp.write("\n")
    for log_dict in audit_log_json[1:]:
        for value in log_dict.values():
            tmp.write(f"{value},")
        tmp.write("\n")

    tmp.seek(0)
    return tmp
