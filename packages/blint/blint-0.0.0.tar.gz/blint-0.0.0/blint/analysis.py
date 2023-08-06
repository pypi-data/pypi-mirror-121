import json
import os
import sys
from pathlib import Path

import yaml
from rich.progress import Progress

from blint.binary import parse
from blint.logger import LOG
from blint.utils import find_exe_files

rules_file = Path(__file__).parent / "data" / "rules.yml"
review_methods_file = Path(__file__).parent / "data" / "review_methods.yml"

rules_dict = {}
review_methods_dict = {}

# Load the rules
with open(rules_file) as fp:
    raw_data = fp.read().split("---")
    for tmp_data in raw_data:
        rules_list = yaml.safe_load(tmp_data)
        for rule in rules_list:
            rules_dict[rule.get("id")] = rule

# Load the default review methods
with open(review_methods_file) as fp:
    raw_data = fp.read().split("---")
    for tmp_data in raw_data:
        methods_list = yaml.safe_load(tmp_data)
        for rule in methods_list:
            review_methods_dict[rule.get("id")] = rule


def check_nx(f, metadata):
    if metadata.get("has_nx") is False:
        return False
    return True


def check_pie(f, metadata):
    if metadata.get("is_pie") is False:
        return False
    return True


def check_relro(f, metadata):
    if metadata.get("relro") == "no":
        return False
    return True


def run_checks(f, metadata):
    results = []
    if not rules_dict:
        LOG.warn("No rules loaded!")
        return None
    if not metadata:
        return None
    for cid, rule_obj in rules_dict.items():
        cfn = getattr(sys.modules[__name__], cid.lower(), None)
        if cfn:
            result = cfn(f, metadata)
            if result is False:
                rule_obj["filename"] = f
                if metadata.get("name"):
                    rule_obj["exe_name"] = metadata.get("name")
                results.append(rule_obj)
    return results


def start(args, src, report_file):
    files = [src]
    findings = []
    if os.path.isdir(src):
        files = find_exe_files(src)
    with Progress(
        transient=True,
        redirect_stderr=False,
        redirect_stdout=False,
        refresh_per_second=1,
    ) as progress:
        task = progress.add_task(
            f"[green] Scan {len(files)} binaries",
            total=len(files),
            start=True,
        )
        for f in files:
            progress.update(task, description=f"Processing [bold]{f}[/bold]")
            metadata = parse(f)
            with open("out.json", mode="w") as fp:
                json.dump(metadata, fp, indent=True)
            finding = run_checks(f, metadata)
            if finding:
                findings += finding
    return findings
