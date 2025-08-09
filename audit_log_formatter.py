import tempfile

async def to_json(audit_log):
    logs_json = []
    for log in audit_log:
        entry = {}
        entry["id"] = str(getattr(log, "id", ""))

        action = getattr(log, "action", None)
        if action is not None:
            entry["action"] = getattr(action, "name", str(action))

        category = getattr(log, "category", None)
        if category is not None:
            entry["category"] = getattr(category, "name", str(category))

        user = getattr(log, "user", None)
        if user is not None:
            user_id = getattr(user, "id", None)
            if user_id is not None:
                entry["user_id"] = str(user_id)
            entry["username"] = str(getattr(user, "name", user))

        target = None
        try:
            target = log.target
        except Exception:
            target = None
        if target is not None:
            try:
                target_id = getattr(target, "id", None)
            except Exception:
                target_id = None
            entry["target"] = str(target)
            if target_id is not None:
                entry["target_id"] = str(target_id)

        reason = getattr(log, "reason", None)
        if reason:
            entry["reason"] = reason

        created_at = getattr(log, "created_at", None)
        if created_at is not None:
            try:
                entry["created_at"] = created_at.isoformat()
            except Exception:
                entry["created_at"] = str(created_at)

        extra = getattr(log, "extra", None)
        if extra is not None:
            entry["extra"] = str(extra)

        logs_json.append(entry)

    return logs_json


async def to_csv(audit_log):
    audit_log_json = await to_json(audit_log)
    all_keys = []
    for d in audit_log_json:
        for k in d.keys():
            if k not in all_keys:
                all_keys.append(k)
    tmp = tempfile.NamedTemporaryFile(mode="w")
    tmp.write(",".join(all_keys))
    tmp.write("\n")
    for log_dict in audit_log_json:
        row = []
        for k in all_keys:
            v = log_dict.get(k, "")
            row.append(str(v))
        tmp.write(",".join(row))
        tmp.write("\n")
    tmp.seek(0)
    return tmp
