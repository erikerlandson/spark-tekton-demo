FROM quay.io/erikerlandson/pyspark-ubi:0.1.0-spark-2.4.7-py-3.6

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
# note, this one binary adds over 70MB to the image size
ENV OC_CLIENT_RELEASE=4.6.0-0.okd-2021-01-23-132511 \
    OC_BIN=/opt/pyspark-s2i/bin
RUN mkdir -p $OC_BIN \
 && cd /tmp \
 && wget -nv https://github.com/openshift/okd/releases/download/${OC_CLIENT_RELEASE}/openshift-client-linux-${OC_CLIENT_RELEASE}.tar.gz \
 && tar xzf openshift-client-linux-${OC_CLIENT_RELEASE}.tar.gz \
 && mv oc $OC_BIN \
 && rm -rf /tmp/* \
 && chown -R 9998:0 /opt/pyspark-s2i \
 && chmod -R g+rwX /opt/pyspark-s2i

# tell oc to generate kube config somewhere it's allowed to
ENV KUBECONFIG=/opt/pyspark-s2i/kubeconfig

# emulate an anonymous uid, which is better aligned with OpenShift environment
USER 9999:0
