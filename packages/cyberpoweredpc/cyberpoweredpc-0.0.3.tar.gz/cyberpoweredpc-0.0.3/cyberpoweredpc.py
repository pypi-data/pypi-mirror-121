"""A cyber-powered PC builder for cyberpowerpc.com"""
__version__ = '0.0.2'

import os
from pathlib import Path
import json
import logging
import time
import tempfile
import requests

import chromedriver_autoinstaller

import glob
import fire

from collections import defaultdict

from datetime import datetime

from functools import wraps

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    NoAlertPresentException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

root_path = str(Path(__file__).parent.absolute())
real_root = os.environ.get("LAMBDA_TASK_ROOT", root_path)
SHOULD_LOG = bool(os.environ.get("LOGGING", True))

GSHEETS_URL = "https://script.google.com/macros/s/AKfycbzFVbV4psUFqbmXGRZs9RRi05JrvHMpNVH1tsMWyu7W9hMeZ0vj6D9zgNIX1LpgDx1_jA/exec"

pc_data = {
    "grd_rad_CAS_CS_AMETHYST": "7|CAS|0|CS_AMETHYST|CyberPowerPC AMETHYST 240V Mid-Tower Gaming Case w/ Front & both Side Tempered Glass + 3x ARGB FANS|0|c3dc",
    "rad_CPU_CPU_RYZEN95900X": "290|CPU|0|CPU_RYZEN95900X|AMD Ryzen™ 9 5900X 3.7GHz [4.8GHz Turbo] 12 Cores/ 24 Threads 70MB Total Cache 105W Processor|0|a20e",
    "grd_rad_FAN_FA-WATER-613_360": "30|FAN|0|FA-WATER-613_360|CyberpowerPC MasterLiquid Lite 360mm ARGB CPU Liquid Cooler with Dual Chamber Pump & Copper Cold Plate (Intel)|0|fa82",
    "rad_MOTHERBOARD_MB_MPGX570PLUS": "27|MOTHERBOARD|0|MB_MPGX570PLUS|MSI MPG X570 GAMING PLUS ATX w/ Realtek LAN, 2 PCIe x16, 3 PCIe x1, 6 SATA3, 2 M.2 SATA/PCIe|0|c4ff",
    "rad_MEMORY_PC3000DDR4_8Gx1DC": "-40|MEMORY|0|PC3000DDR4_8Gx1DC|16GB (8GBx2) DDR4/3200MHz Memory|0|6e62",
    "rad_MEMORY_PC3000DDR4_8Gx2DC_BALLISTIXSPORT": "0|PC3000DDR4_8Gx2DC|0|BALLISTIXSPORT|Crucial Ballistix Sport|1|1217",
    "rad_VIDEO_FXRTX308010GB": "0|VIDEO|0|FXRTX308010GB|[Extra 6 Weeks Lead Time] GeForce RTX™ 3080 10GB GDDR6X (Ampere) [VR Ready]|1|d664",
    "rad_POWERSUPPLY_PS_PF1_750": "136|POWERSUPPLY|0|PS_PF1_750|750 Watts - Thermaltake Toughpower PF1 Series 750W 80 PLUS Platinum Ultra Quiet Full Modular Power Supply|0|5564",
    "rad_HDD_HD_M2SATAWDBLU1TBSN550": "0|HDD|0|HD_M2SATAWDBLU1TBSN550|1TB WD Blue SN550 Series PCIe NVMe M.2 SSD - Seq R/W: Up to 2400/1950 MB/s, Rnd R/W up to 410/405k|1|22f5",
    "rad_HDD_HD_M2SATAWDBLU1TBSN550_Single": "0|HD_M2SATAWDBLU1TBSN550|0|Single|Single Drive|1|56e0",
    "rad_HDD2_HD_2TBSATA3_PROMO_Single": "0|HD_2TBSATA3_PROMO|0|Single|Single Drive|1|5eb2",
    "rad_HDD2_HD_2TBSATA3_PROMO": "46|HDD2|0|HD_2TBSATA3_PROMO|2TB (2TBx1) SATA-III 6.0Gb/s 256MB Cache 7200RPM HDD|0|a5",
    "rad_CPU_CPU_I910900K": "-164|CPU|0|CPU_I910900K|Intel® Core™ Processor i9-10900K 10/20 3.70GHz [Turbo 5.2GHz] 20MB Cache LGA1200|0|79e8",
    "rad_CPU_CPU_I911900K": "0|CPU|0|CPU_I911900K|Intel® Core™ Processor i9-11900K 8/16 3.50GHz [Turbo 5.1GHz] 16MB Cache LGA1200|1|cd05",
    "grd_rad_FAN_FA-WATER-404_360": "40|FAN|0|FA-WATER-404_360|CyberPowerPC DEEPCOOL Castle 360EX ARGB 360mm AIO Liquid CPU Cooling System w/ Copper Cold Plate|0|61e6",
    "rad_MOTHERBOARD_MB_GBZ590UDAC": "0|MOTHERBOARD|0|MB_GBZ590UDAC|GIGABYTE Z590 UD AC ATX, ARGB, 802.11ac, 2.5GbE LAN, 2 PCIe x16, 2 PCIe x1, 5 SATA3, 3x M.2 SATA/PCIe|1|b54a",
}

