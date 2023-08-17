FROM python:3.11-alpine@sha256:603975e62d85aa07578034d3d10ffa1983b7618a6abb6371cf51941be6b8842c
LABEL org.opencontainers.image.source https://github.com/brennerm/aws-quota-checker
WORKDIR /app
ADD setup.py /app
ADD README.md /app
ADD LICENSE /app
ADD Dockerfile /app
ADD aws_quota /app/aws_quota
RUN pip install .[prometheus]
RUN adduser --disabled-password aqc
USER aqc
ENTRYPOINT ["aws-quota-checker"]
CMD "--help"
