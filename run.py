#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json
from pathlib import Path
import traceback

import twitter


PWD = Path(__file__).parents[0].resolve()


def write_log(filename, msg):
    with open(filename, 'a') as fp:
        ts = time.time()
        fp.write(f'{ts}\t{msg}\n')


if __name__ == '__main__':
    with open(PWD / 'twitter-api-key.json') as fp:
        twitter_key = json.loads(fp.read())

    twitter_api = twitter.Api(**twitter_key)

    resp = twitter_api.VerifyCredentials()
    user_id = resp.id

    max_id = None
    while True:
        resp = twitter_api.GetUserTimeline(user_id=user_id,
                                           exclude_replies=False,
                                           max_id=max_id)
        if not resp:
            break
        max_id = None
        for r in resp:
            try:
                twitter_api.DestroyStatus(status_id=r.id)
                max_id = r.id
                print(f'deleted {r}')
            except:
                continue
        time.sleep(10)
