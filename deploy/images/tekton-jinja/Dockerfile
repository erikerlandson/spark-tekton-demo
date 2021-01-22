FROM registry.access.redhat.com/ubi8/ubi-minimal:8.1

RUN microdnf install python36 curl
# && microdnf update \
# && microdnf clean all

WORKDIR /opt/tekton-jinja

COPY apply.py /opt/tekton-jinja/src/
COPY Pipfile /opt/tekton-jinja/run/
COPY run stage /opt/tekton-jinja/bin/

ENV LANG="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8" \
    LC_CTYPE="en_US.UTF-8"

RUN pip3 install pipenv \
 && cd /opt/tekton-jinja/run \
 && pipenv --python 3.6 install \
 && pipenv check \
 && chown -R 9999:0 /opt/tekton-jinja \
 && chmod -R g+rwX /opt/tekton-jinja

# emulate an anonymous uid, which is better aligned with OpenShift environment
USER 9999

CMD [ "echo", "No default command" ]