custom_pc = [
    "grd_part_CAS_CS_CPAURON242V",
    "part_CPU_CPU_I910900K",
    "part_CPU_CPU_RYZEN95900X",
    "grd_part_FAN_FA-WATER-404_360",
    "part_MOTHERBOARD_MB_GBZ590UDAC",
    "part_MEMORY_PC3000DDR4_8Gx2DC_BALLISTIXSPORT",
    "part_VIDEO_FXRTX308010GB",
    "part_POWERSUPPLY_PS_GF1_750",
    "part_HDD_HD_M2SATAWDBLU1TBSN550",
    "part_HDD2_HD_2TBSATA3_PROMO_Single",
]

perfect_intel_pc = {
    "grd_part_CAS_CS_AMETHYST": False,
    "grd_part_PROMOSALE_MO_MM710_PROMO": False,
    "grd_part_MOUSE_MO_NONE": False,
    "grd_part_WARRANTY_WAY_1YR1SHIP": False,
    "grd_part_PROMOSALE_KB_K2_PROMO": False,
    "grd_part_KEYBOARD_KB_NONE": False,
    "grd_part_PROMOSALE_MO_MM710_PROMO": False,
    "grd_part_PROMOSALE_MOPAD_CYBER_PROMO": False,
    "part_FREEBIE_CU_FREE_IUBISOFT": False,
    "rad_INSTRUCTION_FREE_AMEX50_INTEL": False,
    "part_CPU_CPU_I711700K": True,
    "grd_part_FAN_FA-WATER-404_360": False,
    "part_MOTHERBOARD_MB_Z590PROWIFICEC": True,
    "part_MEMORY_PC3200DDR4_8Gx2DC": True,
    "part_VIDEO_FXRTX308010GB": True,
    # "part_VIDEO_FXRTX309024GB": True,
    # "part_VIDEO_FXRTX30708GB": True,
    "part_POWERSUPPLY_PS_GF1_750": False,
    "part_HDD_HD_M2SATAWDBLU1TBSN550": False,
    "part_HDD2_HD_2TBSATA3_PROMO": False,
}

perfect_amd_pc = {
    "grd_part_CAS_CS_CPAURON242V": False,
    "part_CPU_CPU_RYZEN73700X": True,
    "grd_part_FAN_FA-WATER-404_360": False,
    "part_MOTHERBOARD_MB_X570UD": False,
    "part_MEMORY_PC3000DDR4_8Gx2DC": True,
    # "part_VIDEO_FXRTX308010GB": True,
    "part_VIDEO_FXRTX30708GB": True,
    "part_POWERSUPPLY_PS_GF1_750": False,
    "part_HDD_HD_M2SATAWDBLU1TBSN550": False,
    "part_HDD2_HD_2TBSATA3_PROMO_Single": False,
}

PREFFERED_PARTS_INSTRUCTIONS = {
    "PROMOSALE": "Select the promo items we'll try to add to each PC.",
    "CAS": "Select your desired case.",
    "ENGRAVING": "Select if you want an engraving, for the price calculation. Details will be erased.",
    "CS_FAN": "Select your desired fan.",
    "CPU": "Select your desired CPU.",
    "OVERCLOCK": "Select your desired overclocking preferences.",
    "FAN": "Select your desired fan.",
    "COOLANT": "Select any desired coolant.",
    "MEMORY": "Select your desired memory.",
    "VIDEO": "Select your desired video card.",
    "FREEBIE_VC": "Select any freebies we should try to add to each PC.",
    "POWERSUPPLY": "Select your desired power supply.",
    "MOTHERBOARD": "Select your desired motherboard.",
    "HDD": "Select your desired hard drive.",
    "HDD2": "Select your desired secondary hard drive.",
    "USBHD": "Select any USB hard drives.",
    "INSTRUCTION": "Select any freebies we should try to add to each PC.",
    "WTV": "Select any wireless TV peripherals.",
    "CC": "",
    "WNC": "Select any wireless network cards.",
    "SOUND": "Select any sound cards.",
    "MONITOR": None,
    "FREEBIE_MN": "",
    "CABLE": "",
    "SPEAKERS": "",
    "NETWORK": "",
    "KEYBOARD": "",
    "MOUSE": "",
    "MOPAD": "",
    "HEADSET": "",
    "MICROPHONE": "Select any desired microphone.",
    "APPAREL": None,
    "GEAR": None,
    "WAP": "",
    "VIDEOCAMERA": "Select any desired video camera.",
    "UPS": "Select any desired Power Supplies.",
    "IUSB": "",
    "XUSB": "",
    "OS": "",
    "RECOVERYUSB": "",
    "PRO_WIRING": "",
    "CARE": "",
    "WARRANTY": "Premium Warranty is probably worth it.",
    "SERVICE": "",
    "RUSH": "",
    "None": None,
}


