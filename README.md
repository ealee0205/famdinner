# famdinner
## Overview
Project Famdinner is a my personal work in progress to create an app that let's my friends know when I'm studying at a coffee shop, walking at the park, or hosting an open-invite dinner so they can drop in spontaneously and hang out like its an episode from a sitcom. After undergrad, the opportunities for spontaneous interactions has significantly diminished. Post-grad life took from us the ability to just pop into the library or knock on someone's door, but these are the catalytic events that lead to organic communities. Famdinner creates windows of spontaneity in a structured world.

## Design
The app is currently a Flask web application with Jinja HTML templates, CSS, and Javascript.
The database is on a SQLite server.
This is currently just a developing ground that is hosted on my local network (so you wouldn't be able to access it..)

Now obviously, that's not a mature enough stack for a production system, which is why these are the next steps I'm currently taking:

### TODO: New Framework
Flask was simple and flask was what I learned, but if we want real spontaneity, its gotta be a mobile app. I'm rewriting the front end in Swift and the back end as a REST API.

### TODO: Production Capable Database
You may have noticed that the data is stored in a SQLite server, which is convenient for testing queries locally, but not production-ready. The goal is to migrate this to something stronger, like a Postgres server.

### TODO: CI/CD Pipeline
The Docker containerization allows me to deploy it on my PC locally, but right now, I'm undergoing a DevOps project to install Ubuntu bare-metal on an old PC to then partition that into separate dev/prod environments using libvirt, and then get a CI/CD pipeline using Gitlab. Stay tuned because this is the next change that is coming!

### Deployment
I _might_ deploy publically if I feel comfortable opening up an access point or paying AWS to host there. Otherwise, its still a WIP, but I'll let you know once it's officially live!
