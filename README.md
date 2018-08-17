# SonarSource Java checks using bblfsh

This repo contains the implementation of some
[SonarSource](https://rules.sonarsource.com/java) Java checks using the
[bblfsh](https://doc.bblf.sh/) project.

This repository is intended both a test and a demo of bblfsh capabilities.

## How to run

```bash
docker run -d --name bblfshd --privileged -p 9432:9432 bblfsh/bblfshd
pip install bblfsh_sonar_checks
sonarbblfsh --language=java --enable=RSPEC-1143,RSPEC-2975 somefile.java
```

Or using a shorter format for the checks code:

```
sonarbblfsh --language=java --enable=1143,2975 somefile.java
```

You can list the available checks along with the description URL with:

```bash
sonarbblfsh --language=java --list
```
