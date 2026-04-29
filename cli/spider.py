import argparse
import sys
import os

# إضافة المجلد الحالي إلى مسار بايثون لضمان العثور على الموديولات
sys.path.append(os.getcwd())

def interactive_command(args):
    """الوضع التفاعلي للتعامل المباشر مع المستخدم"""
    print("\n" + "🕸️ " * 5 + " SPIDER INTERACTIVE MODE " + "🕸️ " * 5)
    print("Type 'exit' to return to main menu.\n")
    
    while True:
        print("[1] Classical Decryption (Base64, Caesar, XOR, Vigenere, Atbash)")
        print("[2] Manual RSA Input")
        print("[3] Change Flag Format (Current: " + args.flag_format + ")")
        print("[0] Exit")
        
        choice = input("\n[Spider] Select option: ").strip()
        
        if choice == '0' or choice.lower() == 'exit':
            break
            
        if choice == '1':
            data = input("[Spider] Enter ciphertext: ").strip()
            from crypto.classical.solvers import ClassicalSolvers
            
            print("\n--- Classical Analysis ---")
            # 1. Base64
            b64_res = ClassicalSolvers.solve_base64(data)
            if b64_res: print(f"[+] Base64 Decoded: {b64_res}")
            
            # 2. Atbash
            atbash_res = ClassicalSolvers.solve_atbash(data)
            print(f"[+] Atbash Result: {atbash_res}")
            
            # 3. Caesar
            caesar_res = ClassicalSolvers.solve_caesar(data, flag_format=args.flag_format.split('{')[0])
            if caesar_res:
                print("[*] Caesar Potential Results:")
                for res in caesar_res:
                    if res.get('found'):
                        print(f"    [!] MATCH FOUND (Shift {res['shift']}): {res['text']}")
                    elif args.flag_format.split('{')[0].lower() in res['text'].lower():
                         print(f"    [!] Potential Match (Shift {res['shift']}): {res['text']}")
            
            # 4. Vigenere
            vig_key = input("[Spider] Enter Vigenere key (leave empty to skip): ").strip()
            if vig_key:
                vig_res = ClassicalSolvers.solve_vigenere(data, vig_key)
                if vig_res:
                    print(f"[+] Vigenere (Mode 1 - Decrypt): {vig_res['decrypted']}")
                    print(f"[+] Vigenere (Mode 2 - Encrypt): {vig_res['encrypted']}")
            
            # 5. XOR
            xor_key = input("[Spider] Enter XOR key (leave empty to skip): ").strip()
            if xor_key:
                xor_res = ClassicalSolvers.solve_xor(data, xor_key)
                if xor_res: print(f"[+] XOR Result: {xor_res}")
            print("--------------------------\n")

        elif choice == '2':
            try:
                n_str = input("[Spider] Enter n: ").strip()
                e_str = input("[Spider] Enter e: ").strip()
                c_str = input("[Spider] Enter c: ").strip()
                
                n = int(n_str, 0) if n_str else 0
                e = int(e_str, 0) if e_str else 0
                c = int(c_str, 0) if c_str else 0
                
                from reporting.formatter import ReportFormatter
                from models.challenge import CryptoChallenge
                from analyzers.engine import Analyzer
                
                challenge = CryptoChallenge(name="Manual RSA Input")
                challenge.variables = {'n': n, 'e': e, 'c': c}
                
                analyzer = Analyzer(flag_format=args.flag_format)
                findings, flags = analyzer.analyze({'variables': challenge.variables}, raw_contents=[])
                
                challenge.flag_candidates = flags
                if findings:
                    challenge.detected_type = findings[0]['type']
                    challenge.confidence = findings[0]['confidence']
                    challenge.details = findings[0]['details']
                    challenge.suggestions = findings[0].get('suggestions', [])
                
                ReportFormatter.print_summary(challenge)
            except Exception as ex:
                print(f"[!] Error: Invalid input. {ex}")

        elif choice == '3':
            args.flag_format = input("[Spider] Enter new flag format (regex): ").strip()
            print(f"[*] Flag format updated to: {args.flag_format}")

def main():
    parser = argparse.ArgumentParser(
        description="🕷️ Spider - CTF Crypto Challenge Analyzer & Interaction Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--flag-format', default=r"flag\{.*?\}", help="Custom flag format regex")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # أمر التفتيش
    inspect_parser = subparsers.add_parser('inspect', help='Analyze files or directories')
    inspect_parser.add_argument('paths', nargs='+', help='Paths to files or directories')
    inspect_parser.set_defaults(func=lambda args: exec(
        "from core.engine import SpiderEngine; "
        "from reporting.formatter import ReportFormatter; "
        "engine = SpiderEngine(flag_format=args.flag_format); "
        "res = engine.run_full_analysis(args.paths); "
        "ReportFormatter.print_summary(res)"
    ))

    # أمر التفاعل
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive mode')
    interactive_parser.set_defaults(func=interactive_command)

    # أمر Netcat
    netcat_parser = subparsers.add_parser('nc', help='Passive connection to a netcat challenge')
    netcat_parser.add_argument('host', help='Target host/IP')
    netcat_parser.add_argument('port', type=int, help='Target port')
    netcat_parser.set_defaults(func=lambda args: exec(
        "from network.netcat import NetcatClient; from extractors.base import Extractor; "
        "nc = NetcatClient(args.host, args.port); data = nc.receive_passive(); "
        "print(f'\\nReceived Data:\\n{data}\\n'); "
        "res = Extractor().extract({'content': data, 'filepath': 'netcat', 'type': 'text'}); "
        "if res['variables']: print('[+] Extracted Variables:'); [print(f'    - {k}: {v}') for k, v in res['variables'].items()]"
    ))

    args = parser.parse_args()

    if hasattr(args, 'func'):
        try:
            args.func(args)
        except KeyboardInterrupt:
            print("\n[!] Operation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\n[!] Critical Error: {e}")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
