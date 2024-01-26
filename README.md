# Robusta_playbooks

This repository is for defining playbooks for [Robusta](https://docs.robusta.dev/master/index.html) for use in my home kubernetes deployments.

## Playbooks

- **delete_volumeattachment_in_detatcherror**:  Given a Prometheus alert, deletes a `VolumeAttachment`` only when it is in a detach error state.