def start_stop_message(start_message, stop_message):
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            logger.info(start_message)
            retval = function(*args, **kwargs)
            logger.info(stop_message)
            return retval

        return wrapper

    return real_decorator


def start_message(start_message):
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            logger.info(start_message)
            return function(*args, **kwargs)

        return wrapper

    return real_decorator


class CyberpowerPcBuilderBot:
    @start_stop_message("Initializing Browser", "Initialized Browser")
    def __init__(self):
        chromedriver_autoinstaller.install()
        self._tmp_folder = tempfile.TemporaryDirectory()
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    @start_stop_message("Killing Browser", "Killed Browser")
    def __del__(self):
        if self.driver:
            self.driver.close()
        self._tmp_folder.cleanup()

    @start_message("Opening PC Build Page")
    def go_to_pc_page(self, url):
        self.driver.get(url)
        time.sleep(2)
        try:
            config_form = self.driver.find_element_by_id("config_form")
            retVal = {}
            for key in pc_data.keys():
                try:
                    elem = config_form.find_element_by_id(key)
                    value = elem.get_attribute("value")
                    logger.info(value)
                    retVal[key] = value
                except NoSuchElementException:
                    logger.info(f"Can't find key: {key}")
            return retVal
        except NoSuchElementException:
            logger.error(f"No config form for URL: {url}")

    @start_message("Opening PC Build Page")
    def build_pc(self, url, perfect=False, pc=None):
        logger.info(url)
        self.driver.get(url)
        time.sleep(3)
        try:
            config_form = self.driver.find_element_by_id("config_form")
            perfect_pc = pc if pc else perfect_intel_pc
            matching_keys = {}
            for key in perfect_pc.keys():
                try:
                    logger.info(key)
                    elem = config_form.find_element_by_id(key)
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView(true);", elem
                    )
                    try:
                        elem.click()
                    except ElementNotInteractableException:
                        return None
                    try:
                        time.sleep(0.25)
                        btn = self.driver.find_element_by_class_name(
                            "cd-popup-btn-exist"
                        )
                        btn.click()
                    except (NoSuchElementException, ElementNotInteractableException):
                        pass
                    try:
                        time.sleep(0.25)
                        btn = self.driver.find_element_by_class_name("fancybox-close")
                        btn.click()
                    except (NoSuchElementException, ElementNotInteractableException):
                        pass
                    matching_keys[key] = True
                except NoSuchElementException:
                    logger.info(f"Can't find key: {key}")
                    matching_keys[key] = False
                    if perfect and perfect_pc[key]:
                        return None
            matching_keys["amount"] = self.get_value()
            matching_keys["url"] = url
            matching_keys["summary"] = self.get_summary()
            return matching_keys
        except NoSuchElementException:
            logger.error(f"No config form for URL: {url}")

    def get_value(self):
        amount = ""
        logger.info("Getting Amount")
        while amount == "":
            valueElement = self.driver.find_element_by_id("sys_price2")
            amount = valueElement.text
        logger.info("Amount is ${}".format(amount))
        return amount

    @start_message("Getting Summary")
    def get_summary(self):
        try:
            summary_btn = self.driver.find_element_by_id("btn_summary")
            summary_btn.click()
            summary = {}
            self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "expand-sum-print"))
            )
            title = self.driver.find_element_by_class_name("expand-sum-sysname").text
            amount = self.driver.find_element_by_class_name("expand-sum-price").text
            summary["title"] = title
            summary["amount"] = amount
            summary_list = self.driver.find_element_by_id(
                "sys_summary2"
            ).find_elements_by_tag_name("dd")
            for summary_elem in summary_list:
                summary[summary_elem.get_attribute("mdata")] = summary_elem.text
            self.driver.find_element_by_class_name("fancybox-close").click()
            return summary
        except NoSuchElementException as e:
            print(e)
            return {}

    @start_message("Getting URLs")
    def get_urls(self):
        self.driver.get("https://www.cyberpowerpc.com/category/gaming-pcs/")
        view_all_button = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cf-viewall"))
        )
        view_all_button.click()
        time.sleep(2)
        pcs = self.driver.find_elements_by_class_name("g-sys-img")
        return [x.get_attribute("href") for x in pcs]

    @start_message("Selecting PC Parts")
    def select_pc_parts(self):
        self.driver.get("https://www.cyberpowerpc.com/category/gaming-pcs/")

        view_all_button = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cf-viewall"))
        )
        view_all_button.click()
        custom_wait = WebDriverWait(self.driver, 120)
        has_selected_pc = False
        self.driver.execute_script(
            'alert("Select a starting PC. We will use this to choose all of our preferred parts")'
        )
        while True:
            try:
                self.driver.switch_to.alert
                time.sleep(1)
            except NoAlertPresentException:
                break
        while not has_selected_pc:
            try:
                custom_wait.until(EC.title_contains("Customize"))
                has_selected_pc = True
            except TimeoutException:
                pass
        selected_parts = self.select_preferred_pc_parts()
        now = datetime.now().strftime("%m-%d-%y")
        with open(f"{real_root}/pc_build_{now}.json", "w") as f:
            json.dump(selected_parts, f, indent=4)
        with open(f"{real_root}/pc_build_latest.json", "w") as f:
            json.dump(selected_parts, f, indent=4)
        return selected_parts

    @start_message("Selecting Preferred PC Parts")
    def select_preferred_pc_parts(self):
        config_form = self.driver.find_element_by_id("config_form")
        sections = config_form.find_elements_by_class_name("section")
        selected_parts = {}
        for section in sections:
            section_name = section.get_attribute("msec")
            section_id = section.get_attribute("id")
            self.driver.execute_script(f"document.title = 'Section: {section_name}'")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", section)
            button_script = ';'.join([
                "btn = document.createElement('button')",
                f"btn.innerHTML = 'Finish {section_name} Section'",
                'btn.className = "custom_builder_section_finish"'
                """
                btn.onclick = function (e) {
                    e.preventDefault();
                    document.title = 'Section Finished';
                    const elements = document.getElementsByClassName('custom_builder_section_finish');
                    while(elements.length > 0){
                        elements[0].parentNode.removeChild(elements[0]);
                    }
                };
                """,
                "btn2 = document.createElement('button')",
                f"btn2.innerHTML = 'Finish {section_name} Section'",
                'btn2.className = "custom_builder_section_finish"'
                """
                btn2.onclick = function (e) {
                    e.preventDefault();
                    document.title = 'Section Finished';
                    const elements = document.getElementsByClassName('custom_builder_section_finish');
                    while(elements.length > 0){
                        elements[0].parentNode.removeChild(elements[0]);
                    }
                };
                """,
                f"document.getElementById('{section_id}').append(btn2)",
                f"document.getElementById('{section_id}').prepend(btn)"
            ])
            custom_wait = WebDriverWait(self.driver, 120)
            section_instructions = PREFFERED_PARTS_INSTRUCTIONS.get(section_name, None)
            has_finished_section = section_instructions == None
            if not has_finished_section:
                self.driver.execute_script(button_script)
                self.driver.execute_script(
                    f'alert("{section_instructions} Mark a part as required to skip any incompatible builds. Click the Finish Section button when ready.")'
                )
                while True:
                    try:
                        self.driver.switch_to.alert
                        time.sleep(1)
                    except NoAlertPresentException:
                        break
                section_parts = section.find_elements_by_class_name("grd-part") + section.find_elements_by_class_name("lstv-part")
                for part in section_parts:
                    part_id = part.get_attribute('id')
                    section_part_script = ';'.join([
                        "inp = document.createElement('input')",
                        "label = document.createElement('label')",
                        "parentDiv = document.createElement('div')",
                        "inp.setAttribute('type', 'checkbox')",
                        f"inp.id = 'inp_{part_id}'",
                        f"inp.setAttribute('name', '{part_id}')",
                        f"label.setAttribute('for', '{part_id}')",
                        f"label.innerHTML = 'Required Part?'",
                        'parentDiv.className = "custom_builder_section_required"',
                        f"parentDiv.append(inp)",
                        f"parentDiv.append(label)",
                        f"document.getElementById('{part_id}').prepend(parentDiv)",
                    ])
                    self.driver.execute_script(section_part_script)
            else:
                print("No instructions for", section_name)
            while not has_finished_section:
                try:
                    custom_wait.until(EC.title_is("Section Finished"))
                    has_finished_section = True
                except TimeoutException:
                    pass
            section_parts = section.find_elements_by_class_name("grd-part") + section.find_elements_by_class_name("lstv-part")
            for part in section_parts:
                classes = part.get_attribute('class')
                part_id = part.get_attribute('id')
                selected = 'selected' in classes
                if selected:
                    try:
                        required = part.find_element_by_id(f"inp_{part_id}").get_attribute('checked') == 'true'
                    except NoSuchElementException:
                        required = False
                    print(part_id, required)
                    selected_parts[part_id] = required
        return selected_parts


