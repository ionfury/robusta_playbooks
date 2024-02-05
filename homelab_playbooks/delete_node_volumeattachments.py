import logging

from typing import List
from robusta.api import NodeEvent, ErrorCodes, ActionException, action

from kubernetes import client

@action
def delete_node_volumeattachments(event: NodeEvent):
    """
    When a node is deleted, delete all related volume attachments, removing any finalizers.
    """
    body = {"metadata": {"finalizers": None}}  # Removing finalizers
    node = event.get_node()

    volume_attachments = client.StorageV1Api().list_volume_attachment()
    for volume_attachment in volume_attachments.items:
        if volume_attachment.spec.node_name == node.metadata.name:
            try:
                logging.info(f"delete_node_volumeattachments: deleting & removing finalizers from volume_attachment {volume_attachment.metadata.name} from node {node.metadata.name}")
                client.StorageV1Api().delete_volume_attachment(volume_attachment.metadata.name)
                client.StorageV1Api().patch_volume_attachment(volume_attachment.metadata.name, body)
            except Exception as e:
                raise ActionException(ErrorCodes.ACTION_UNEXPECTED_ERROR, f"delete_node_volumeattachments: failed to delete node volumeattachment {volume_attachment.metadata.name}")
