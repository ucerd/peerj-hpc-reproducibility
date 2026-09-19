# Reference architecture

```mermaid
flowchart TB
  A["Institutional Service Layer<br/>Teaching | Research | External Projects | Innovation"]
  B["AI & Data Platform Layer<br/>Jupyter/IDEs | ML Environments | Model Registry | Data Governance"]
  C["System Software & Resource Management<br/>Slurm | Containers | Modules | Portal | IAM | Monitoring"]
  D["Physical HPC Infrastructure<br/>CPU | GPU | Login/Management | Storage | Low-Latency Network"]

  D --> C --> B --> A
```

The layers are designed jointly. Physical resources without scheduler, identity,
storage policy, reproducibility mechanisms, support, and institutional service
ownership constitute a cluster, but not yet a sustainable university
cyberinfrastructure service.
