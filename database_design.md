# Database Design:

### Needed Types
1. Project (also proposal)
2. User
3. Organization
4. Vote

----------------
[Currently all DB design is assuming a NoSQL Model using JSON blobs]


##### Project Node:
```
{
    "id": 123098493287 (unique ID #)
    "title": "Name your project"
    "text" : "The bulk description written in .md format"
    "short_desciption": "The description you'll write up for summary views of the project in 144 characters"
    "date": Unix Timestamp
    "budget": 1384.98 (some float)
    "owner": 1093824098 (User ID #)
    "organization": 2342345 (organization ID #)
    "members": [2340898, 920385, 23948084] (list of user ID #s)
    "complete": 0 (boolean on whether this project has been filed as completed)
    "base_node": 2341234324 (project ID # that is the base of this proposal or phase; if it is 0 then you know this is the root of the project or that it is a proposal)
    "phases": [2309840, 02983490, 203984098] List of other Project ID #s; if it is a proposal, this will be "None"]
    "next_phase": 902384098 (next chronological phase; if it is a proposal, this will be "None"; if it is the last phase of a project, we could have a placeholder like -1 or something)
    "vote_status": 0 [Has this been voted on?  This boolean will be reset if a new vote is awaiting]
    "to_do": [("fix JS", 098203498, 0), ("write overview", 08230984,1)]   (list of tuples for to-do items on this particular project or phase and who is the lead for each item, and whether it is done)
}
```


##### User Node: [May want to consider using a Gravitar or similar ID system]
```
{
    "id": 23947987234 (user ID #)
    "name": user_name
    "pass_token": ... (some password)
    "e-mail": me@you.com
    "organizations": [2903840, 9084205] (list of organizations belonged to)
    "owner": [908430198, 0928340] (list of projects and proposal on which this user has owner permissions)
    "member": [2390480, 93028408] (list of projects that user has voting permissions)
    "following": [90832048, 09832048] (list of projects you are following)
    "join_date": Unix Timestamp
}
```


##### Organization:
```
{
    "id": 2903840398 (organization ID #)
    "name": CoLab, or whatever
    "owners": [239832434908, 092830498] (list of those with owner permissions)
    "members": [90823048, 09820384, 08923048] (Those following this organization)
    "start_date": Unix Timestamp
    "short_description": "What is this organization?"
}
```

##### Vote:
```
{
    "initiator": 908230498 (user ID # of who requested vote)
    "base_node": 098320984 (project ID for what is being voted on)
    "content": "Description of what is being voted on."
    "majority": .5 (percent needed to pass)
    "voters": [239408, 0982304] (list of user IDs who have permission to vote)
    "votes": [0, 1, 0 ,1] (list of votes in boolean form)
    "passed": 0 (boolean representing whether this vote was a pass or fail)
}
```


