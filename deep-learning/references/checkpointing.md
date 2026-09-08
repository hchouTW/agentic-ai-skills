# Checkpointing Reference

## Save training checkpoint

```python
torch.save({
    "epoch": epoch,
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "scheduler_state_dict": scheduler.state_dict() if scheduler else None,
    "best_metric": best_metric,
    "config": config,
}, path)
```

## Resume training

```python
ckpt = torch.load(path, map_location=device)
model.load_state_dict(ckpt["model_state_dict"])
optimizer.load_state_dict(ckpt["optimizer_state_dict"])
if scheduler is not None and ckpt.get("scheduler_state_dict") is not None:
    scheduler.load_state_dict(ckpt["scheduler_state_dict"])
start_epoch = ckpt["epoch"] + 1
```

## Inference-only weights

```python
torch.save(model.state_dict(), "model_weights.pt")
```

Load:

```python
state_dict = torch.load("model_weights.pt", map_location=device)
model.load_state_dict(state_dict)
model.eval()
```
