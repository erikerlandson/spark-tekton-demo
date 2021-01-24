FROM registry.access.redhat.com/ubi8/ubi-minimal:8.3

WORKDIR /opt/pyspark-s2i

# s2i scripts assemble, run
LABEL io.openshift.s2i.scripts-url=image:///opt/pyspark-s2i/s2i/bin

# s2i source loads here
# The s2i process creates the 'src' directory, so don't add it here
LABEL io.openshift.s2i.destination=/opt/pyspark-s2i

RUN microdnf install python36 wget tar gzip which \
 && pip3 install pipenv

COPY ./s2i/ /opt/pyspark-s2i/s2i/bin/
RUN chown -R 9999:0 /opt/pyspark-s2i \
 && chmod -R g+rwX /opt/pyspark-s2i

ENV OC_CLIENT_BINARY=openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit \
    OC_BIN=/opt/pyspark-s2i/bin
RUN mkdir -p $OC_BIN && \
    cd /tmp && \
    wget -nv https://github.com/openshift/origin/releases/download/v3.11.0/${OC_CLIENT_BINARY}.tar.gz && \
    tar xzf ${OC_CLIENT_BINARY}.tar.gz && \
    cd ${OC_CLIENT_BINARY} && \
    mv oc kubectl $OC_BIN && \
    chmod a+rx ${OC_BIN}/* && \
    cd /tmp && \
    rm -rf ${OC_CLIENT_BINARY} ${OC_CLIENT_BINARY}.tar.gz && \
    chown -R 9999:0 $OC_BIN && \
    chmod -R g+rwX $OC_BIN

ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8" \
    LC_CTYPE="C.UTF-8" \
    WORKON_HOME=/opt/pyspark-s2i/pyenv \
    PIPENV_NOSPIN=1

COPY Pipfile /opt/pyspark-s2i/pyenv/

RUN cd /opt/pyspark-s2i/pyenv \
 && pipenv --python 3.6 install \
 && chown -R 9999:0 /opt/pyspark-s2i/pyenv \
 && chmod -R g+rwX /opt/pyspark-s2i/pyenv

# emulate an anonymous uid, which is better aligned with OpenShift environment
USER 9999
