import os


def get_compute_context_id():
    return hash(f"{os.environ.get('HOSTNAME')}_{os.environ.get('USERNAME')}")