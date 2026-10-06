#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================
HERMES AI AGENT - YANSHEE EMBODIMENT BRIDGE (CLIENT AGENT)
====================================================================
Script ini berjalan di Raspberry Pi dalam robot UBTECH Yanshee.
Menghubungkan mikrofon, speaker, dan 17 servo gerak Yanshee langsung
ke otak Hermes di VPS Cloud (43.134.179.61).
"""

import os
import sys
import time
import json
import socket
import urllib.request
import urllib.parse
import subprocess
import shutil

SERVER_URL = "http://43.134.179.61:8088"
ROBOT_ID = "yanshee_alpha"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# Check available audio players on Linux/Raspbian
def find_audio_player():
    for player in ["mpg123", "ffplay", "mplayer", "cvlc", "aplay", "paplay"]:
        if shutil.which(player):
            return player
    return None

AUDIO_PLAYER = find_audio_player()

def play_audio(file_path):
    print(f"[SPEAKER] Memutar audio: {file_path}")
    if AUDIO_PLAYER == "mpg123":
        subprocess.run(["mpg123", "-q", file_path])
    elif AUDIO_PLAYER == "ffplay":
        subprocess.run(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", file_path])
    elif AUDIO_PLAYER == "mplayer":
        subprocess.run(["mplayer", "-really-quiet", file_path])
    elif AUDIO_PLAYER == "cvlc":
        subprocess.run(["cvlc", "--play-and-exit", "--quiet", file_path])
    elif AUDIO_PLAYER == "aplay":
        # If wav format
        subprocess.run(["aplay", "-q", file_path])
    else:
        # Fallback to python sound
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except Exception as e:
            print(f"[WARN] Tidak menemukan player audio, mencoba aplay/mpg123 via os.system: {e}")
            os.system(f"mpg123 '{file_path}' 2>/dev/null || ffplay -nodisp -autoexit '{file_path}' 2>/dev/null")

# Try to initialize YanAPI if installed on Yanshee
yan_motion = None
try:
    import YanAPI
    YanAPI.yan_api_init()
    yan_motion = YanAPI
    print("[YANAPI] Berhasil terhubung ke hardware robot Yanshee (YanAPI)!")
except Exception:
    pass

def trigger_motion(motion_name):
    if yan_motion:
        try:
            print(f"[MOTION] Menjalankan gerakan fisik: {motion_name}")
            yan_motion.start_play_motion(name=motion_name)
        except Exception as e:
            print(f"[MOTION ERROR] Gagal menjalankan gerakan {motion_name}: {e}")
    else:
        # Check if local Yanshee REST API is running on port 9090
        try:
            req = urllib.request.Request(
                f"http://127.0.0.1:9090/v1/motions/play?name={motion_name}",
                method="PUT"
            )
            urllib.request.urlopen(req, timeout=2)
            print(f"[MOTION REST] Gerakan {motion_name} dikirim ke local port 9090")
        except Exception:
            pass

def register():
    local_ip = get_local_ip()
    hostname = socket.gethostname()
    payload = {
        "robot_id": ROBOT_ID,
        "ip": local_ip,
        "hostname": hostname,
        "audio_player": AUDIO_PLAYER,
        "has_yanapi": yan_motion is not None
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{SERVER_URL}/api/yanshee/register",
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "Yanshee-Client/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            res = json.loads(resp.read().decode())
            print(f"[ONLINE] Terdaftar di Hermes VPS: {res.get('message')}")
            return True
    except Exception as e:
        print(f"[CONNECT ERROR] Gagal terhubung ke Hermes VPS: {e}")
        return False

def report_status(task_id, status, message):
    payload = {"task_id": task_id, "status": status, "message": message}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{SERVER_URL}/api/yanshee/report",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass

def poll_and_execute():
    req = urllib.request.Request(
        f"{SERVER_URL}/api/yanshee/poll?robot_id={ROBOT_ID}&ip={get_local_ip()}",
        headers={"User-Agent": "Yanshee-Client/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            tasks = json.loads(resp.read().decode()).get("tasks", [])
            for task in tasks:
                task_id = task.get("id")
                action = task.get("action")
                text = task.get("text", "")
                audio_url = task.get("audio_url")
                motion = task.get("motion")

                print(f"\n[TASK DITERIMA] #{task_id} -> Action: {action}, Text: \"{text}\"")
                
                # If motion requested
                if motion:
                    trigger_motion(motion)

                # If speech requested
                if audio_url:
                    full_audio_url = audio_url if audio_url.startswith("http") else f"{SERVER_URL}{audio_url}"
                    local_audio = f"/tmp/speech_{task_id}.mp3"
                    try:
                        urllib.request.urlretrieve(full_audio_url, local_audio)
                        play_audio(local_audio)
                        report_status(task_id, "completed", f"Berhasil berbicara: {text}")
                    except Exception as err:
                        print(f"[AUDIO ERROR] Gagal download/play: {err}")
                        report_status(task_id, "failed", str(err))
                else:
                    report_status(task_id, "completed", "Aksi selesai")

    except Exception as e:
        # Timeout is normal for polling
        pass

def main():
    print("=" * 60)
    print("🤖 UBTECH YANSHEE - HERMES EMBODIMENT BRIDGE CLIENT")
    print(f"Server Target : {SERVER_URL}")
    print(f"Local IP      : {get_local_ip()}")
    print(f"Audio Output  : {AUDIO_PLAYER or 'System Default / Pygame'}")
    print("=" * 60)

    # Initial greeting trigger
    trigger_motion("stand")
    time.sleep(0.5)

    connected = False
    while not connected:
        connected = register()
        if not connected:
            print("[RETRY] Mencoba menghubungkan ulang ke VPS dalam 3 detik...")
            time.sleep(3)

    print("\n[READY] Yanshee siap menerima instruksi suara dan gerak dari Hermes!")
    while True:
        try:
            poll_and_execute()
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n[STOP] Yanshee agent dimatikan.")
            break
        except Exception as e:
            time.sleep(2)

if __name__ == "__main__":
    main()
