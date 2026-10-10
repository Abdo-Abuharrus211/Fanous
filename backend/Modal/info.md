# Introduction

For demo purposes, deploying a version of the app onto Modal's platform.
This directory houses modules used to run the service on Modal's platform and infrastructure, utilizing scalable
serverless capabilities and GPU inference.

# Running

To deploy this on Modal run this command:

```shell
uv add modal
odal secret create hf-token HF_TOKEN=xxx
modal deploy /backend/Modal/modal_server.py
```