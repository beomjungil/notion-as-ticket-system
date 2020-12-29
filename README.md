# Notion-as-ticket-system

> Use your favorite tool, Notion as better issue tracker for GitHub<br/>
> **[Example](https://www.notion.so/beomjungil/Notion-as-ticket-system-578c2caf61094f04ab04094d96c7866d#bc8c5e1c27ea4e16bce5caafa7a73cbd)**

## Features

[Check Notion](https://www.notion.so/beomjungil/Notion-as-ticket-system-578c2caf61094f04ab04094d96c7866d#24c8a8116f6043b68e2544cddf743f38)

## Issues

[Notion Link](https://www.notion.so/beomjungil/d050b6907fe94dd2ba268956f80fd6bd?v=bda2e696f2754b10bc64bea49ccb6558)

## Development

1. Copy `setting.example.yaml` in same directory and Rename with `setting.yaml`
2. Change to valid values
3. Install Python dependencies
4. Type `./bin.start` on terminal to start 

## Create Docker Image

```bash
# Create Image
$ docker build -t notion-as-ticket-system:<tag> ./

# Start Container with 80 port
$ docker run -d --name <Container Name> -p 80:80 notion-as-ticket-system:<tag>
```
