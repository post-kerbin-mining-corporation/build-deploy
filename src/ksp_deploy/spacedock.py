# Class for accessing the SpaceDock API
import requests
import logging
from contextlib import closing


class SpaceDockAPI(object):

    base_url = "https://spacedock.info"
    login_url = "api/login"
    query_mod_url = "api/mod/{mod_id}"
    update_mod_url = "api/mod/{mod_id}/update"

    def __init__(self, login, password, session=None):
        """
        Initializes the API session

        Inputs:
            login (str): SpaceDock user
            password (str): Spacedock PW
        """
        self.credentials = {"username":login, "password":password}

        self.logger = logging.getLogger('deploy.spacedock')

        if isinstance(session, requests.Session):
            self.session = session
        else:
            self.session =requests.Session()

    def query_mod(self, mod_id):
        """
        Queries the API for a mod

        Inputs:
            mod_id (str): SpaceDock mod ID

        Returns:
            response (dict): The query result
        """
        url = f'{self.base_url}/{self.query_mod_url}'.format(mod_id=mod_id)
        self.logger.info(f"Getting {url}")
        with closing(self.session.get(url)) as resp:
            try:
                m = getattr(resp, "json")
                return m() if callable(m) else m
            except requests.exceptions.HTTPError as err:
                self.logger.error(err)
                return resp.text

    def check_version_exists(mod_id, version):
    {
        """
        Checks to see if this version of the mod exists

        Inputs:
            mod_id (str): SpaceDock mod ID
            version (str): The version to check for

        Returns:
            exists (bool): Whether the version exists or not
        """
        data = self.query_mod(mod_id)
        versions = data["versions"]
        for v in versions:
            if v["friendly_version"] == version:
                self.logger.info(f"Spacedock already has {version}")
                return true
        return false
    }

    def update_mod(self, mod_id, version, changelog, game_version, notify_followers, zip):
        """
        Submits an update to a mod

        Inputs:
            mod_id (str): the Spacedock mod ID
            version (str): the string mod version to use
            changelog (str): a Markdown-formatted changelog
            game_version (str): the string game version to use
            notify_followers (bool): email followers
            zip (str): the path of the zip to upload

        """
        url = f'{self.base_url}/{self.update_mod_url}'.format(mod_id=mod_id)
        payload = {
            "version": version,
            "changelog": changelog,
            "game-version": game_version,
            "notify-followers": "yes" if True else "no"
        }
        self.logger.info(f"Posting {payload} to {url}")

        try:
            resp = self.session.post(url, data=payload, files={'zipball': open(zip, 'rb')})
            resp.raise_for_status()
            self.logger.info(f"{resp.url} returned {resp.text}")
            return resp.text
        except requests.exceptions.HTTPError as err:
            self.logger.error(f"HTTP ERROR: {err}")
            self.logger.error(f"{resp.url} returned {resp.text}")
            return resp.text


    def login(self):
        with closing(self.session.post(f'{self.base_url}/{self.login_url}', data=self.credentials)) as resp:
            if resp.reason == 'OK':
                self.logger.info("Successfully logged in")
                return self.session
            else:
                self.logger.error(f"Login error: {resp.text}")

    def logout(self):
        pass

    def close(self):
        self.session.close()

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, *args):
        self.logout()
        self.close()
