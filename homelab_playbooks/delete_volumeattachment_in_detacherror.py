import logging

from robusta.api import ActionException, ErrorCodes, PrometheusKubernetesAlert, action

from kubernetes import client
from kubernetes.client import V1VolumeAttachment, V1VolumeAttachmentStatus

def delete_volume_attachment(volume_attachment_name):
    """
    Deletes a volume attachment.
    """
    try:
        client.StorageV1Api().delete_volume_attachment(volume_attachment_name)
        logging.info(f"delete_volumeattachment_in_detacherror: VolumeAttachment {volume_attachment_name} deleted.")
    except Exception as e:
        ActionException(ErrorCodes.ACTION_UNEXPECTED_ERROR, f"delete_volumeattachment_in_detacherror: Exception when calling StorageV1Api->delete_volume_attachment: {e}")

def patch_volume_attachment_finalizers(volume_attachment_name):
    """
    Patches out the finalizers on a VolumeAttachment.
    """
    body = {"metadata": {"finalizers": None}}  # Removing finalizers
    try:
        client.StorageV1Api().patch_volume_attachment(volume_attachment_name, body)
        logging.info(f"delete_volumeattachment_in_detacherror: VolumeAttachment {volume_attachment_name} patched.")
    except Exception as e:
        ActionException(ErrorCodes.ACTION_UNEXPECTED_ERROR, f"delete_volumeattachment_in_detacherror: Exception when calling StorageV1Api->patch_volume_attachment: {e}")

@action
def delete_volumeattachment_in_detacherror(event: PrometheusKubernetesAlert):
    """
    Deletes a volumeattachment only when it is in a detach error state.
    """
    volume_attachment_name = event.alert.labels.get('volumeattachment')

    if volume_attachment_name is None:
        raise ActionException(ErrorCodes.RESOURCE_NOT_FOUND, f"delete_volumeattachment_in_detacherror: VolumeAttachment name not found in alert labels")

    try:
        volume_attachment: V1VolumeAttachment = client.StorageV1Api().read_volume_attachment_status(volume_attachment_name)

        volume_attachment_status: V1VolumeAttachmentStatus = volume_attachment.status

        if volume_attachment_status.detach_error is not None:
            logging.info(f"delete_volumeattachment_in_detacherror: detachError found in {volume_attachment_name}.  Deleting...")
            patch_volume_attachment_finalizers(volume_attachment_name)
        else:
            logging.info(f"delete_volumeattachment_in_detacherror: No detachError found in {volume_attachment_name}.")

    except Exception as e:
        raise ActionException(ErrorCodes.ACTION_UNEXPECTED_ERROR, f"delete_volumeattachment_in_detacherror: Failed to detect volume attachment status for {volume_attachment_name}: {e}")
