FROM registry.access.redhat.com/ubi8/ubi-minimal:8.3

WORKDIR /opt/pyspark-s2i

# s2i scripts assemble, run
LABEL io.openshift.s2i.scripts-url=image:///opt/pyspark-s2i/s2i/bin

# s2i source loads here
# The s2i process creates the 'src' directory, so don't add it here
LABEL io.openshift.s2i.destination=/opt/pyspark-s2i

COPY ./s2i/ /opt/pyspark-s2i/s2i/bin/
COPY Pipfile /opt/pyspark-s2i/pyenv/

# I'm using python 3.6 specifically, as it's known to work everywhere
# and the ODH spark-cluster images from the ephemeral cluster also use it.
# tar+gzip are used by standard s2i logic
# 'which' is used by pipenv to locate a python interpreter to run
# wget could in theory be removed after the oc binary install but everything
# would need to be done in a single RUN to actually reduce total image size
RUN microdnf install python36 wget tar gzip which \
 && microdnf clean all \
 && pip3 install pipenv

# download and install the 'oc' static binary
# note, this one binary adds about 100MB to the image size
ENV OC_CLIENT_BINARY=openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit \
    OC_BIN=/opt/pyspark-s2i/bin
RUN mkdir -p $OC_BIN \
 && cd /tmp \
 && wget -nv https://github.com/openshift/origin/releases/download/v3.11.0/${OC_CLIENT_BINARY}.tar.gz \
 && tar xzf ${OC_CLIENT_BINARY}.tar.gz \
 && cd ${OC_CLIENT_BINARY} \
 && mv oc $OC_BIN \
 && chmod a+rx ${OC_BIN}/* \
 && cd /tmp \
 && rm -rf ${OC_CLIENT_BINARY} ${OC_CLIENT_BINARY}.tar.gz \
 && chown -R 9999:0 /opt/pyspark-s2i \
 && chmod -R g+rwX /opt/pyspark-s2i

# environment for doing the pipenv install of the Pipfile
# WORKON_HOME tells pipenv to put the virtualenv in same dir so
# it gets properly used when container runs using anonymous uid
ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8" \
    LC_CTYPE="C.UTF-8" \
    WORKON_HOME=/opt/pyspark-s2i/pyenv \
    PIPENV_NOSPIN=1

# after the install, deleting caches and /tmp saves over 800MB
RUN cd /opt/pyspark-s2i/pyenv \
 && pipenv --python 3.6 install \
 && rm -rf /tmp/* /root/.cache /root/.local \
 && chown -R 9999:0 /opt/pyspark-s2i/pyenv \
 && chmod -R g+rwX /opt/pyspark-s2i/pyenv

# && pipenv lock --clear \
# && rm -rf /tmp/* \

# emulate an anonymous uid, which is better aligned with OpenShift environment
USER 9999
