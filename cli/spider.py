import argparse
import sys
import os

# إضافة المجلد الحالي إلى مسار بايثون لضمان العثور على الموديولات
sys.path.append(os.getcwd())

def inspect_command(args):
    """أمر فحص الملفات والمجلدات"""
    # استيراد الموديولات داخل الدالة لتجنب أخطاء Circular Import
    try:
        from core.engine import SpiderEngine
        from reporting.formatter import ReportFormatter
    except ImportError as e:
        print(f"[!] Error: Could not import core modules. {e}")
        return

    print(f"[*] Starting Spider Analysis on: {args.paths}...")
    
    # تشغيل المحرك الأساسي
    engine = SpiderEngine(flag_format=args.flag_format)
    challenge_result = engine.run_full_analysis(args.paths)
    
    # طباعة التقرير المنسق
    ReportFormatter.print_summary(challenge_result)

def netcat_command(args):
    """أمر الاتصال بسيرفر Netcat وتحليل البيانات الواردة"""
    try:
        from network.netcat import NetcatClient
        from extractors.base import Extractor
    except ImportError as e:
        print(f"[!] Error: Could not import network modules. {e}")
        return

    print(f"[*] Connecting to {args.host}:{args.port} (Passive Mode)...")
    
    nc = NetcatClient(args.host, args.port)
    data = nc.receive_passive()
    
    print("\n" + "="*20 + " RECEIVED DATA " + "="*20)
    print(data)
    print("=" * 55 + "\n")
    
    # تحليل سريع للبيانات المستلمة
    extractor = Extractor()
    nc_info = {'content': data, 'filepath': 'netcat_stream', 'type': 'text'}
    res = extractor.extract(nc_info)
    
    if res['variables']:
        print("[+] Extracted Variables from stream:")
        for var, val in res['variables'].items():
            print(f"    - {var}: {str(val)[:50]}...")
    else:
        print("[-] No immediate variables detected in the stream.")

def main():
    parser = argparse.ArgumentParser(
        description="🕷️ Spider - CTF Crypto Challenge Analyzer & Interaction Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # خيار تحديد صيغة الـ Flag (Regex)
    parser.add_argument('--flag-format', default=r"flag\{.*?\}", help="Custom flag format regex")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # إعداد أمر Inspect
    inspect_parser = subparsers.add_parser('inspect', help='Analyze files or directories')
    inspect_parser.add_argument('paths', nargs='+', help='Paths to files or directories')
    inspect_parser.set_defaults(func=inspect_command)

    # إعداد أمر Netcat
    netcat_parser = subparsers.add_parser('nc', help='Passive connection to a netcat challenge')
    netcat_parser.add_argument('host', help='Target host/IP')
    netcat_parser.add_argument('port', type=int, help='Target port')
    netcat_parser.set_defaults(func=netcat_command)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        try:
            args.func(args)
        except KeyboardInterrupt:
            print("\n[!] Operation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\n[!] Critical Error: {e}")
            import traceback
            traceback.print_exc()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
