# hideandseek
deep learning and privacy preserving deep learning library



    import hideandseek as hs

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cfg = OmegaConf.load('config.yaml') # omegaconf.OmegaConf.DictConfig object
    model = DNN() # torch.nn.Module object
    train_dataset = dataset # torch.utils.data.Dataset object
    kwargs = {
      'model': model,
      'dataset': train_dataset,
      'cfg_train': cfg,
      'criterion': criterion,
    }
    node = hs.Node(**kwargs)

    model.to(device)
    node.step(local_T=20, horizon='epoch')
    model.cpu()
