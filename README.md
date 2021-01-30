# spark-tekton-demo

demo of running apache spark jobs using tekton and s2i workflows

This repository contains implementations of two styles of tekton pipeline for running spark jobs.
1. executing the spark job directly in a pipeline task step.
1. spawning an independent pod that runs the spark job.

I view the first option (embedding the spark run directly in the pipeline) as the preferable architecture,
however the second implementation demonstrates a true S2I build of a runnable image that can spawn its own ephemeral
spark cluster and run the job against it.

Below are instructions for running both demos on an OpenShift cluster,
using OpenShift Pipelines to provide the cluster tekton operator and
the Open Data Hub community operator to provide the Spark operator that services ephemeral Spark clusters.

These demos should also be runnable on Kubernetes, using "community" tekton,
with some modifications to supply tekton pipelines and tasks with the necessary service accounts,
and manually installing the Spark operator directly.

### Demo of spark job run directly in a tekton pipeline

1. Create a project namespace in your OpenShift cluster to use for your demo.
1. Make sure that the Open Data Hub (ODH) operator and the Openshift Pipelines operator are installed. In OpenShift this can be done via the Operator Catalog.
1. Create a deployed instance of the ODH operator in your namespace. It requires the odh sub-components for: spark, prometheus. Other components (seldon, superset, strimzi, etc) can be left off.
1. Install the yaml files in the `deploy/pipelines` directory into your namespace. The command `oc apply -R -f deploy/pipelines` will install all the objects used by both demos.
1. This version of the demo also uses the `git-clone` task from the standard tekton catalog: `oc apply -f https://raw.githubusercontent.com/tektoncd/catalog/v1alpha1/git/git-clone.yaml`
1. Go to the `Pipelines` screen of your namespace, and you should see a pipeline named `spark-tekton-demo`. Start a run of this pipeline.
1. Make sure you choose a PVC for the `staged-repo` workspace, e.g. `spark-tekton-demo` as created from the yaml in this repo. This is important because the workspace is used to pass data between tasks, and the default `emptyDir` will lose data after each task, and the demo will fail.
1. Pipeline parameters are defaulted to run the 'spark-pi' example that is contained in this demo repository.
1. Once the pipeline run finishes, you can examine the log output for the task named `run-spark-task`. You should see the results of your spark run, as shown below
1. This version of the demo cleans up the SparkCluster and companion Service object in a final task. Once you delete the pipeline run, all objects associated with the run will be deleted.

Example output from version 1 of the demo.
Find this in the `spark-run-task` log outputs.
```
+ cd /staged/src/examples/spark-pi
+ python3 spark-app.py
21/01/30 17:43:15 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Attaching to Spark cluster spark-cluster-d51b669b-4ec7-4935-b676-60d003ea9d81
[Stage 0:> (0 + 2) / 2] 
Running Spark job to compute pi
====================================================
Pi is roughly 3.139900
====================================================
```

### Demo of spark job that is spawned as an independent pod

1. Create a project namespace in your OpenShift cluster to use for your demo.
1. The pod that runs spark in this demo must have permissions to create objects on your cluster. To give the `default` service-account full project admin privs: `$ oc policy add-role-to-user admin -z default -n <your-namespace>`
1. Make sure that the Open Data Hub (ODH) operator and the Openshift Pipelines operator are installed. In OpenShift this can be done via the Operator Catalog.
1. Create a deployed instance of the ODH operator in your namespace. It requires the odh sub-components for: spark, prometheus. Other components (seldon, superset, strimzi, etc) can be left off.
1. Install the yaml files in the `deploy/pipelines` directory into your namespace. The command `oc apply -R -f deploy/pipelines` will install all the objects used by both demos.
1. This version of the demo also uses jinja from tekton, so install: `oc apply -f https://raw.githubusercontent.com/erikerlandson/tekton-jinja/0.1.0/task-tekton-jinja.yaml`
1. Go to the `Pipelines` screen of your namespace, and you should see a pipeline named `spark-tekton-demo-pod`. Start a run of this pipeline.
1. Make sure you choose a PVC for the `render` workspace, e.g. `spark-tekton-demo` as created from the yaml in this repo. This is important because the workspace is used to pass data between tasks, and the default `emptyDir` will lose data after each task, and the demo will fail.
1. Pipeline parameters are defaulted to run the 'spark-pi' example that is contained in this demo repository.
1. Once the pipeline finishes, you should now have a pod named `spark-tekton-demo-xxxxxx...` in your project pods.
1. If you watch the log output of this pod, it should eventually finish with log output like the example below.
1. The pod `spark-tekton-demo-xxxxxxx` is not deleted when you delete the pipeline-run, so if you want to get rid of these you'll need to do it manually.

Example output from version 2 of this demo.
Find this log output in the logs for the independent pod spawned to run your spark job.
```
RUNNING spark application:
21/01/30 16:36:44 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Attaching to Spark cluster spark-cluster-346f1a0d-27ce-4754-8080-25d70ec807a1
[Stage 0:>                                                          (0 + 0) / 2]
Running Spark job to compute pi
====================================================
Pi is roughly 3.143140
====================================================

TEARING DOWN EPHEMERAL SPARK spark-cluster-346f1a0d-27ce-4754-8080-25d70ec807a1
sparkcluster.radanalytics.io "spark-cluster-346f1a0d-27ce-4754-8080-25d70ec807a1" deleted
TEARING DOWN companion Service
service "spark-tekton-demo-346f1a0d-27ce-4754-8080-25d70ec807a1" deleted

RUN FINISHED
```
