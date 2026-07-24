"""
Car Repair Process Analysis — BPMN & Petri Net (PNML) structural reader.

Scans the models/ directory for .bpmn and .pnml files and prints a structural summary for each: participants/activities for BPMN, and places/transitions for Petri nets. Originally developed and run as a Kaggle notebook (https://www.kaggle.com/rahman4li/business-process-analysis-and-modeling-car-repair); adapted here to run locally against the models/ folder in this repo.

Usage:
    pip install pandas
    python analyze_process.py
"""

import xml.etree.ElementTree as ET
import pandas as pd
import os

MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")


def detailed_analyze_bpmn(file_path):
    """Extracts participants and process activities from a BPMN file."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        ns = {"bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL"}

        participants = [
            p.get("name") for p in root.findall(".//bpmn:participant", ns) if p.get("name")
        ]

        activities = []
        task_types = ["task", "userTask", "serviceTask", "manualTask"]
        for t_type in task_types:
            for task in root.findall(f".//bpmn:{t_type}", ns):
                name = task.get("name")
                if name:
                    activities.append({"Component": t_type.replace("Task", " Task"), "Activity Name": name})

        return participants, pd.DataFrame(activities)
    except Exception:
        return [], pd.DataFrame()


def detailed_analyze_pnml(file_path):
    """Extracts places (states) and transitions (actions) from a PNML file."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        places = []
        for p in root.findall(".//place"):
            name_node = p.find("./name/text")
            places.append(name_node.text if name_node is not None else p.get("id"))

        transitions = []
        for t in root.findall(".//transition"):
            name_node = t.find("./name/text")
            if name_node is not None and name_node.text:
                transitions.append(name_node.text)

        return (
            pd.DataFrame(places, columns=["States (Places)"]),
            pd.DataFrame(transitions, columns=["Actions (Transitions)"]),
        )
    except Exception:
        return pd.DataFrame(), pd.DataFrame()


def main():
    if not os.path.isdir(MODELS_DIR):
        print(f"Error: models directory not found at {MODELS_DIR}")
        return

    files = []
    for sub in ("bpmn", "pnml"):
        d = os.path.join(MODELS_DIR, sub)
        if os.path.isdir(d):
            files += [os.path.join(d, f) for f in sorted(os.listdir(d))]

    for full_p in files:
        f = os.path.basename(full_p)
        print("-" * 60)
        print(f"ANALYSIS REPORT: {f.upper()}")
        print("-" * 60)

        if f.endswith(".bpmn"):
            parts, act_df = detailed_analyze_bpmn(full_p)
            print(f"Entities: {', '.join(parts) if parts else 'Main Process'}")
            if not act_df.empty:
                print("\nProcess Activities:")
                print(act_df.to_string(index=False))
            else:
                print("\nNo specific activities found in this BPMN model.")

        elif f.endswith(".pnml"):
            places_df, trans_df = detailed_analyze_pnml(full_p)
            print(f"Structural Summary: {len(places_df)} States, {len(trans_df)} Transitions")
            if not trans_df.empty:
                print("\nModel Transitions:")
                print(trans_df.to_string(index=False))

            if "redesign" in f.lower():
                print("\nNote: This model represents the redesigned (cyclic, relaxed-sound) workflow.")
            elif "complete" in f.lower():
                print("\nNote: This model represents the end-to-end integrated process.")

        print()


if __name__ == "__main__":
    main()
