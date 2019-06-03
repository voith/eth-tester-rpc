from contextlib import (
    contextmanager,
)
from decimal import (
    Decimal,
)
import json
from time import (
    monotonic,
    sleep,
)
import urllib.request
import warnings
import zipfile

from splinter.driver import (
    DriverAPI,
)

METAMASK_DOWNLOAD_URL = 'https://github.com/MetaMask/metamask-extension/' \
                        'releases/download/v{version}/{extension_basename}.zip'


def change_maifest_key(manifest_path, key):
    with open(manifest_path, "r") as fr:
        manifest = json.load(fr)
        manifest['key'] = key
        with open(manifest_path, "w") as fw:
            json.dump(manifest, fw)


def download_metamask(version, extension_basename, extension_dir):
    dl_url = METAMASK_DOWNLOAD_URL.format(
        version=version,
        extension_basename=extension_basename
    )
    temporary_zipfile, _ = urllib.request.urlretrieve(dl_url)
    with zipfile.ZipFile(temporary_zipfile) as metamask_zip:
        metamask_zip.extractall(path=extension_dir)


class MetamaskNotificationWindowNotOpen(Exception):
    pass


@contextmanager
def ignore_deprecation_warnings():
    # Splinter uses some deprecated selenium API when switching windows which needlessly spams logs,
    # and as such this is needed. Though we could move it somewhere else
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        yield


class MetamaskExtension:
    def __init__(self, browser: DriverAPI, rpc_port, seed_phrase, address):
        self._seed_phrase = seed_phrase
        self._address = address
        self._browser = browser
        self._rpc_port = rpc_port
        self._password = "abracadabra123"

    @contextmanager
    def _extension_page(self, page):
        previous_url = self._browser.url
        page_url = self._get_page_url(page)
        if previous_url != page_url:
            self._browser.visit(page_url)
        yield
        if previous_url != page_url:
            self._browser.visit(previous_url)

    @contextmanager
    def _switch_to_notification_window(self, *, wait_time=5):
        current_window, metamask_window = self._get_current_and_notification_windows(
            wait_time=wait_time
        )
        if current_window is not metamask_window:
            self._browser.switch_to.window(metamask_window.name)

            yield

            self._browser.switch_to.window(current_window.name)
        else:
            yield

    def _get_current_and_notification_windows(self, *, wait_time=5):
        start_time = monotonic()
        current_window, metamask_window = None, None
        while True:
            with ignore_deprecation_warnings():
                for window in self._browser.windows:
                    if window.is_current:
                        current_window = window
                    if window.title == 'MetaMask Notification':
                        if metamask_window is not None:
                            raise RuntimeError("more than one metamask notification window found")
                        metamask_window = window
            if metamask_window is not None:
                return current_window, metamask_window
            if start_time - monotonic() > wait_time:
                raise MetamaskNotificationWindowNotOpen(
                    "metamask notification window not open")
            else:
                sleep(1)

    def _get_page_url(self, page):
        # NOTE: this id is controlled by the key in manifest.json in the exchange dir
        return f"chrome-extension://kijbclonokjjccmfnkapjafbgkimopfd/{page}"

    def initialize(self):
        browser = self._browser

        # Open metamask page in chrome
        with self._extension_page('home.html'):
            getting_started_btn = browser.find_by_css(".first-time-flow__button")
            if len(getting_started_btn) == 0:
                return
            sleep(2)
            with ignore_deprecation_warnings():
                browser.windows[1].close()  # close the window it opens

            # Full page view with fox
            browser.find_by_css(".first-time-flow__button").click()
            sleep(1)

            # Create password -> restore from seed phrase
            browser.find_by_css(".first-time-flow__button").click()
            browser.find_by_css(".btn-default.page-container__footer-button").click()
            browser.find_by_css(".first-time-flow__textarea").fill(self._seed_phrase)
            browser.find_by_id("password").fill(self._password)
            browser.find_by_id("confirm-password").fill(self._password)
            browser.find_by_css(".first-time-flow__checkbox").click()
            browser.find_by_css(".first-time-flow__button").click()
            sleep(2)
            browser.find_by_css(".first-time-flow__button").click()

    def change_network(self, network):
        network_map = {
            "mainnet": "Main Ethereum Network",
            "kovan": "Kovan Test Network",
            "ropsten": "Ropsten Test Network",
            "testrpc": "Test rpc",
        }
        if network not in network_map:
            raise ValueError(
                f"invalid network: {network}. valid values: {', '.join(network_map.keys())}"
            )
        browser = self._browser
        with self._extension_page('home.html'):
            browser.find_by_css('.network-indicator').click()

            network = browser.find_by_text(network_map[network])
            if len(network) > 0:
                browser.find_by_text(network_map[network]).click()
            else:
                browser.find_by_text("Custom RPC").click()
                browser.find_by_css('#network-name').fill("testrpc")
                browser.find_by_css('#rpc-url').fill("http://localhost:{}".format(self._rpc_port))
                browser.find_by_css('#chainId').fill("99")
                browser.find_by_text("Save").click()

            sleep(1)

    def visit_home(self):
        self._browser.visit(self._get_page_url('home.html'))

    def get_balance(self):
        self.visit_home()
        element = self._browser.find_by_css('.token-amount').first
        balance_title = element['title']
        balance_str, _, token_symbol = balance_title.partition(' ')
        assert token_symbol == 'ETH'
        return Decimal(balance_str)

    def confirm_notification(self):
        with self._switch_to_notification_window():
            self._browser.find_by_css(".button.btn-primary").click()

    def deposit_amount(self, address, amount):
        self.visit_home()
        self._browser.find_by_xpath(
            '//button[contains(text(), "Send")]'
        ).click()
        self._browser.find_by_xpath(
            '//input[@placeholder="Recipient Address"]'
        ).fill(address)
        self._browser.find_by_xpath(
            '//input[@type="number"]'
        ).fill(str(amount))
        self._browser.find_by_xpath(
            '//button[contains(text(), "Next")]'
        ).click()
        self._browser.find_by_xpath(
            '//button[contains(text(), "Confirm")]'
        ).click()
