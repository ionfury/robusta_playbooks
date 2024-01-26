# Robusta_playbooks

This repository is for defining playbooks for [Robusta](https://docs.robusta.dev/master/index.html) for use in my home kubernetes deployments.

## Playbooks

- **delete_volumeattachment_in_detatcherror**:  Given a Prometheus alert, removes the finalizers on a `VolumeAttachment`` only when it is in a detach error state. Workaround for [this issue in longhorn](https://github.com/longhorn/longhorn-manager/blob/b810121b33789d145f220bfd0e41102a7801a354/csi/controller_server.go#L399).
