#!/usr/bin/env python3
"""
Puter.js Free AI Chat - Python Client (OpenAI Compatible)
Akses model AI gratis via Puter.js + OpenRouter
"""

import requests
import json
import sys

# Puter.js API Config (OpenAI Compatible)
BASE_URL = "https://api.puter.com/puterai/openai/v1/"

# Available free models
FREE_MODELS = {
    "1": ("meta-llama/llama-3.3-70b-instruct:free", "🦙 Llama 3.3 70B"),
    "2": ("google/gemma-4-31b-it:free", "💎 Gemma 4 31B"),
    "3": ("qwen/qwen3-coder-480b-a35b-instruct:free", "🧠 Qwen3 Coder 480B"),
    "4": ("openai/gpt-oss-20b:free", "🤖 GPT-OSS 20B"),
    "5": ("nvidia/nemotron-3-super-120b-a12b:free", "💚 Nemotron 3 Super 120B"),
    "6": ("nvidia/nemotron-3-nano-30b-a3b:free", "💚 Nemotron 3 Nano 30B"),
    "7": ("nvidia/nemotron-nano-9b-v2:free", "💚 Nemotron Nano 9B"),
}

def chat_withputer(prompt, model="meta-llama/llama-3.3-70b-instruct:free", auth_token=None):
    """
    Send a chat message to Puter.js API (OpenAI Compatible)
    """
    url = f"{BASE_URL}chat/completions"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def display_menu():
    """Display model selection menu"""
    print("\n" + "="*50)
    print("🤖 PUTER.JS FREE AI CHAT")
    print("="*50)
    print("\nPilih model:")
    for key, (model_id, name) in FREE_MODELS.items():
        print(f"  {key}. {name}")
    print(f"  0. Keluar")
    print("="*50)

def main():
    """Main chat loop"""
    print("\n🚀 Puter.js Free AI Chat - Python Client")
    print("Akses model AI gratis via OpenRouter!")
    print("\n⚠️  Catatan: Puter.js memerlukan auth token dari Puter dashboard")
    print("    Buka https://puter.com untuk daftar/login")
    
    auth_token = input("\nMasukkan Puter auth token (atau tekan Enter jika tidak ada): ").strip()
    if not auth_token:
        auth_token = None
        print("⚠️  Running without auth token (mungkin ada limit)")
    
    selected_model = "meta-llama/llama-3.3-70b-instruct:free"
    
    while True:
        display_menu()
        
        choice = input("\nPilihan (1-7, 0=keluar): ").strip()
        
        if choice == "0":
            print("\n👋 Sampai jumpa!")
            break
        elif choice in FREE_MODELS:
            selected_model = FREE_MODELS[choice][0]
            print(f"\n✅ Model dipilih: {FREE_MODELS[choice][1]}")
        else:
            print("\n❌ Pilihan tidak valid!")
            continue
        
        # Chat loop
        print("\n💬 Ketik pesan (ketik 'quit' untuk ganti model, 'exit' untuk keluar):")
        
        while True:
            user_input = input("\n🧑 You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'exit':
                print("\n👋 Sampai jumpa!")
                sys.exit(0)
            elif not user_input:
                continue
            
            print(f"\n🤖 AI ({FREE_MODELS[choice][1]}): ", end="", flush=True)
            
            result = chat_withputer(user_input, selected_model, auth_token)
            
            if "error" in result:
                print(f"\n❌ Error: {result['error']}")
            elif "choices" in result and len(result["choices"]) > 0:
                print(result["choices"][0]["message"]["content"])
            else:
                print(f"\nResponse: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    main()
