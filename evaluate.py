#!/usr/bin/env python3

from recommender import Client
import sys

visits = 0
tries = 0
guesses = 0

host, port = sys.argv[1].split(':')
c = Client(host, int(port))

# Pour document_id,person_id into this script
for row in sys.stdin:
    visits += 1
    row = row.split(',')

    # let's see if a person has already been here
    prs_hist = c.person_history(row[1])
    if len(prs_hist) > 0:

        # if so, we can try to guess current document_id
        # by looking into recommendations for the previous document_id
        prev_did = prs_hist[-1]
        rec = c.recommend(prev_did, row[1])

        # If we have something to recommend at all
        # and current document_id isn't the same as previous
        if len(rec) > 0 and prev_did != row[0]:

            # in my opinion, it wouldn't be fair to count
            # empty recs as a try, so, I increment tries only here
            tries += 1
            if row[0] in rec:

                # Hooray!
                guesses += 1

    # finally, record current visit to keep recommender up to date
    c.record(row[0], row[1])


print('Total visits:    {}'.format(visits))
print('Tries to guess:  {}'.format(tries))
print('Guesses:         {}'.format(guesses))
print('CTR:             {:.2f}%'.format(guesses*100/tries))

