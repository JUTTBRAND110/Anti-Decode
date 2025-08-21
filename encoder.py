import os
import sys
import base64
import zlib
import marshal
from colorama import Fore, Style

# ----------------- CONFIG ----------------- #
APPROVAL_PASSWORD = "JUTT"
LOGO = r"""
     ██ ██    ██ ████████ ████████     
     ██ ██    ██    ██       ██        
     ██ ██    ██    ██       ██        
██   ██ ██    ██    ██       ██        
 █████   ██████     ██       ██
"""
NAME = "JUTT BADSHAH"
# ----------------------------------------- #

def approve():
    print(Fore.GREEN + LOGO)
    print(Fore.GREEN + f"       🔒 Welcome {NAME} 🔒")
    pwd = input(Fore.GREEN + "\n[?] Enter Password for Approval: ")
    if pwd != APPROVAL_PASSWORD:
        print(Fore.RED + "[x] Wrong Password! Access Denied.")
        sys.exit(1)

def encode_marshal(source):
    code = compile(source, "<string>", "exec")
    return f"import marshal\nexec(marshal.loads({repr(marshal.dumps(code))}))"

def encode_base64(source):
    data = base64.b64encode(source.encode()).decode()
    return f"import base64\nexec(base64.b64decode('{data}').decode())"

def encode_zlib_base64(source):
    data = base64.b64encode(zlib.compress(source.encode())).decode()
    return f"import zlib,base64\nexec(zlib.decompress(base64.b64decode('{data}')).decode())"

def encode_powerful(source):
    code = compile(source, "<string>", "exec")
    data = base64.b64encode(zlib.compress(marshal.dumps(code))).decode()
    return f"import marshal,zlib,base64\nexec(marshal.loads(zlib.decompress(base64.b64decode('{data}'))))"

def encode_cython(file_path):
    setup_code = f"""
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("{file_path}", compiler_directives={{"language_level": "3"}})
)
"""
    with open("setup_temp.py", "w") as f:
        f.write(setup_code)

    os.system("pip install cython setuptools wheel > /dev/null 2>&1")
    os.system("python setup_temp.py build_ext --inplace")

    print(Fore.GREEN + f"[✔] Cython build complete! Check for .so file.")
    os.remove("setup_temp.py")

def main():
    approve()
    file_path = input(Fore.GREEN + "\n[?] Enter Python file to encode: ").strip()
    if not os.path.exists(file_path):
        print(Fore.RED + "[x] File not found!")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    print(Fore.GREEN + "\n[ Select Encoding Method ]")
    print(Fore.GREEN + "1. Marshal (Encode)")
    print(Fore.GREEN + "2. Base64 (Encode)")
    print(Fore.GREEN + "3. Zlib + Base64 (Encode)")
    print(Fore.GREEN + "4. Zlib + Base64 + Marshal (Powerful Encode)")
    print(Fore.GREEN + "5. Cython Compile (Generate .so)")

    choice = input(Fore.GREEN + "\n[?] Choose Option (1-5): ").strip()

    output_file = "encoded_output.py"

    if choice == "1":
        encoded = encode_marshal(source)
    elif choice == "2":
        encoded = encode_base64(source)
    elif choice == "3":
        encoded = encode_zlib_base64(source)
    elif choice == "4":
        encoded = encode_powerful(source)
    elif choice == "5":
        encode_cython(file_path)
        return
    else:
        print(Fore.RED + "[x] Invalid Choice!")
        return

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(encoded)

    print(Fore.GREEN + f"\n[✔] File encoded successfully → {output_file}")

if __name__ == "__main__":
    main()
