FROM registry.access.redhat.com/ubi8/ubi-minimal:8.1

RUN microdnf install python36 curl which
# && microdnf update \
# && microdnf clean all

WORKDIR /opt/tekton-jinja

COPY render.py /opt/tekton-jinja/src/
COPY Pipfile /opt/tekton-jinja/pyenv/
COPY render stage /opt/tekton-jinja/bin/

ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8" \
    LC_CTYPE="C.UTF-8" \
    WORKON_HOME=/opt/tekton-jinja/pyenv \
    PIPENV_NOSPIN=1

RUN pip3 install pipenv \
 && cd /opt/tekton-jinja/pyenv \
 && pipenv --python 3.6 install \
 && chown -R 9999:0 /opt/tekton-jinja \
 && chmod -R g+rwX /opt/tekton-jinja

# emulate an anonymous uid, which is better aligned with OpenShift environment
USER 9999

CMD [ "echo", "No default command" ]
