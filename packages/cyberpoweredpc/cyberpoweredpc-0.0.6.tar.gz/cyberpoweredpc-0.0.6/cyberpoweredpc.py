import os
from pathlib import Path
import json
import logging
import time
import tempfile

import chromedriver_autoinstaller

import easygui
import glob
import fire

from datetime import datetime

from functools import wraps

from selenium import webdriver
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

PREFFERED_PARTS_INSTRUCTIONS = {
    "PROMOSALE": "Select the promo items we'll try to add to each PC. We recommend adding any mouse and keyboard promo, and removing the included mouse and keyboard from the cart.",
    "ENGRAVING": "Select if you want an engraving, for the price calculation. Details will be erased.",
    "CPU": "We recommend setting this as a required part.",
    "VIDEO": "We recommend setting this as a required part.",
    "MOTHERBOARD": "We recommend setting this as a required part.",
    "WARRANTY": "Premium Warranty is probably worth it.",
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
    def build_pc(self, url, perfect=False, pc=None):
        logger.info(url)
        self.driver.get(url)
        time.sleep(3)
        try:
            config_form = self.driver.find_element_by_id("config_form")
            perfect_pc = pc if pc else {}
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
                        logger.error(f'Cannot click {key}')
                        pass
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
        results_path = get_preferred_path()
        with open(f"{results_path}/pc_build_{now}.json", "w") as f:
            json.dump(selected_parts, f, indent=4)
        with open(f"{results_path}/pc_build_latest.json", "w") as f:
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
            button_script = ";".join(
                [
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
                    f"document.getElementById('{section_id}').prepend(btn)",
                ]
            )
            custom_wait = WebDriverWait(self.driver, 120)
            section_instructions = PREFFERED_PARTS_INSTRUCTIONS.get(section_name, None)
            has_finished_section = False
            if not has_finished_section:
                self.driver.execute_script(button_script)
                if section_instructions is not None and section_instructions != '':
                    self.driver.execute_script(
                        f'alert("{section_instructions} Mark a part as required to skip any incompatible builds. Click the Finish Section button when ready.")'
                    )
                    while True:
                        try:
                            self.driver.switch_to.alert
                            time.sleep(1)
                        except NoAlertPresentException:
                            break
                section_parts = section.find_elements_by_class_name(
                    "grd-part"
                ) + section.find_elements_by_class_name("lstv-part")
                for part in section_parts:
                    part_id = part.get_attribute("id")
                    section_part_script = ";".join(
                        [
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
                        ]
                    )
                    self.driver.execute_script(section_part_script)
            else:
                print("No instructions for", section_name)
            while not has_finished_section:
                try:
                    custom_wait.until(EC.title_is("Section Finished"))
                    has_finished_section = True
                except TimeoutException:
                    pass
            section_parts = section.find_elements_by_class_name(
                "grd-part"
            ) + section.find_elements_by_class_name("lstv-part")
            for part in section_parts:
                classes = part.get_attribute("class")
                part_id = part.get_attribute("id")
                selected = "selected" in classes
                if selected:
                    try:
                        required = (
                            part.find_element_by_id(f"inp_{part_id}").get_attribute(
                                "checked"
                            )
                            == "true"
                        )
                    except NoSuchElementException:
                        required = False
                    print(part_id, required)
                    # if 'grd_part' not in part_id:
                    #     part_id = part_id.replace('part_', 'rad_', 1)
                    selected_parts[part_id] = required
        return selected_parts


def by_amount(item):
    return int(item[1]["amount"].strip("$"))


def get_latest_pc():
    perfect_pc = None
    results_path = get_preferred_path()
    for filepath in glob.glob(f"{results_path}/pc_build_latest.json"):
        with open(filepath, "r") as f:
            perfect_pc = json.load(f)
            print("Loaded from file")
            return perfect_pc


def get_bad_urls(hashed):
    results_path = get_preferred_path()
    if os.path.exists(f"{results_path}/cyber-bad-urls-{hashed}.txt"):
        with open(f"{results_path}/cyber-bad-urls-{hashed}.txt", "r+") as f:
            bad_urls = f.read().split("\n")
            return bad_urls
    return []

def set_preferred_path():
    preferred_path = None
    while preferred_path is None:
        easygui.msgbox(msg="Select a folder to store our results in.")
        preferred_path = easygui.diropenbox(msg="Select a folder to store our results in.", title="Select A Results Folder")
        print(preferred_path)
    with open(f"{real_root}/results-path.txt", "w") as f:
        f.write(preferred_path)
    return preferred_path

def get_preferred_path():
    if os.path.exists(f"{real_root}/results-path.txt"):
        with open(f"{real_root}/results-path.txt", "r") as f:
            preferred_path = f.read()
            if os.path.exists(preferred_path):
                return preferred_path
    return set_preferred_path()

class CyberPowerPcBotController:
    """A program to help build a cost-effective PC."""
    def __init__(self):
        self.path = get_preferred_path()

    def clear_bad_urls(self):
        """Run this command to reset the URLs marked as invalid when trying to find the ideal PC."""
        filepaths = glob.glob(f"{self.path}/cyber-bad-urls-*.txt")
        len_filepaths = len(filepaths)
        if len_filepaths > 0:
            logger.info(f"Clearing {len_filepaths} files")
        else:
            logger.info(f"No files to clear")
        for i, filepath in enumerate(filepaths, start=1):
            os.remove(filepath)
            logger.info(f"Removed file {i}/{len_filepaths}: " + filepath)

    def set_path(self):
        """Use this command to change the location of the results folder."""
        self.path = set_preferred_path()

    def find(self):
        """Use this command to find your ideal PC, at the ideal price! Will run `create` if not run at least once prior."""
        bot = CyberpowerPcBuilderBot()
        # Filter this list for only the PCs I want
        urls = bot.get_urls()
        bestest = {}
        lowest = ""
        lowest_price = 1000000000

        total_time = 0
        perfect_pc = get_latest_pc()
        if not perfect_pc:
            perfect_pc = bot.select_pc_parts()
        hash_perfect_pc = hash(str(perfect_pc.keys()))
        bad_urls = get_bad_urls(hashed=hash_perfect_pc)
        urls = list(set(urls).difference(bad_urls))
        count = len(urls)
        logger.info(f"Processing {count} Possible PCs")
        for index, url in enumerate(urls, start=1):
            start = time.time()
            logger.info(f"Processing PC {index}/{count}")
            try:
                built_pc = bot.build_pc(url, perfect=True, pc=perfect_pc)
            except Exception as e:
                print(e)
                built_pc = None
            if built_pc is not None:
                bestest[url] = built_pc
                amount = int(built_pc.get("amount", "$-1").replace("$", ""))
                if amount > 0 and amount < lowest_price:
                    lowest = url
                    lowest_price = amount
                    logger.info(
                        f"The lowest PC is now: ${lowest_price}\nConfigurator URL: ${lowest}"
                    )
            else:
                bad_urls.append(url)
                logger.error("Could not get amount for URL: {}".format(url))
            end = time.time()
            elapsed_time = end - start
            logger.info(f"Processed PC {index}/{count} in {elapsed_time} seconds")
            total_time += elapsed_time
        now = datetime.now().strftime("%m-%d-%y")
        logger.info(f"Processed {count} PCs in {total_time} seconds")
        with open(f"{self.path}/cyber-bad-urls-{hash_perfect_pc}.txt", "w") as f:
            f.write("\n".join(bad_urls))
        with open(f"{self.path}/cyber-results-{hash_perfect_pc}_{now}.json", "w") as f:
            json.dump(dict(sorted(bestest.items(), key=by_amount)), f, indent=4)
        logger.info("Dumped sorted results to file in folder " + self.path)

    def create(self):
        """Use this command to create your ideal custom PC, meaning the parts not price!"""
        bot = CyberpowerPcBuilderBot()
        bot.select_pc_parts()


if __name__ == "__main__":
    fire.Fire(CyberPowerPcBotController)
