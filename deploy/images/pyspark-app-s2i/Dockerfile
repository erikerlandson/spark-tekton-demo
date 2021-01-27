FROM quay.io/erikerlandson/pyspark-ubi:0.1.0

WORKDIR /opt/pyspark-s2i

# s2i scripts assemble, run
LABEL io.openshift.s2i.scripts-url=image:///opt/pyspark-s2i/bin

# s2i source loads here
# The s2i process creates the 'src' directory, so don't add it here
LABEL io.openshift.s2i.destination=/opt/pyspark-s2i

USER root:0

COPY ./s2i/ /opt/pyspark-s2i/bin/

# tar+gzip are used by standard s2i logic
# util-linux provides uuidgen, which can be used to generate uniqe spark cluster names
# wget could in theory be removed after the oc binary install but everything
# would need to be done in a single RUN to actually reduce total image size
RUN microdnf install wget tar gzip util-linux \
 && microdnf clean all

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
 && chown -R 9998:0 /opt/pyspark-s2i \
 && chmod -R g+rwX /opt/pyspark-s2i

# tell oc to generate kube config somewhere it's allowed to
ENV KUBECONFIG=/opt/pyspark-s2i/kubeconfig

# emulate an anonymous uid, which is better aligned with OpenShift environment
USER 9999:0
