import time
import logging
import uiautomator2 as u2
from mobly import test_runner
from mobly import base_test
from mobly.controllers import android_device


class AndroidToggleTest(base_test.BaseTestClass):
    def setup_class(self):
        self.ads = self.register_controller(android_device)
        self.dut = self.ads[0]
        self.device = u2.connect(self.dut.serial)
        self.android_version = self._get_android_version()
        logging.info(f"Connected to device: {self.dut.serial}, Android version: {self.android_version}")

        self.dut.adb.shell("input keyevent KEYCODE_WAKEUP")
        self.dut.adb.shell("wm dismiss-keyguard")
        self.dut.adb.shell("svc power stayon true")

    def _get_android_version(self):
        version = self.dut.adb.shell("getprop ro.build.version.release")
        version = version.decode().strip()  # Decode bytes to string
        return int(version.split(".")[0])


    def _wait_for_element(self, selector, timeout=10):
        for _ in range(timeout):
            if selector.exists:
                return selector
            time.sleep(1)
        raise TimeoutError(f"Element not found: {selector}")

    def _find_switch(self, hint=""):
        for _ in range(3):
            switch = self.device(className="android.widget.Switch")
            if switch.exists:
                return switch
            self.device(scrollable=True).scroll.to(textContains=hint)
            time.sleep(1)
        raise Exception(f"Switch not found near: {hint}")

    def _toggle_switch(self, switch, enable=True):
        if not switch.exists:
            raise Exception("Switch not found")
        current_state = switch.info.get('checked')
        if current_state != enable:
            switch.click()
            time.sleep(2)
            self._handle_confirmation_popup()
            for _ in range(5):
                if switch.exists and switch.info.get('checked') == enable:
                    logging.info(f"Switch set to {'ON' if enable else 'OFF'}")
                    return
                time.sleep(1)
            raise AssertionError(f"Failed to set switch to {enable}")
        else:
            logging.info(f"Switch already {'ON' if enable else 'OFF'}")

    def _handle_confirmation_popup(self):
        popup = self.device(textMatches="(?i)yes|ok|allow|continue")
        if popup.exists(timeout=3):
            popup.click()
            logging.info("Confirmation popup handled")
            time.sleep(1)

    def test_01_wifi_toggle(self):
        logging.info("Test 01: Wi-Fi toggle")
        self.dut.adb.shell("am start -a android.settings.WIFI_SETTINGS")
        time.sleep(3)

        if self.android_version >= 14:
            self.device(textContains="Internet").click_exists(timeout=5)
        elif self.android_version == 13:
            self.device(scrollable=True).scroll.to(textContains="Network")
            self.device(textContains="Internet").click_exists(timeout=5)
        else:
            self.device(scrollable=True).scroll.to(text="Wi‑Fi")
            self.device(text="Wi‑Fi").click_exists(timeout=5)

        wifi_switch = self._find_switch("Wi‑Fi")
        self._toggle_switch(wifi_switch, True)
        time.sleep(1)
        self._toggle_switch(wifi_switch, False)

    def test_02_bluetooth_toggle(self):
        logging.info("Test 02: Bluetooth toggle")
        self.dut.adb.shell("am start -a android.settings.BLUETOOTH_SETTINGS")
        time.sleep(3)

        self.device(scrollable=True).scroll.to(textContains="Bluetooth")
        bt_switch = self._find_switch("Bluetooth")
        self._toggle_switch(bt_switch, True)
        time.sleep(2)

        if self.device(textContains="Pair new device").click_exists(timeout=5):
            logging.info("Scanning for devices...")
            # Replace with a known nearby device name
            target_device = "YourDeviceName"
            for _ in range(10):
                if self.device(text=target_device).exists:
                    self.device(text=target_device).click()
                    logging.info("Device found and clicked")
                    break
                time.sleep(2)
            else:
                logging.warning("Device not found. Skipping pairing step.")
        else:
            logging.warning("'Pair new device' not found")

        if self.device(text='Pair').exists:
            self.device(text='Pair').click()
        elif self.device(text='OK').exists:
            self.device(text='OK').click()
        time.sleep(3)

        self._toggle_switch(bt_switch, False)

    def test_03_location_toggle(self):
        logging.info("Test 03: Location toggle")
        self.dut.adb.shell("am start -a android.settings.LOCATION_SOURCE_SETTINGS")
        time.sleep(3)

        self.device(scrollable=True).scroll.to(textContains="Location")
        loc_switch = self._find_switch("Location")
        self._toggle_switch(loc_switch, True)
        time.sleep(1)
        self._toggle_switch(loc_switch, False)

    def test_04_mobile_data_toggle(self):
        logging.info("Test 04: Mobile Data toggle")

        if self.android_version >= 14:
            self.dut.adb.shell("am start -a android.settings.DATA_USAGE_SETTINGS")
        else:
            self.dut.adb.shell("am start -n com.android.settings/.Settings")
            time.sleep(2)
            self.device(scrollable=True).scroll.to(textContains="Network")
            self.device(textContains="Network").click_exists(timeout=5)
            time.sleep(2)
            self.device(textContains="Mobile network").click_exists(timeout=5)

        time.sleep(3)
        self.device(scrollable=True).scroll.to(textContains="Mobile")
        data_switch = self._find_switch("Mobile")

        self._toggle_switch(data_switch, True)
        time.sleep(2)

        # Turn OFF with confirmation if needed
        if data_switch.exists:
            data_switch.click()
            time.sleep(2)
            if self.device(textMatches="(?i)turn off|disable|yes|ok").exists:
                self.device(textMatches="(?i)yes|ok").click_exists(timeout=3)
            time.sleep(2)

            # Verify OFF
            if not data_switch.info.get('checked'):
                logging.info("Mobile Data turned OFF successfully")
            else:
                raise AssertionError("Mobile Data toggle OFF failed")

            self._toggle_switch(data_switch, True)

    def teardown_class(self):
        self.dut.adb.shell("input keyevent KEYCODE_HOME")
        logging.info("Returned to Home screen")


if __name__ == "__main__":
    test_runner.main()
