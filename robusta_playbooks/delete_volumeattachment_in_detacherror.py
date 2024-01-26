import logging

from robusta.api import ActionException, ErrorCodes, PrometheusKubernetesAlert, action

from kubernetes import client
from kubernetes.client import V1VolumeAttachmentStatus

def delete_volume_attachment(volume_attachment_name):
    """
    Deletes a volume attachment.
    """
    try:
        api_response = client.StorageV1Api().delete_volume_attachment(volume_attachment_name)
        logging.info(f"VolumeAttachment {volume_attachment_name} deleted: {api_response}")
    except Exception as e:
        ActionException(ErrorCodes.ACTION_UNEXPECTED_ERROR, f"Exception when calling StorageV1Api->delete_volume_attachment: {e}")

@action
def delete_volumeattachment_in_detacherror(event: PrometheusKubernetesAlert):
    """
    Deletes a volumeattachment only when it is in a detach error state.
    """

    volume_attachment_name = event.alert.labels.get('volumeattachment')

    if volume_attachment_name is None:
        raise ActionException(ErrorCodes.RESOURCE_NOT_FOUND, f"VolumeAttachment name not found in alert labels")

    try:
        volume_attachment_status: V1VolumeAttachmentStatus = client.StorageV1Api().read_volume_attachment_status(volume_attachment_name)

        if volume_attachment_status.detach_error is not None:
            logging.info(f"detachError found in {volume_attachment_name}.  Deleting...")
            delete_volume_attachment(volume_attachment_name)
        else:
            logging.info(f"No detachError found in {volume_attachment_name}.")

    except Exception as e:
        raise ActionException(ErrorCodes.ACTION_UNEXPECTED_ERROR, f"Failed to detect volume attachment status for {volume_attachment_name}")
