import rtm
from types import *

apiKey = "c1a983bba360889c5089d5ccf1a94e4a"
secret = "67b5855d779f0d37"
token = "ad9ce7ad7956bbf1a02ae6a8963085025a800472"

ms = rtm.RTM(apiKey, secret, token)
l = ms.lists.getList()
lists = [{"archived":l.archived, 
    "deleted":l.deleted, 
    "id":l.id, 
    "locked":l.locked, 
    "name":l.name, 
    "position":l.position, 
    "smart":l.smart, 
    "sort_order":l.sort_order} for l in l.lists.list]
print lists

tsk = ms.tasks.getList(filter=u"")
tasks = list()

for ts in tsk.tasks.list:
    if (isinstance(ts.taskseries, ListType)):
        for t in ts.taskseries:
            tasks.append({"created":t.created, 
                "id":t.id, 
                "location_id":t.location_id, 
                "modified":t.modified, 
                "name":t.name, 
                "notes":t.notes, 
                "participants":t.participants, 
                "source":t.source, 
                "tags":t.tags, 
                "task":t.task, 
                "url":t.url})
    else:
        t = ts.taskseries
        tasks.append({"created":t.created, 
            "id":t.id, 
            "location_id":t.location_id, 
            "modified":t.modified, 
            "name":t.name, 
            "notes":t.notes, 
            "participants":t.participants, 
            "source":t.source, 
            "tags":t.tags, 
            "task":t.task, 
            "url":t.url})
print tasks
