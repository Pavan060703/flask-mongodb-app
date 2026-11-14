
# Flask + MongoDB on Kubernetes (Minikube)

A Flask app with `/` and `/data` endpoints, backed by MongoDB with authentication. It runs on Minikube with persistent storage, a Secret for credentials, and CPU-based autoscaling (HPA).

Docker image: `pavanvbhavsar2003/flask-mongodb-app:1.1`

## Project structure
```
flask-mongodb-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
├── screenshots/
└── k8s/
    ├── 01-mongo-secret.yaml
    ├── 02-mongo-pv.yaml
    ├── 03-mongo-pvc.yaml
    ├── 04-mongo-service.yaml
    ├── 05-mongo-statefulset.yaml
    ├── 06-flask-deployment.yaml
    ├── 07-flask-service.yaml
    └── 08-flask-hpa.yaml
```

## Prerequisites
Docker Desktop, Minikube, kubectl, a Docker Hub account.

## 1. Build and push the image
```
docker build --platform linux/amd64 -t pavanvbhavsar2003/flask-mongodb-app:1.1 .
docker login
docker push pavanvbhavsar2003/flask-mongodb-app:1.1
```

## 2. Start Minikube
```
minikube start --driver=docker --cpus=2 --memory=2200
minikube addons enable metrics-server
```

## 3. Deploy
```
kubectl apply -f k8s/
kubectl get pods,svc,pv,pvc,hpa
```

## 4. Access the app
```
minikube service flask-service --url
```
Keep that terminal open, then test with the printed URL:
```
curl.exe <url>/
Invoke-RestMethod -Method Post -Uri "<url>/data" -ContentType "application/json" -Body '{"sampleKey":"sampleValue"}'
curl.exe <url>/data
```

## 5. DNS resolution in the cluster
Kubernetes runs CoreDNS in the `kube-system` namespace, and every pod sends its DNS lookups there. Each Service gets a name like `<service>.<namespace>.svc.cluster.local`, so the MongoDB Service is `mongodb.default.svc.cluster.local`. Pods in the same namespace can use the short name `mongodb`.

Flask reads `MONGO_HOST=mongodb`, asks CoreDNS for that name, and connects to port 27017. The MongoDB Service is headless (`clusterIP: None`), so CoreDNS returns the MongoDB pod's own IP. The pod IP changes on restart, but the DNS name stays the same.

## 6. Resource requests and limits
A **request** is the amount of CPU and memory a container is guaranteed. The HPA measures CPU as a percentage of the request. A **limit** is the maximum a container may use (CPU over the limit is throttled, memory over the limit is OOMKilled).

| | CPU | Memory |
|---|---|---|
| Request | 200m | 250M |
| Limit | 500m | 500M |

The HPA target of 70% means it scales up when pods average more than 140m CPU. MongoDB uses `--wiredTigerCacheSizeGB 0.25` to stay under its 500M limit (measured about 238Mi).

## 7. Design choices
| Choice | Why | Alternative | Why not |
|---|---|---|---|
| StatefulSet for MongoDB | Stable pod name and its own disk | Deployment | Pod names change, replicas could share one disk |
| Headless Service | Internal only, direct pod DNS | Normal ClusterIP | Hides pod identity a database needs |
| NodePort for Flask | Simple to reach from a laptop | LoadBalancer / Ingress | Needs extra setup |
| hostPath PV, Retain policy | Works on one-node Minikube, keeps data if PVC is deleted | Dynamic StorageClass | Better for real multi-node clusters |
| Secret for credentials | Password kept out of code and image | Plain env values | Visible in the Deployment |
| mongo:7.0 pinned | Repeatable builds | latest | Version could change |
| python:3.11-slim, non-root user | Small and safer | Full image | Bigger image |
| Readiness and liveness probes | Traffic only to ready pods | No probes | Requests could hit starting pods |

## 8. Testing

### Database
- Login with the password works, and the data is visible in mongosh.
- Without the password MongoDB answers `Command find requires authentication`.
- After `kubectl delete pod mongodb-0`, the data was still there, so the PV works.

### Autoscaling (HPA results)
HPA settings: target 70% CPU, min 2 pods, max 5 pods.

Load was generated with three busybox pods that call Flask in a loop:
```
kubectl run load-1 --image=busybox:1.36 --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://flask-service:5000/ > /dev/null; done"
kubectl run load-2 --image=busybox:1.36 --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://flask-service:5000/ > /dev/null; done"
kubectl run load-3 --image=busybox:1.36 --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://flask-service:5000/ > /dev/null; done"
```

| Stage | Load pods | CPU (TARGETS) | Flask replicas | Notes |
|---|---|---|---|---|
| Baseline | 0 | 1% | 2 | idle |
| Load started | 3 | 113% | 2 | passed the 70% target |
| Scale-up | 3 | 113% | 4 | HPA added 2 pods |
| Stable under load | 3 | 51% to 72% | 4 | about 108m CPU per pod |
| Load stopped | 0 | 1% | 4 | waits for the stabilization window |
| After about 5 min | 0 | 1% | 2 | scaled back to the minimum |

Summary: under load, CPU rose to 113% of the 70% target and the HPA scaled Flask from 2 to 4 pods. CPU then settled around 51% to 72%. After the load stopped, CPU fell to 1% and replicas returned to 2 after about 5 minutes (Kubernetes' default scale-down wait).

![HPA scale up](screenshots/result%201.png)
![Top pods under load](screenshots/result%202.png)
![HPA scale down](screenshots/result%203.png)

### Problems I hit and how I fixed them
1. `docker build` failed with `exec format error`. Building with `--platform linux/amd64` fixed it.
2. The C: drive was full, so Docker went read-only and Minikube would not start. I cleaned the disk and moved Docker's disk image to D:.
3. Flask connected to `localhost:27017` because the first image was built before the auth code change. I rebuilt it as tag `1.1`.
4. The HPA first showed `unable to get metrics` until metrics-server warmed up.

## Clean up
```
kubectl delete -f k8s/
minikube stop
```
