FROM quay.io/odh-jupyterhub/s2i-spark-minimal-notebook:py36-spark2.4.5-hadoop2.7.3

# first cut is to simply use the pre-installed spark & pyspark from base image

USER root

# s2i scripts assemble, run
LABEL io.openshift.s2i.scripts-url=image:///opt/spark-app/s2i/bin

# s2i source loads here
# The s2i process creates the 'src' directory, so don't add it here
LABEL io.openshift.s2i.destination=/opt/spark-app

COPY ./s2i/ /opt/spark-app/s2i/bin/
COPY ./bin/ /opt/spark-app/bin/

RUN gzip -d /opt/spark-app/bin/oc.gz \
 && mkdir -p /opt/spark-app/src \
 && chown -R 9999:0 /opt/spark-app \
 && chmod -R g+rwX /opt/spark-app

# emulate anonymous uid
USER 99999
