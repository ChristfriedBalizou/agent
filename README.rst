Agent
=====

The following project aim to continuously deploy a git repository
directory into production or development environment.

Context
-------

Based on the work done and being a user of Kubernetes and Docker, I wanted to build something lite which use the Linux system standard service and cron job to orchestrate the workflow.

Linux is a complete environment and the safer I ever used it provide everything to organize your application.

As this tools you can write your own or do it manually. This tool is here to help me in my personal work to deploy simply pushing a commit or a tag to a repository and trigger a workflow to deploy and handle my application as a Linux service. I could also push further to use `systemd` to create safe containers an run each server in it's own container sharing the computer resource but die and crash alone.

An agent will create a service and a cron job for a given application.


Service
-------

The service will be use as a normal linux service
status stop start and restart.

Cron
----

The cron job will watch the repository and if a change occur
will trigger a workflow update the service and restart the application.
