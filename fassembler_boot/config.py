def config(path):
    fp = open(path)
    _config = {}
    for line in fp.readlines():
        line = line.strip()
        if not line: continue
        if line.startswith('#'): continue
        key, val = line.split('=')
        key = key.strip()
        val = val.strip()
        _config[key] = val
    fp.close()
    return _config
