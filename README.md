# spark-app-s2i

demo of source to image that creates an ephemeral spark cluster and runs a spark job against it

This demo currently has some warts:
- It needs a service account with permissions to create a SparkCluster object in the namespace. Currently it just assumes that `default` has been edited with admin privs.
- It cannot create a uniqe id suffix for objects, so it's resulting object names `spark-app-demo` are hardcoded
- Its git repo is hard coded due to inflexible nature of git tekton resources
- You have to enter the project namespace has part of the pipeline parameter form.

### How to run:

1. Create a project namespace in your OpenShift cluster
1. Make sure that the `default` service-account has admin privs: `$ oc policy add-role-to-user admin -z default -n spark`
1. Make sure that Open Data Hub operator and the Openshift Pipelines operator are installed
1. Create a deployed instance of the ODH operator in your namespace. It requires the odh sub-components to run jupyterhub and spark. Other components can be left off.
1. Install the yaml files in the `deploy` directory into your project. (except for `job-spark-app.yaml` which is used by the pipeline itself)
1. Go to the `Pipelines` screen of your namespace, and you should see a pipeline named `spark-app`
1. Start up a pipeline run: you will need to enter your namespace in this form.
1. Once the pipeline finishes, you should now have a pod named `spark-app-demo` in your project pods.
1. If you watch the log output of this pod, it should eventually finish with log output like the example below.
1. Since this demo currently creates objects of same name each time, you need to manually remove pod `spark-app-demo` and service `spark-app-demo` before you run it again.


```
RUNNING spark application:
Attaching to Spark cluster spark-cluster-0c68529a
21/01/18 23:16:29 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Running Spark job to compute pi
[Stage 0:>                                                          (0 + 0) / 2]  .......
Pi is roughly 3.143480
====================================================

TEARING DOWN EPHEMERAL SPARK spark-cluster-0c68529a
sparkcluster.radanalytics.io "spark-cluster-0c68529a" deleted

RUN FINISHED
```
