#!/usr/bin/env python3
# coding: utf-8

import os
import subprocess


class RepositoryInterface:
    def __init__(self, result_path: str, script_path: str = None):
        self.result_path = result_path
        self.script_path = script_path

    def _read_commitinfo(self) -> list:
        if self.script_path:
            subp = subprocess.run(
                ['bash', self.script_path],
                capture_output=True
            )
            return subp.stdout.decode('utf-8').splitlines()
        if not os.path.isfile(self.result_path):
            return []
        with open(self.result_path) as fin:
            lines = (s.strip() for s in fin.readlines())
            return [s for s in lines if s]

    def get_commitinfo(self):
        lines = self._read_commitinfo()
        keys = ['branch', 'author', 'commit', 'committed_at', 'message']
        n = len(keys)
        if len(lines) < n:
            return {}
        info = dict(zip(keys, lines[:n]))
        info['status'] = lines[n:]
        return info
