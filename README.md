# A template for your Django project

**Do not reinvent the wheel**: Here's is the project you should use as a template to create yours. Then, use our [Python Playbook](https://github.com/juntossomosmais/playbook/blob/master/backend/python.md) to guide you through the development process.

## ⚠ DOT NOT DELETE ME WITHOUT READING ME!

This project has the [example application](./django_template/apps/example) as a sample. You'll notice it has a [model](django_template/apps/example/models.py). You must delete it and then insert yours concerning your business rules. Look very carefully in the entire project to find names you should change. For instance, if your application name is Carl Sagan, you must change the folder `django_template` to `carl_sagan` and change any other required place.  Let's say, if you are not going to use [Django-Q](https://django-q.readthedocs.io/en/latest/), you must delete [this script](./scripts/start-worker.sh) from your main project.

To create your back-end application, you must use **Django**, **DRF**, and **Django STOMP**. Look at [this post](https://juntossomosmais.slack.com/archives/CGK0SU5BJ/p1644498920970319) on Slack. If you're willing to change them, please talk with your techlead and staff.
