# spark-app-s2i

demo of source to image that creates an ephemeral spark cluster and runs a spark job against it

This demo currently has some warts:
- It needs a service account with permissions to create a SparkCluster object in the namespace. Currently it just assumes that `default` has been edited with admin privs.

### How to run:

1. Create a project namespace in your OpenShift cluster
1. Make sure that the `default` service-account has admin privs: `$ oc policy add-role-to-user admin -z default -n <your-namespace>`
1. Make sure that Open Data Hub operator and the Openshift Pipelines operator are installed
1. Create a deployed instance of the ODH operator in your namespace. It requires the odh sub-components to run jupyterhub and spark. Other components can be left off.
1. Install the yaml files in the `deploy` directory into your project. (except for `job-spark-app.yaml` which is used by the pipeline itself)
1. Also install: `oc apply -f https://raw.githubusercontent.com/erikerlandson/tekton-jinja/0.1.0/task-tekton-jinja.yaml`
1. Create a PVC, name it something like `spark-demo-pvc`. You will need this when kicking off the pipeline run.
1. Go to the `Pipelines` screen of your namespace, and you should see a pipeline named `spark-app`
1. Make sure you choose a PVC for the `render` workspace, e.g. `spark-demo-pvc` as mentioned above. This is important because the `render` workspace is used to pass data between tasks, and the default `emptyDir` will lose data after each task, and the demo will fail.
1. Once the pipeline finishes, you should now have a pod named `spark-app-xxxxxx...` in your project pods.
1. If you watch the log output of this pod, it should eventually finish with log output like the example below.
1. The pod `spark-app-xxxxx...` and corresponding service `spark-app-xxxxx...` are not deleted when you delete the pipeline-run, so if you want to get rid of these you'll need to do it manually.


```
RUNNING spark application:
Attaching to Spark cluster spark-cluster-0c68529a
21/01/18 23:16:29 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Running Spark job to compute pi
[Stage 0:>                                                          (0 + 0) / 2]  .......
====================================================
Pi is roughly 3.143480
====================================================

TEARING DOWN EPHEMERAL SPARK spark-cluster-0c68529a
sparkcluster.radanalytics.io "spark-cluster-0c68529a" deleted

RUN FINISHED
```
