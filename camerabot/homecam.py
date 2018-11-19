import logging
from datetime import datetime
from io import BytesIO

import requests
from PIL import Image
from requests.auth import HTTPDigestAuth


class HomeCam:
    """Camera class."""

    def __init__(self, api, user, password, description):
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.debug('Initializing {0}'.format(description))

        self._api = api
        self._user = user
        self._password = password
        self.description = description
        self._req = requests
        self.snapshots_taken = 0

    def take_snapshot(self, update, resize=False):
        """Takes and returns full or resized snapshot from the camera."""
        self._log.debug('Snapshot from {0}'.format(self._api))

        try:
            auth = HTTPDigestAuth(self._user, self._password)
            response = self._req.get(self._api, auth=auth, stream=True)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            self._log.error('Connection to {0} failed'.format(self.description))
            update.message.reply_text(
                'Connection to {0} failed, try later or /list other cameras'.format(self.description))
            return None, None

        snapshot_timestamp = int(datetime.now().timestamp())
        self.snapshots_taken += 1

        snapshot = self._resize_snapshot(response.raw) if resize else response.raw
        return snapshot, snapshot_timestamp

    def _resize_snapshot(self, raw_snapshot):
        """Resizes and returns JPEG snapshot."""
        size = 1280, 724
        snapshot = Image.open(raw_snapshot)
        resized_snapshot = BytesIO()

        snapshot.resize(size, Image.ANTIALIAS)
        snapshot.save(resized_snapshot, 'JPEG', quality=90)
        resized_snapshot.seek(0)

        self._log.debug("Raw snapshot: {0}, {1}, {2}".format(snapshot.format, snapshot.mode, snapshot.size))
        self._log.debug("Resized snapshot: {0}".format(size))

        return resized_snapshot
