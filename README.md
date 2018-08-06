# SonarSource Java checks using bblfsh

This repo contains the implementation of some
[SonarSource](https://rules.sonarsource.com/java) Java checks using the
[bblfsh](https://doc.bblf.sh/) project.

This repository is intended both a test and a demo of bblfsh capabilities.

## How to run

```bash
pip install bblfsh
docker run -d --name bblfshd --privileged -p 9432:9432 bblfsh/bblfshd
```

And then go to the `python` subdirectory and run the checks. Every check will
be run against a Java file with the same name in the `java` directory.