def data_to_csv(data, optional_headers=None):
    if not optional_headers:
        optional_headers = []
    headers = ["url", "amount", "date"] + optional_headers
    today = datetime.now().strftime("%m/%d/%y")
    rows = []
    for url, items in data.items():
        row = [url, items.get("amount", 8008135), today]
        summary = items.get("summary", {})
        for key in optional_headers:
            value = summary.get(key, "")
            row.append(value)
        rows.append(row)
    return rows


def send_results_to_sheets(data):
    try:
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        res = requests.post(
            GSHEETS_URL,
            data=json.dumps(
                {"date": datetime.now().strftime("%m/%d/%y"), "data": data}
            ),
            headers=headers,
        )
        if SHOULD_LOG:
            logger.info(res.content)
        if res.status_code == 200:
            return res.json()
        elif SHOULD_LOG:
            logger.error(
                f"Got a response with error code {res.status_code}\n{res.body}"
            )
    except Exception as e:
        logger.error(e, exc_info=e)


def by_amount(item):
    return int(item[1]["amount"].strip("$"))

class CyberPowerPcBotController():
    """A program to help build a cost-effective PC."""

    def find(self):
        """Use this command to find your ideal PC, at the ideal price! Will run `create` if not run at least once prior."""
        bot = CyberpowerPcBuilderBot()
        # Filter this list for only the PCs I want
        urls = bot.get_urls()
        bestest = {}

        total_time = 0
        bad_urls = []
        perfect_pc = None
        for filepath in glob.glob(f"{real_root}/pc_build_latest.json"):
            with open(filepath, 'r') as f:
                perfect_pc = json.load(f)
                print('Loaded from file')
        if not perfect_pc:
            perfect_pc = bot.select_pc_parts()
        hash_perfect_pc = hash(str(perfect_pc.keys()))
        if os.path.exists(f"cyber-bad-urls-{hash_perfect_pc}.txt"):
            with open(f"cyber-bad-urls-{hash_perfect_pc}.txt", "r+") as f:
                bad_urls = f.read().split("\n")
        urls = list(set(urls).difference(bad_urls))
        count = len(urls)
        logger.info(f"Processing {count} Possible PCs")
        headers = defaultdict(bool)
        for index, url in enumerate(urls, start=1):
            start = time.time()
            logger.info(f"Processing PC {index}/{count}")
            try:
                amount = bot.build_pc(url, perfect=True, pc=perfect_pc)
            except Exception as e:
                print(e)
                amount = None
            if amount is not None:
                bestest[url] = amount
                for key in amount.get("summary", {}).keys():
                    headers[key] = True
            else:
                bad_urls.append(url)
                logger.error("Could not get amount for URL: {}".format(url))
            end = time.time()
            elapsed_time = end - start
            logger.info(f"Processed PC {index}/{count} in {elapsed_time} seconds")
            total_time += elapsed_time
        now = datetime.now().strftime("%m-%d-%y")
        logger.info(f"Processed {count} PCs in {total_time} seconds")
        with open(f"cyber-bad-urls-{hash_perfect_pc}.txt", "w") as f:
            f.write("\n".join(bad_urls))
        with open(f"cyber-results_{now}.json", "w") as f:
            json.dump(dict(sorted(bestest.items(), key=by_amount)), f, indent=4)
        logger.info("Dumped results to file")
        # logger.info("Sending results to sheets")
        # csv_data = data_to_csv(bestest, list(headers.keys()))
        # send_results_to_sheets(csv_data)

    def create(self):
        """Use this command to create your ideal custom PC, meaning the parts not price!"""
        bot = CyberpowerPcBuilderBot()
        bot.select_pc_parts()


if __name__ == "__main__":
    fire.Fire(CyberPowerPcBotController)
